#本文件是对模型回答的结果进行评判
import json
import model
import operate_excel
import tool
from threading import Thread

#提取不符合json规则的字符串中的JSON字符串,deepseek在输出judge结果的时候，总是带一些前缀，然后再跟上一个json字符串
def json_string(text):
    start_index = text.find('{')
    end_index = text.rfind('}') + 1
    json_string = text[start_index:end_index]
    return json_string

#安全解析json_str
def safe_parse_json(json_str):
    try:
        # 解析JSON字符串
        json_dict = json.loads(json_str)
        x = json_dict['x'] # 获取X值
        y = json_dict['y']
        effective = json_dict['effective']
        effective.sort()
        return x, y, effective

    except json.JSONDecodeError as e:
        print(f"JSON格式错误 - {e}")
    except KeyError as e:
        key = str(e).strip("'")
        if key == 'X':
            print(" JSON中缺少'X'键")
        elif key == 'Y':
            print("JSON中缺少'Y'键")
        elif key == 'effective':
            print("JSON中缺少'effective'键")
        else:
            print(f"键错误: 缺少键 {e}")
    except AttributeError as e:
        print(f" effective不是可排序的类型 - {e}")

#异常日志记录
def save_judge_log(text):
    file_path = 'D:/study/PyCharm/WorkHouse/pycharmtest/test/file/judge_log.txt'
    file = open(file_path, 'a', encoding='utf-8')
    file.write(text)
    file.write('\n')
    file.close()

#使用deepseek模型进行评判(输入：模型回答的文本、测试试题的答案、答案中要点个位、excel文件路径、表单名称、题目id、reason列、text列：输出：X、Y、effective[])
def use_deepseek_judge(text_model, text_explain, num, file_path, sheet_name, question_id, col_judge_reason_text, col_judge_text):
    # 拼装提示词(此处模型在该提示下，指令遵循出现异常的次数为：5次，其中1次为各式错误，4次为模型响应异常。人工抽样判断与模型判断的一致性：)
    prompt = ("现在你是一个评估大模型生成内容好坏的评委，你需要完成以下四项工作："
              "\n第一、将测试用例中的标准答案和模型的回答进行对比（测试用例中的答案要点用'1.'、'2.'、'3.'等字符做了标注）。"
              "\n第二、计算出模型给出的解释的总个数和模型给出的有效解释的个数，分别赋值给x和y；"
              "\n  要点划分规则："
              "\n    1. 显式划分：如果模型回答使用了明确的编号（如'1.','2.','3.'或'a)','b)','c)'等）、项目符号（如'•', '-', '*'）或分段，按这些标记划分要点"
              "\n    2. 隐式划分：如果没有明确标记，按以下标准划分："
              "\n      - 语义完整性：每个要点应表达一个相对完整的意思"
              "\n      - 逻辑分隔：根据句号、分号、换行等自然语言分隔符"
              "\n      - 连接词提示：注意'首先'、'其次'、'另外'、'此外'、'同时'、'另一方面'等逻辑连接词"
              "\n      - 主题一致性：同一要点内应保持主题一致，主题变化通常意味着新要点的开始"
              "\n     3. 合并处理：如果模型将多个相关但独立的观点放在同一个编号或段落中，且这些观点在标准答案中属于不同要点，应将其拆分为多个要点"
              "\n     4. 排除标准：以下情况不计为独立要点："
              "\n      - 过渡性语句（如'总的来说'、'综上所述'）"
              "\n      - 重复表述（用不同方式说同一内容）"
              "\n      - 过于笼统或无关的陈述"
              "\n  有效解释的判断标准："
              "\n    1.内容相关性：模型回答的要点必须与标准答案中的某个要点在语义上相关"
              "\n    2.信息完整性：可以多个模型要点共同覆盖一个标准答案要点"
              "\n    3.准确性：信息正确无误，不包含错误或误导性内容"
              "\n    4.不重复计数：即使多个模型要点对应同一个标准要点，也要分别记录"
              "\n第三、列出模型给出的有效解释在答案中对应的编号，存入数组effective[]中；"
              "\n第四、仅需输出包含x、y和effective[]的json格式的字符串即可。"

              "\n(重要说明："
              "\n1. 如果模型的回答中，有多个要点合并在一起恰好覆盖标准答案中的一个要点，那么这些模型回答的要点都应分别列出"
              "\n2. 如果模型的回答中的，全部要点合并在一起也不能覆盖标准答案中的一个要点，那么这些模型回答的要点均计为无效"
              "\n3. effective数组中元素的顺序应该对应模型回答中要点的出现顺序"
              "\n4. 如果模型回答的要点包含标准答案中没有的额外信息，但只要核心内容正确且相关，仍视为有效"
              "\n5. 如果模型回答的要点部分正确但包含错误信息，则该要点计为无效)"

              "\n示例：标准答案中有3个要点，模型回答了5个要点，其中："
              "\n- 模型回答的第1个、第2个和第5个要点共同完整覆盖了标准答案的要点1"
              "\n- 模型回答的第3个要点对应标准答案中的第3个要点"
              "\n- 模型回答的第4个要点没有对应任何标准答案要点"
              "\n那么x=5、y=4、effective=[1, 1, 3, 1]，最终输出：{\"x\": 5, \"y\": 4, \"effective\": [1, 1, 3, 1]}"

              "\n\n******测试用例的标准答案：" + text_explain +
              "\n\n其中，测试用例中的答案要点个数为:" + str(num) + "个。" +
              "\n\n******模型的回答：" + text_model)
    judge_reason_text , judge_text = model.deepseek_reasoner(prompt)#提取deepseek_reason模型作为裁判
    #及时保存模型输出，防止后续因解析原因导致程序异常，跳到下一个题目
    operate_excel.write_excel(file_path,
                              sheet_name, question_id,
                              col_judge_reason_text, judge_reason_text)
    operate_excel.write_excel(file_path,sheet_name, question_id,col_judge_text, judge_text)
    x, y, effective = safe_parse_json(judge_text)
    return  x, y, effective

def judge_deepseek_v3_2_exp_thread():
    file_path = "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark.xlsx"
    # 标记现在正在执行的题目
    for question_id in range(513, 526):
        try:
            text_model = operate_excel.read_excel(file_path,"DeepSeek_V3.2_Exp", question_id, 1)  # 第question_id题模型回答的答案
            #判断该题目模型是否有回答
            if type(text_model) != float: #如果为空pandas读excel输出的就是float类型的nan
                text_explain = operate_excel.read_excel(file_path,"benchmark", question_id, 6) #第question_id题的标准答案
                num = operate_excel.read_excel(file_path,"benchmark", question_id, 7)  # 答案中要点个数
                x, y, effective = use_deepseek_judge(text_model, text_explain, num, file_path, "DeepSeek_V3.2_Exp", question_id,5,6)
                #保存评判结果及实验过程
                operate_excel.write_excel(file_path,"DeepSeek_V3.2_Exp", question_id,2, x)
                operate_excel.write_excel(file_path,"DeepSeek_V3.2_Exp", question_id,3, y)
                operate_excel.write_excel(file_path,"DeepSeek_V3.2_Exp", question_id,4,effective)
                print(f"对deepseek_V3_2_Exp模型回答的第{question_id}个题评判完毕")
        except Exception as e:
            print(f"模型在对deepseek_V3_2_Exp模型回答的第{question_id}题进行判断时，捕获到异常: {type(e).__name__}: {e}")
            save_judge_log("评判deepseek_V3_2_Exp模型回答的第"+str(question_id)+"题时，出现异常！！！异常为:"+type(e).__name__+":"+str(e)) #将异常写入到judge_log.txt文件中
            continue
    print("###################judge_deepseek_v3_2_exp_thread线程结束")

def judge_deepseek_v3_2_exp_reasoner_thread():
    file_path = "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_DeepSeek_V3.2_Exp_reasoner.xlsx"
    # 标记现在正在执行的题目
    for question_id in range(513, 526):
        try:
            text_model = operate_excel.read_excel(file_path,"DeepSeek_V3.2_Exp_reasoner", question_id, 2)  # 第question_id题模型回答的答案
            #判断该题目模型是否有回答
            if type(text_model) != float: #如果为空pandas读excel输出的就是float类型的nan
                text_explain = operate_excel.read_excel(file_path,"benchmark", question_id, 6) #第question_id题的标准答案
                num = operate_excel.read_excel(file_path,"benchmark", question_id, 7)  # 答案中要点个数
                x, y, effective = use_deepseek_judge(text_model, text_explain, num, file_path, "DeepSeek_V3.2_Exp_reasoner", question_id,6,7)
                #保存评判结果及实验过程
                operate_excel.write_excel(file_path,"DeepSeek_V3.2_Exp_reasoner", question_id,3, x)
                operate_excel.write_excel(file_path,"DeepSeek_V3.2_Exp_reasoner", question_id,4, y)
                operate_excel.write_excel(file_path,"DeepSeek_V3.2_Exp_reasoner", question_id,5,effective)
                print(f"对deepseek_v3_2_exp_reasoner模型回答的第{question_id}个题评判完毕")
        except Exception as e:
            print(f"模型在对deepseek_v3_2_exp_reasoner模型回答的第{question_id}题进行判断时，捕获到异常: {type(e).__name__}: {e}")
            save_judge_log("评判deepseek_v3_2_exp_reasoner模型回答的第"+str(question_id)+"题时，出现异常！！！异常为:"+type(e).__name__+":"+str(e)) #将异常写入到judge_log.txt文件中
            continue
    print("###################judge_deepseek_v3_2_exp_thread线程结束")

def judge_dou_bao_seed_1_6_thinking_25071_thread():
    file_path = "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_dou_bao_seed_1_6_thinking_25071.xlsx"
    # 标记现在正在执行的题目
    for question_id in range(308, 309):
        try:
            text_model = operate_excel.read_excel(file_path,"dou_bao_seed_1_6_thinking_25071", question_id, 2)  # 第question_id题模型回答的答案
            #判断该题目模型是否有回答
            if type(text_model) != float: #如果为空pandas读excel输出的就是float类型的nan
                text_explain = operate_excel.read_excel(file_path,"benchmark", question_id, 6) #第question_id题的标准答案
                num = operate_excel.read_excel(file_path,"benchmark", question_id, 7)  # 答案中要点个数
                x, y, effective = use_deepseek_judge(text_model, text_explain, num, file_path, "dou_bao_seed_1_6_thinking_25071", question_id,6,7)
                #保存评判结果及实验过程
                operate_excel.write_excel(file_path,"dou_bao_seed_1_6_thinking_25071", question_id,3, x)
                operate_excel.write_excel(file_path,"dou_bao_seed_1_6_thinking_25071", question_id,4, y)
                operate_excel.write_excel(file_path,"dou_bao_seed_1_6_thinking_25071", question_id,5,effective)
                print(f"对dou_bao_seed_1_6_thinking_25071模型回答的第{question_id}个题评判完毕")
        except Exception as e:
            print(f"模型在对dou_bao_seed_1_6_thinking_25071模型回答的第{question_id}题进行判断时，捕获到异常: {type(e).__name__}: {e}")
            save_judge_log("评判dou_bao_seed_1_6_thinking_25071模型回答的第"+str(question_id)+"题时，出现异常！！！异常为:"+type(e).__name__+":"+str(e)) #将异常写入到judge_log.txt文件中
            continue
    print("###################judge_dou_bao_seed_1_6_thinking_25071_thread线程结束")

def judge_glm_4_5v_thread():
    file_path = "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_glm_4_5v.xlsx"
    # 标记现在正在执行的题目
    for question_id in range(446, 447):
        try:
            text_model = operate_excel.read_excel(file_path,"glm_4_5v", question_id, 2)  # 第question_id题模型回答的答案
            #判断该题目模型是否有回答
            if type(text_model) != float: #如果为空pandas读excel输出的就是float类型的nan
                text_explain = operate_excel.read_excel(file_path,"benchmark", question_id, 6) #第question_id题的标准答案
                num = operate_excel.read_excel(file_path,"benchmark", question_id, 7)  # 答案中要点个数
                x, y, effective = use_deepseek_judge(text_model, text_explain, num, file_path, "glm_4_5v", question_id,6,7)
                #保存评判结果及实验过程
                operate_excel.write_excel(file_path,"glm_4_5v", question_id,3, x)
                operate_excel.write_excel(file_path,"glm_4_5v", question_id,4, y)
                operate_excel.write_excel(file_path,"glm_4_5v", question_id,5,effective)
                print(f"对glm_4_5v模型回答的第{question_id}个题评判完毕")
        except Exception as e:
            print(f"模型在对glm_4_5v模型回答的第{question_id}题进行判断时，捕获到异常: {type(e).__name__}: {e}")
            save_judge_log("评判glm_4_5v模型回答的第"+str(question_id)+"题时，出现异常！！！异常为:"+type(e).__name__+":"+str(e)) #将异常写入到judge_log.txt文件中
            continue
    print("###################judge_glm_4_5v_thread线程结束")

def judge_glm_4_6_thread():
    file_path = "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_glm_4_6.xlsx"
    # 标记现在正在执行的题目
    for question_id in range(526, 526):
        try:
            text_model = operate_excel.read_excel(file_path,"glm_4_6", question_id, 2)  # 第question_id题模型回答的答案
            #判断该题目模型是否有回答
            if type(text_model) != float: #如果为空pandas读excel输出的就是float类型的nan
                text_explain = operate_excel.read_excel(file_path,"benchmark", question_id, 6) #第question_id题的标准答案
                num = operate_excel.read_excel(file_path,"benchmark", question_id, 7)  # 答案中要点个数
                x, y, effective = use_deepseek_judge(text_model, text_explain, num, file_path, "glm_4_6", question_id,6,7)
                #保存评判结果及实验过程
                operate_excel.write_excel(file_path,"glm_4_6", question_id,3, x)
                operate_excel.write_excel(file_path,"glm_4_6", question_id,4, y)
                operate_excel.write_excel(file_path,"glm_4_6", question_id,5,effective)
                print(f"对glm_4_6模型回答的第{question_id}个题评判完毕")
        except Exception as e:
            print(f"模型在对glm_4_6模型回答的第{question_id}题进行判断时，捕获到异常: {type(e).__name__}: {e}")
            save_judge_log("评判glm_4_6模型回答的第"+str(question_id)+"题时，出现异常！！！异常为:"+type(e).__name__+":"+str(e)) #将异常写入到judge_log.txt文件中
            continue
    print("###################judge_glm_4_6_thread线程结束")

def judge_qwen3_max_thread():
    file_path = "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_qwen3_max.xlsx"
    # 标记现在正在执行的题目
    for question_id in range(404, 526):
        try:
            text_model = operate_excel.read_excel(file_path,"qwen3_max", question_id, 1)  # 第question_id题模型回答的答案
            #判断该题目模型是否有回答
            if type(text_model) != float: #如果为空pandas读excel输出的就是float类型的nan
                text_explain = operate_excel.read_excel(file_path,"benchmark", question_id, 6) #第question_id题的标准答案
                num = operate_excel.read_excel(file_path,"benchmark", question_id, 7)  # 答案中要点个数
                x, y, effective = use_deepseek_judge(text_model, text_explain, num, file_path, "qwen3_max", question_id,5,6)
                #保存评判结果及实验过程
                operate_excel.write_excel(file_path,"qwen3_max", question_id,2, x)
                operate_excel.write_excel(file_path,"qwen3_max", question_id,3, y)
                operate_excel.write_excel(file_path,"qwen3_max", question_id,4,effective)
                print(f"对qwen3_max模型回答的第{question_id}个题评判完毕")
        except Exception as e:
            print(f"模型在对qwen3_max模型回答的第{question_id}题进行判断时，捕获到异常: {type(e).__name__}: {e}")
            save_judge_log("评判qwen3_max模型回答的第"+str(question_id)+"题时，出现异常！！！异常为:"+type(e).__name__+":"+str(e)) #将异常写入到judge_log.txt文件中
            continue
    print("###################judge_qwen3_max_thread线程结束")

def judge_qwen3_next_80b_a3b_thinking_thread():
    file_path = "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_qwen3_next_80b_a3b_thinking.xlsx"
    # 标记现在正在执行的题目
    for question_id in range(343, 344):
        try:
            text_model = operate_excel.read_excel(file_path,"qwen3_next_80b_a3b_thinking", question_id, 2)  # 第question_id题模型回答的答案
            #判断该题目模型是否有回答
            if type(text_model) != float: #如果为空pandas读excel输出的就是float类型的nan
                text_explain = operate_excel.read_excel(file_path,"benchmark", question_id, 6) #第question_id题的标准答案
                num = operate_excel.read_excel(file_path,"benchmark", question_id, 7)  # 答案中要点个数
                x, y, effective = use_deepseek_judge(text_model, text_explain, num, file_path, "qwen3_next_80b_a3b_thinking", question_id,6,7)
                #保存评判结果及实验过程
                operate_excel.write_excel(file_path,"qwen3_next_80b_a3b_thinking", question_id,3, x)
                operate_excel.write_excel(file_path,"qwen3_next_80b_a3b_thinking", question_id,4, y)
                operate_excel.write_excel(file_path,"qwen3_next_80b_a3b_thinking", question_id,5,effective)
                print(f"对qwen3_next_80b_a3b_thinking模型回答的第{question_id}个题评判完毕")
        except Exception as e:
            print(f"模型在对qwen3_next_80b_a3b_thinking模型回答的第{question_id}题进行判断时，捕获到异常: {type(e).__name__}: {e}")
            save_judge_log("评判qwen3_next_80b_a3b_thinking模型回答的第"+str(question_id)+"题时，出现异常！！！异常为:"+type(e).__name__+":"+str(e)) #将异常写入到judge_log.txt文件中
            continue
    print("###################judge_qwen3_next_80b_a3b_thinking_thread线程结束")

def judge_gpt_5_high_thread():
    file_path = "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_gpt_5_high.xlsx"
    # 标记现在正在执行的题目
    for question_id in [90,319,485,488,492]:
        try:
            text_model = operate_excel.read_excel(file_path,"gpt_5_high", question_id, 1)  # 第question_id题模型回答的答案
            #判断该题目模型是否有回答
            if type(text_model) != float: #如果为空pandas读excel输出的就是float类型的nan
                text_explain = operate_excel.read_excel(file_path,"benchmark", question_id, 6) #第question_id题的标准答案
                num = operate_excel.read_excel(file_path,"benchmark", question_id, 7)  # 答案中要点个数
                x, y, effective = use_deepseek_judge(text_model, text_explain, num, file_path, "gpt_5_high", question_id,5,6)
                #保存评判结果及实验过程
                operate_excel.write_excel(file_path,"gpt_5_high", question_id,2, x)
                operate_excel.write_excel(file_path,"gpt_5_high", question_id,3, y)
                operate_excel.write_excel(file_path,"gpt_5_high", question_id,4,effective)
                print(f"对gpt_5_high模型回答的第{question_id}个题评判完毕")
        except Exception as e:
            print(f"模型在对gpt_5_high模型回答的第{question_id}题进行判断时，捕获到异常: {type(e).__name__}: {e}")
            save_judge_log("评判gpt_5_high模型回答的第"+str(question_id)+"题时，出现异常！！！异常为:"+type(e).__name__+":"+str(e)) #将异常写入到judge_log.txt文件中
            continue
    print("###################judge_gpt_5_high_thread线程结束")

def judge_o4_mini_high_thread():
    file_path = "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_o4_mini_high.xlsx"
    # 标记现在正在执行的题目
    for question_id in [101,253,263,265,435,473]:
        try:
            text_model = operate_excel.read_excel(file_path,"o4_mini_high", question_id, 1)  # 第question_id题模型回答的答案
            #判断该题目模型是否有回答
            if type(text_model) != float: #如果为空pandas读excel输出的就是float类型的nan
                text_explain = operate_excel.read_excel(file_path,"benchmark", question_id, 6) #第question_id题的标准答案
                num = operate_excel.read_excel(file_path,"benchmark", question_id, 7)  # 答案中要点个数
                x, y, effective = use_deepseek_judge(text_model, text_explain, num, file_path, "o4_mini_high", question_id,5,6)
                #保存评判结果及实验过程
                operate_excel.write_excel(file_path,"o4_mini_high", question_id,2, x)
                operate_excel.write_excel(file_path,"o4_mini_high", question_id,3, y)
                operate_excel.write_excel(file_path,"o4_mini_high", question_id,4,effective)
                print(f"对o4_mini_high模型回答的第{question_id}个题评判完毕")
        except Exception as e:
            print(f"模型在对o4_mini_high模型回答的第{question_id}题进行判断时，捕获到异常: {type(e).__name__}: {e}")
            save_judge_log("评判o4_mini_high模型回答的第"+str(question_id)+"题时，出现异常！！！异常为:"+type(e).__name__+":"+str(e)) #将异常写入到judge_log.txt文件中
            continue
    print("###################judge_o4_mini_high_thread线程结束")

def judge_claude_sonnet_4_5_thinking_thread():
    file_path = "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_claude_sonnet_4_5_thinking.xlsx"
    # 标记现在正在执行的题目
    for question_id in [31, 105,129,264,283,408,424]:
        try:
            text_model = operate_excel.read_excel(file_path,"claude_sonnet_4_5_thinking", question_id, 2)  # 第question_id题模型回答的答案
            #判断该题目模型是否有回答
            if type(text_model) != float: #如果为空pandas读excel输出的就是float类型的nan
                text_explain = operate_excel.read_excel(file_path,"benchmark", question_id, 6) #第question_id题的标准答案
                num = operate_excel.read_excel(file_path,"benchmark", question_id, 7)  # 答案中要点个数
                x, y, effective = use_deepseek_judge(text_model, text_explain, num, file_path, "claude_sonnet_4_5_thinking", question_id,6,7)
                #保存评判结果及实验过程
                operate_excel.write_excel(file_path,"claude_sonnet_4_5_thinking", question_id,3, x)
                operate_excel.write_excel(file_path,"claude_sonnet_4_5_thinking", question_id,4, y)
                operate_excel.write_excel(file_path,"claude_sonnet_4_5_thinking", question_id,5,effective)
                print(f"对claude_sonnet_4_5_thinking模型回答的第{question_id}个题评判完毕")
        except Exception as e:
            print(f"模型在对claude_sonnet_4_5_thinking模型回答的第{question_id}题进行判断时，捕获到异常: {type(e).__name__}: {e}")
            save_judge_log("评判claude_sonnet_4_5_thinking模型回答的第"+str(question_id)+"题时，出现异常！！！异常为:"+type(e).__name__+":"+str(e)) #将异常写入到judge_log.txt文件中
            continue
    print("###################judge_claude_sonnet_4_5_thinkingh_thread线程结束")

def judge_gemini_2_5_pro_thread():
    file_path = "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_gemini_2_5_pro.xlsx"
    # 标记现在正在执行的题目
    for question_id in [181,358,373,384]:
        try:
            text_model = operate_excel.read_excel(file_path,"gemini_2_5_pro", question_id, 1)  # 第question_id题模型回答的答案
            #判断该题目模型是否有回答
            if type(text_model) != float: #如果为空pandas读excel输出的就是float类型的nan
                text_explain = operate_excel.read_excel(file_path,"benchmark", question_id, 6) #第question_id题的标准答案
                num = operate_excel.read_excel(file_path,"benchmark", question_id, 7)  # 答案中要点个数
                x, y, effective = use_deepseek_judge(text_model, text_explain, num, file_path, "gemini_2_5_pro", question_id,5,6)
                #保存评判结果及实验过程
                operate_excel.write_excel(file_path,"gemini_2_5_pro", question_id,2, x)
                operate_excel.write_excel(file_path,"gemini_2_5_pro", question_id,3, y)
                operate_excel.write_excel(file_path,"gemini_2_5_pro", question_id,4,effective)
                print(f"对gemini_2_5_pro模型回答的第{question_id}个题评判完毕")
        except Exception as e:
            print(f"模型在对gemini_2_5_pro模型回答的第{question_id}题进行判断时，捕获到异常: {type(e).__name__}: {e}")
            save_judge_log("评判gemini_2_5_pro模型回答的第"+str(question_id)+"题时，出现异常！！！异常为:"+type(e).__name__+":"+str(e)) #将异常写入到judge_log.txt文件中
            continue
    print("###################judge_gemini_2_5_pro_thread线程结束")


#下面是main函数
if __name__ == '__main__':
    try:
        thread1 = Thread(target = judge_gpt_5_high_thread)
        thread2 = Thread(target = judge_o4_mini_high_thread)
        thread3 = Thread(target = judge_claude_sonnet_4_5_thinking_thread)
        thread4 = Thread(target = judge_gemini_2_5_pro_thread)
        #thread5 = Thread(target = judge_qwen3_max_thread)
        #thread6 = Thread(target = judge_qwen3_next_80b_a3b_thinking_thread)

        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        #thread5.start()
        #thread6.start()



        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        #thread5.join()
        #thread6.join()


    except Exception as e:
        # 捕获所有常规异常
        #print(f"捕获到异常: {type(e).__name__}: {e}")
        tool.send_email("1902900584@qq.com", "异常中断提醒", "邮件的内容")
    finally:
        tool.send_email("1902900584@qq.com", "正常运行结束提醒", "邮件的内容")

