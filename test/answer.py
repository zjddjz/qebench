#本文件是将benchmark中的问题对各个模型进行测试，将模型回答的结果保存在txt文档中。
from openai import images
import operate_excel
import model
from threading import Thread
import tool


#拼接图片真实地址
def image_address_real(image):
    for i in range(len(image)):
        image[i] = "C:/Users/19029/Desktop/explainBenchmark/image" + image[i]
    return image

#查看编号为id的试题第4列是否为空，如果为空返回0，不为空返回该题目图片数量和图片地址后半段
def multimodal_judgment(file_path , id):
    sheet_name = "benchmark"
    try:
        # 缓存各列的读取结果，避免重复调用
        col5_value = operate_excel.read_excel(file_path, sheet_name, id, 5)
        col4_value = operate_excel.read_excel(file_path, sheet_name, id, 4)
        col3_value = operate_excel.read_excel(file_path, sheet_name, id, 3)
        if type(col5_value) == float:  col5_value=""  #判断col5_value是nan还是字符串,读excel用的是pd中的DF格式，如果为空返回的是float样式的nan
        if type(col4_value) == float:  col4_value = ""
        if type(col3_value) == float:  col3_value = ""
        if  col5_value != '':
            #创建一个名为images的列表保存图片地址
            image = [col5_value , col4_value , col3_value]
            return 3 , image
        if col4_value != '':
            image = [col4_value , col3_value]
            return 2 , image
        if col3_value != '':
            image =  [col3_value]
            return 1 , image
        image = []
        return 0 , image
    except Exception as e:
        # 根据实际需求可以记录日志或重新抛出异常
        raise e

#异常日志记录
def save_judge_log(text):
    file_path = 'D:/study/PyCharm/WorkHouse/pycharmtest/test/file/answer_log.txt'
    file = open(file_path, 'a', encoding='utf-8')
    file.write(text)
    file.write('\n')
    file.close()
"""
#DeepSeek_V3.2_Exp回答记录
#标记现在正在执行的题目
question_id = 483
for i in range(5, 526):
    print(f"正在回答第{question_id}个题")
    operate_excel.write_excel("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark.xlsx", "DeepSeek_V3.2_Exp", question_id,
                              0, question_id) #保存题目编号
    #查看编号为id的
    num , image_s = multimodal_judgment("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark.xlsx",question_id)
    #判断是否为多模态，如果是则跳过
    if num == 0:
        question_text = operate_excel.read_excel("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark.xlsx", "benchmark", question_id, 1)#获取题目文本
        model_text = model.deepseek_chat(question_text)
        operate_excel.write_excel("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark.xlsx", "DeepSeek_V3.2_Exp", question_id,
                                  1, model_text) #保存模型回答
        question_id = question_id + 1
    else:
        #print(f"第{question_id}题是多模态试题，故跳过")
        question_id = question_id + 1
print("DeepSeek_V3.2_Exp模型的回答结束")
"""
"""
#DeepSeek_V3.2_Exp推理版回答记录
#question_id=现在正在执行的题目
for question_id in range(5, 526):
    print(f"正在回答第{question_id}个题")
    operate_excel.write_excel("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark.xlsx", "DeepSeek_V3.2_Exp_reasoner", question_id,
                              0, question_id) #保存题目编号
    #查看编号为id的
    num , image_s = multimodal_judgment("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark.xlsx",question_id)
    #判断是否为多模态，如果是则跳过
    if num == 0:
        question_text = operate_excel.read_excel("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark.xlsx", "benchmark", question_id, 1)#获取题目文本
        model_reason_text , model_text = model.deepseek_reasoner(question_text)
        operate_excel.write_excel("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark.xlsx",
                                  "DeepSeek_V3.2_Exp_reasoner", question_id,
                                  1, model_reason_text)  # 保存模型回答
        operate_excel.write_excel("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark.xlsx", "DeepSeek_V3.2_Exp_reasoner", question_id,
                                  2, model_text) #保存模型回答
        question_id = question_id + 1
    else:
        #print(f"第{question_id}题是多模态试题，故跳过")
print("DeepSeek_V3.2_Exp推理版模型的回答结束")
"""

#doubao-seed-1-6-thinking-250715回答线程
def dou_bao_seed_1_6_thinking_250715_thread():
    #标记现在正在执行的题目
    for question_id in range(438, 526):
        try:
            print(f"dou_bao_seed_1_6_thinking_250715模型正在回答第{question_id}个题")
            operate_excel.write_excel("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark.xlsx",
                                      "dou_bao_seed_1_6_thinking_25071", question_id,
                                      0, question_id) #保存题目编号
            # 查看编号为id的试题图片和文本
            num, image_s = multimodal_judgment("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark.xlsx",question_id)
            #给image_s列表里面的字符串全部加上"C:/Users/19029/Desktop/explainBenchmark/image"
            image_s = image_address_real(image_s)
            question_text = operate_excel.read_excel("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark.xlsx",
                                                     "benchmark", question_id, 1)#获取题目文本
            model_reason_text , model_text = model.dou_bao_seed_1_6_thinking_250715(question_text , image_s)
            operate_excel.write_excel("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark.xlsx",
                                      "dou_bao_seed_1_6_thinking_25071", question_id,
                                      1, model_reason_text)  # 保存模型回答
            operate_excel.write_excel("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark.xlsx",
                                      "dou_bao_seed_1_6_thinking_25071", question_id,
                                      2, model_text) #保存模型回答
            print(f"dou_bao_seed_1_6_thinking_250715模型对第{question_id}个题回答完毕")
        except Exception as e:
            print(f"dou_bao_seed_1_6_thinking_250715模型执行第{question_id}题时，捕获到异常: {type(e).__name__}: {e}")
            continue
    print("###################doubao-seed-1-6-thinking-250715线程结束")

#qwen3_max大模型线程
def qwen3_max_thread():
    #question_id=现在正在执行的题目
    for question_id in range(342, 526):
        try:
            print(f"qwen3_max正在回答第{question_id}个题")
            operate_excel.write_excel("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_qwen3_max.xlsx",
                                      "qwen3_max", question_id,
                                      0, question_id) #保存题目编号
            # 查看编号为id的试题图片和文本
            num, image_s = multimodal_judgment("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_qwen3_max.xlsx",question_id)
            #给image_s列表里面的字符串全部加上"C:/Users/19029/Desktop/explainBenchmark/image"
            image_s = image_address_real(image_s)
            question_text = operate_excel.read_excel("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_qwen3_max.xlsx",
                                                     "benchmark", question_id, 1)#获取题目文本
            model_text = model.qwen3_max(question_text , image_s)
            operate_excel.write_excel("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_qwen3_max.xlsx",
                                      "qwen3_max", question_id,
                                      1, model_text) #保存模型回答
            print(f"qwen3_max对第{question_id}个题回答完毕")
        except Exception as e:
            print(f"qwen3_max模型执行第{question_id}题时，捕获到异常: {type(e).__name__}: {e}")
            continue
    print("###################qwen3_max_thread线程结束")

#qwen3-next-80b-a3b-thinking大模型开启线程
def qwen3_next_80b_a3b_thinking_thread():
    #question_id=现在正在执行的题目
    for question_id in range(233, 526):
        try:
            print(f"qwen3_next_80b_a3b_thinking正在回答第{question_id}个题")
            operate_excel.write_excel("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_qwen3_next_80b_a3b_thinking.xlsx",
                                      "qwen3_next_80b_a3b_thinking", question_id,
                                      0, question_id) #保存题目编号
            # 查看编号为id的试题图片和文本
            num, image_s = multimodal_judgment("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_qwen3_next_80b_a3b_thinking.xlsx",question_id)
            #给image_s列表里面的字符串全部加上"C:/Users/19029/Desktop/explainBenchmark/image"
            image_s = image_address_real(image_s)
            question_text = operate_excel.read_excel("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_qwen3_next_80b_a3b_thinking.xlsx",
                                                     "benchmark", question_id, 1)#获取题目文本
            model_reason_text , model_text = model.qwen3_next_80b_a3b_thinking(question_text , image_s)
            operate_excel.write_excel("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_qwen3_next_80b_a3b_thinking.xlsx",
                                      "qwen3_next_80b_a3b_thinking", question_id,
                                      1, model_reason_text)  # 保存模型回答
            operate_excel.write_excel("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_qwen3_next_80b_a3b_thinking.xlsx",
                                      "qwen3_next_80b_a3b_thinking", question_id,
                                      2, model_text) #保存模型回答
            print(f"qwen3_next_80b_a3b_thinking对第{question_id}个题回答完毕")
        except Exception as e:
            print(f"qwen3_next_80b_a3b_thinking模型执行第{question_id}题时，捕获到异常: {type(e).__name__}: {e}")
            continue
    print("###################qwen3_next_80b_a3b_thinking_thread线程结束")

#glm_4.6大模型开启线程
def glm_4_6_thread():
    # question_id=现在正在执行的题目
    for question_id in range(75, 526):
        try:
            print(f"正在回答第{question_id}个题")
            operate_excel.write_excel("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_glm_4_6.xlsx",
                                      "glm_4_6", question_id,
                                      0, question_id)  # 保存题目编号
            # 查看编号为id的
            num, image_s = multimodal_judgment("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_glm_4_6.xlsx", question_id)
            # 判断是否为多模态，如果是则跳过
            if num == 0:
                question_text = operate_excel.read_excel("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_glm_4_6.xlsx",
                                                         "benchmark", question_id, 1)  # 获取题目文本
                model_reason_text, model_text = model.glm_4_6(question_text)
                operate_excel.write_excel("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_glm_4_6.xlsx",
                                          "glm_4_6", question_id,
                                          1, model_reason_text)  # 保存模型回答
                operate_excel.write_excel("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_glm_4_6.xlsx",
                                          "glm_4_6", question_id,
                                          2, model_text)  # 保存模型回答
                print(f"glm_4_6模型对第{question_id}个题回答完毕")
            else:
                print(f"第{question_id}题是多模态试题，故跳过")
        except Exception as e:
            print(f"glm_4_6模型执行第{question_id}题时，捕获到异常: {type(e).__name__}: {e}")
            continue
    print("###################glm_4_6_thread线程结束")

#glm-4.5v大模型开启线程
def glm_4_5v_thread():
    # question_id=现在正在执行的题目
    for question_id in range(3, 526):
        try:
            print(f"glm-4.5v正在回答第{question_id}个题")
            operate_excel.write_excel(
                "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_glm_4_5v.xlsx",
                "glm_4_5v", question_id,
                0, question_id)  # 保存题目编号
            # 查看编号为id的试题图片和文本
            num, image_s = multimodal_judgment(
                "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_glm_4_5v.xlsx",
                question_id)
            # 给image_s列表里面的字符串全部加上"C:/Users/19029/Desktop/explainBenchmark/image"
            image_s = image_address_real(image_s)
            question_text = operate_excel.read_excel(
                "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_glm_4_5v.xlsx",
                "benchmark", question_id, 1)  # 获取题目文本
            model_reason_text, model_text = model.glm_4_5v(question_text, image_s)
            operate_excel.write_excel(
                "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_glm_4_5v.xlsx",
                "glm_4_5v", question_id,
                1, model_reason_text)  # 保存模型回答
            operate_excel.write_excel(
                "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_glm_4_5v.xlsx",
                "glm_4_5v", question_id,
                2, model_text)  # 保存模型回答
            print(f"glm-4.5v对第{question_id}个题回答完毕")
        except Exception as e:
            print(f"glm-4.5v模型执行第{question_id}题时，捕获到异常: {type(e).__name__}: {e}")
            continue
    print("###################glm-4.5v线程结束")

#ernie-x1.1-preview大模型开启线程
def ernie_x_1_1_preview_thread():
    # question_id=现在正在执行的题目
    for question_id in range(3, 5):
        try:
            print(f"ernie-x1.1-preview大模型正在回答第{question_id}个题")
            operate_excel.write_excel("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_ernie_x_1_1_preview.xlsx",
                                      "ernie_x_1_1_preview", question_id,
                                      0, question_id)  # 保存题目编号
            # 查看编号为id的
            num, image_s = multimodal_judgment("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_ernie_x_1_1_preview.xlsx",
                                               question_id)
            # 判断是否为多模态，如果是则跳过
            if num == 0:
                question_text = operate_excel.read_excel(
                    "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_ernie_x_1_1_preview.xlsx",
                    "benchmark", question_id, 1)  # 获取题目文本
                model_reason_text, model_text = model.ernie_x_1_1_preview(question_text)
                operate_excel.write_excel("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_ernie_x_1_1_preview.xlsx",
                                          "ernie_x_1_1_preview", question_id,
                                          1, model_reason_text)  # 保存模型回答
                operate_excel.write_excel("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_ernie_x_1_1_preview.xlsx",
                                          "ernie_x_1_1_preview", question_id,
                                          2, model_text)  # 保存模型回答
                print(f"ernie-x1.1-preview大模型对第{question_id}个题回答完毕")
            else:
                print(f"第{question_id}题是多模态试题，故跳过")
        except Exception as e:
            print(f"ernie-x1.1-preview大模型执行第{question_id}题时，捕获到异常: {type(e).__name__}: {e}")
            continue
    print("###################ernie_x_1_1_preview_thread线程结束")

#gpt-5_high大模型开启线程
def gpt_5_high_thread():
    # question_id=现在正在执行的题目
    file_path = "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_gpt_5_high.xlsx"
    for question_id in range(23,526):
        try:
            print(f"gpt_5_high正在回答第{question_id}个题")
            operate_excel.write_excel(file_path,"gpt_5_high", question_id,0, question_id)  # 保存题目编号
            # 查看编号为id的试题图片和文本
            num, image_s = multimodal_judgment(file_path,question_id)
            # 给image_s列表里面的字符串全部加上"C:/Users/19029/Desktop/explainBenchmark/image"
            image_s = image_address_real(image_s)
            question_text = operate_excel.read_excel(file_path,"benchmark", question_id, 1)  # 获取题目文本
            model_text = model.gpt_5_high(question_text, image_s)
            operate_excel.write_excel(file_path,"gpt_5_high", question_id,1, model_text)  # 保存模型回答
            print(f"gpt_5_high对第{question_id}个题回答完毕")
        except Exception as e:
            print(f"gpt_5_high模型执行第{question_id}题时，捕获到异常: {type(e).__name__}: {e}")
            save_judge_log(f"gpt_5_high模型执行第{question_id}题时，捕获到异常: {type(e).__name__}: {e}")
            continue
    print("###################gpt_5_high线程结束")

#o4_mini_high大模型开启线程
def o4_mini_high_thread():
    # question_id=现在正在执行的题目
    file_path = "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_o4_mini_high.xlsx"
    for question_id in range(100,101):
        try:
            print(f"o4_mini_high正在回答第{question_id}个题")
            operate_excel.write_excel(file_path,"o4_mini_high", question_id,0, question_id)  # 保存题目编号
            # 查看编号为id的试题图片和文本
            num, image_s = multimodal_judgment(file_path,question_id)
            # 给image_s列表里面的字符串全部加上"C:/Users/19029/Desktop/explainBenchmark/image"
            image_s = image_address_real(image_s)
            question_text = operate_excel.read_excel(file_path,"benchmark", question_id, 1)  # 获取题目文本
            model_text = model.o4_mini_high(question_text, image_s)
            operate_excel.write_excel(file_path,"o4_mini_high", question_id,1, model_text)  # 保存模型回答
            print(f"o4_mini_high对第{question_id}个题回答完毕")
        except Exception as e:
            print(f"o4_mini_high模型执行第{question_id}题时，捕获到异常: {type(e).__name__}: {e}")
            save_judge_log(f"o4_mini_high模型执行第{question_id}题时，捕获到异常: {type(e).__name__}: {e}")
            continue
    print("###################o4_mini_high线程结束")

#claude_sonnet_4_5_thinking大模型开启线程
def claude_sonnet_4_5_thinking_thread():
    # question_id=现在正在执行的题目
    file_path = "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_claude_sonnet_4_5_thinking.xlsx"
    for question_id in range(117,120):
        try:
            print(f"claude_sonnet_4_5_thinking正在回答第{question_id}个题")
            operate_excel.write_excel(file_path,"claude_sonnet_4_5_thinking", question_id,0, question_id)  # 保存题目编号
            # 查看编号为id的试题图片和文本
            num, image_s = multimodal_judgment(file_path,question_id)
            # 给image_s列表里面的字符串全部加上"C:/Users/19029/Desktop/explainBenchmark/image"
            image_s = image_address_real(image_s)
            question_text = operate_excel.read_excel(file_path,"benchmark", question_id, 1)  # 获取题目文本
            model_thinking_text, model_text = model.claude_sonnet_4_5_thinking(question_text, image_s)
            operate_excel.write_excel(file_path, "claude_sonnet_4_5_thinking", question_id, 1, model_thinking_text)  # 保存模型回答
            operate_excel.write_excel(file_path,"claude_sonnet_4_5_thinking", question_id,2, model_text)  # 保存模型回答
            print(f"claude_sonnet_4_5_thinking对第{question_id}个题回答完毕")
        except Exception as e:
            print(f"claude_sonnet_4_5_thinking模型执行第{question_id}题时，捕获到异常: {type(e).__name__}: {e}")
            save_judge_log(f"claude_sonnet_4_5_thinking模型执行第{question_id}题时，捕获到异常: {type(e).__name__}: {e}")
            continue
    print("###################claude_sonnet_4_5_thinking线程结束")

#gemini_2_5_pro大模型开启线程
def gemini_2_5_pro_thread():
    # question_id=现在正在执行的题目
    file_path = "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_gemini_2_5_pro_1.xlsx"
    for question_id in range(256,556):
        try:
            print(f"gemini_2_5_pro正在回答第{question_id}个题")
            operate_excel.write_excel(file_path,"gemini_2_5_pro", question_id,0, question_id)  # 保存题目编号
            # 查看编号为id的试题图片和文本
            num, image_s = multimodal_judgment(file_path,question_id)
            # 给image_s列表里面的字符串全部加上"C:/Users/19029/Desktop/explainBenchmark/image"
            image_s = image_address_real(image_s)
            question_text = operate_excel.read_excel(file_path,"benchmark", question_id, 1)  # 获取题目文本
            model_text = model.gemini_2_5_pro(question_text, image_s)
            operate_excel.write_excel(file_path,"gemini_2_5_pro", question_id,1, model_text)  # 保存模型回答
            print(f"gemini_2_5_pro对第{question_id}个题回答完毕")
        except Exception as e:
            print(f"gemini_2_5_pro模型执行第{question_id}题时，捕获到异常: {type(e).__name__}: {e}")
            save_judge_log(f"gemini_2_5_pro模型执行第{question_id}题时，捕获到异常: {type(e).__name__}: {e}")
            continue
    print("###################gemini_2_5_pro线程结束")



#下面是main函数
if __name__ == '__main__':
    try:
        #thread1 = Thread(target = gpt_5_high_thread)
        #thread2 = Thread(target = o4_mini_high_thread)
        #thread3 = Thread(target = claude_sonnet_4_5_thinking_thread)
        thread4 = Thread(target = gemini_2_5_pro_thread)

        #thread1.start()
        #thread2.start()
        #thread3.start()
        thread4.start()

        #thread1.join()
        #thread2.join()
        #thread3.join()
        thread4.join()


    except Exception as e:
        # 捕获所有常规异常
        #print(f"捕获到异常: {type(e).__name__}: {e}")
        tool.send_email("1902900584@qq.com", "异常中断提醒", "邮件的内容")
    finally:
        tool.send_email("1902900584@qq.com", "正常运行结束提醒", "邮件的内容")
