import operate_excel
import pandas as pd
import tool


#模型应该回答却没有回答的题目，输出题目编号(题目类型type，0代表只能接收文字输入的模型、1代表可以接收文字+图片的模型)
def calculate_missing_question(question_type,file_path,sheet_name,column):
    question_id_list = [] #记录拒绝回答的题目编号
    if question_type == 0:
        for question_id in range(1,526):
            question_image_1_address = operate_excel.read_excel(file_path, "benchmark", question_id, 3)
            model_text= operate_excel.read_excel(file_path, sheet_name, question_id, column)
            if type(question_image_1_address) == float and type(model_text) == float:
                question_id_list.append(question_id)
    else:
        for question_id in range(1,526):
            model_text = operate_excel.read_excel(file_path, sheet_name, question_id, column)
            if type(model_text) == float:
                question_id_list.append(question_id)
    return question_id_list

#模型应该回答却没有回答的题目，x、y、effective置为0、0、"[]"
def save_null(question_id_list, file_path, sheet_name,column_x, column_y, column_effective):
    if len(question_id_list) > 0:
        for question_id in question_id_list:
            operate_excel.write_excel(file_path, sheet_name, question_id, column_x, 0)
            operate_excel.write_excel(file_path, sheet_name, question_id, column_y, 0)
            operate_excel.write_excel(file_path, sheet_name, question_id, column_effective, "[]")

#剔除列表中的重复元素
def delete_repeat(list_v):
    list_v = list(set(list_v))
    return list_v

#计算每个题目的完整性得分，输入（excel路径、表单、effective列）
def calculate_completeness(file_path,sheet_name,column):
    geography_gao_kao_score_list = []#1-200 #存放整个模型回答的完整性得分，每个元素为该问题的完整性得分
    history_gao_kao_score_list = []#201-400
    history_postgraduate_score_list = []#401-500
    geography_postgraduate_score_list = [] #501-525
    for question_id in range(1,526):
        str_effective = operate_excel.read_excel(file_path, sheet_name, question_id, column)
        if type(str_effective) != float:  # 如果为空pandas读excel输出的就是float类型的nan
            effective = eval(str_effective)  # 转化为列表
            effective = delete_repeat(effective) #删除重复元素
            num = operate_excel.read_excel(file_path,"benchmark", question_id, 7)  # 答案中要点个数
            #如果question_id的范围在1到200
            if 1 <= question_id <= 200:
                geography_gao_kao_score_list.append(len(effective)/ num)
            elif 201 <= question_id <= 400:
                history_gao_kao_score_list.append(len(effective) / num)
            elif 401 <= question_id <= 500:
                history_postgraduate_score_list.append(len(effective) / num)
            else:
                geography_postgraduate_score_list.append(len(effective) / num)
    completeness_score_list = geography_gao_kao_score_list + history_gao_kao_score_list + history_postgraduate_score_list + geography_postgraduate_score_list
    return  completeness_score_list, geography_gao_kao_score_list , history_gao_kao_score_list, history_postgraduate_score_list, geography_postgraduate_score_list

def save_completeness(model_name,completeness_score_list,geography_gao_kao_score_list,history_gao_kao_score_list,history_postgraduate_score_list,geography_postgraduate_score_list):
    with open('D:/study/PyCharm/WorkHouse/pycharmtest/test/file/completeness.txt', 'a', encoding='utf-8') as f:
        f.write(f"这是{model_name}模型的完整性得分")
        f.write('\n')
        f.write(str(completeness_score_list))
        f.write('\n')
        f.write(str(geography_gao_kao_score_list))
        f.write('\n')
        f.write(str(history_gao_kao_score_list))
        f.write('\n')
        f.write(str(history_postgraduate_score_list))
        f.write('\n')
        f.write(str(geography_postgraduate_score_list))
        f.write('\n')

#计算列表的平均值和方差
def calculate_mean_variance(list_v):
    series = pd.Series(list_v)
    mean = series.mean()
    #计算标准差
    standard_deviation = series.std(ddof=0)
    return round(mean,3),round(standard_deviation,3)


if __name__ == '__main__':
    try:
        """
        #记录模型应该回答却没有回答的题目
        gpt_5_high = calculate_missing_question(0,"C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_gpt_5_high.xlsx","gpt_5_high",1)
        o4_mini_high = calculate_missing_question(0,
                                                "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_o4_mini_high.xlsx",
                                                "o4_mini_high", 1)
        claude_sonnet_4_5_thinking = calculate_missing_question(0,
                                                "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_claude_sonnet_4_5_thinking.xlsx",
                                                "claude_sonnet_4_5_thinking", 2)
        gemini_2_5_pro = calculate_missing_question(0,
                                                "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_gemini_2_5_pro.xlsx",
                                                "gemini_2_5_pro", 1)

        with open('D:/study/PyCharm/WorkHouse/pycharmtest/test/file/missing_question.txt', 'a', encoding='utf-8') as f:
            f.write("这是gpt_5_high未回答的题目")
            f.write('\n')
            f.write(str(gpt_5_high))
            f.write('\n')
            f.write("这是o4_mini_high未回答的题目")
            f.write('\n')
            f.write(str(o4_mini_high))
            f.write('\n')
            f.write("这是claude_sonnet_4_5_thinking未回答的题目")
            f.write('\n')
            f.write(str(claude_sonnet_4_5_thinking))
            f.write('\n')
            f.write("这是gemini_2_5_pro未回答的题目")
            f.write('\n')
            f.write(str(gemini_2_5_pro))
            f.write('\n')
        """

        """
        #将模型应该回答却没有回答的题目，x、y、effective置为0、0、"[]"
        with open('D:/study/PyCharm/WorkHouse/pycharmtest/test/file/missing_question.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        line_2 = lines[1]
        line_4 = lines[3]
        line_6 = lines[5]
        line_8 = lines[7]
        line_10 = lines[9]
        line_12 = lines[11]
        line_14 = lines[13]
        deepseek_chat = eval(line_2)
        deepseek_reason = eval(line_4)
        dou_bao = eval(line_6)
        glm_4v = eval(line_8)
        glm_4_6 = eval(line_10)
        qwen3_max = eval(line_12)
        qwen3_next_80b_a3b_thinking = eval(line_14)
        #遍历列表deepseek_chat中的元素
        save_null(deepseek_chat, "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark.xlsx", "DeepSeek_V3.2_Exp", 2, 3, 4)
        save_null(deepseek_reason, "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_DeepSeek_V3.2_Exp_reasoner.xlsx", "DeepSeek_V3.2_Exp_reasoner", 3, 4, 5)
        save_null(dou_bao, "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_dou_bao_seed_1_6_thinking_25071.xlsx", "dou_bao_seed_1_6_thinking_25071", 3, 4, 5)
        save_null(glm_4v, "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_glm_4_5v.xlsx", "glm_4_5v", 3, 4, 5)
        save_null(glm_4_6, "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_glm_4_6.xlsx", "glm_4_6", 3, 4, 5)
        save_null(qwen3_max, "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_qwen3_max.xlsx", "qwen3_max", 2, 3, 4)
        save_null(qwen3_next_80b_a3b_thinking, "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_qwen3_next_80b_a3b_thinking.xlsx", "qwen3_next_80b_a3b_thinking", 3, 4, 5)
        """


        #计算每个题目模型回答的完整性得分,并保存到file/completeness.txt中
        """
        completeness_score_list, geography_gao_kao_score_list, history_gao_kao_score_list, history_postgraduate_score_list, geography_postgraduate_score_list = (
            calculate_completeness("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_gpt_5_high.xlsx",
                                   "gpt_5_high",
                                   4))
        save_completeness("gpt_5_high",completeness_score_list, geography_gao_kao_score_list, history_gao_kao_score_list, history_postgraduate_score_list, geography_postgraduate_score_list)

        completeness_score_list, geography_gao_kao_score_list, history_gao_kao_score_list, history_postgraduate_score_list, geography_postgraduate_score_list = (
            calculate_completeness("C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_o4_mini_high.xlsx",
                                   "o4_mini_high",
                                   4))
        save_completeness("o4_mini_high", completeness_score_list, geography_gao_kao_score_list,
                          history_gao_kao_score_list, history_postgraduate_score_list, geography_postgraduate_score_list)
        
        completeness_score_list, geography_gao_kao_score_list, history_gao_kao_score_list, history_postgraduate_score_list, geography_postgraduate_score_list = (
            calculate_completeness(
                "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_claude_sonnet_4_5_thinking.xlsx",
                "claude_sonnet_4_5_thinking",
                5))
        save_completeness("claude_sonnet_4_5_thinking", completeness_score_list, geography_gao_kao_score_list,
                          history_gao_kao_score_list, history_postgraduate_score_list, geography_postgraduate_score_list)

        completeness_score_list, geography_gao_kao_score_list, history_gao_kao_score_list, history_postgraduate_score_list, geography_postgraduate_score_list = (
            calculate_completeness(
                "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_gemini_2_5_pro.xlsx",
                "gemini_2_5_pro",
                4))
        save_completeness("gemini_2_5_pro", completeness_score_list, geography_gao_kao_score_list,
                          history_gao_kao_score_list, history_postgraduate_score_list, geography_postgraduate_score_list)

        """


        #计算得分
        with open('D:/study/PyCharm/WorkHouse/pycharmtest/test/file/concise.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for i in [1,7,13,19,25,31,37,43,49,55,61]:
            list_1 = eval(lines[i])
            list_2 = eval(lines[i+1])
            list_3 = eval(lines[i+2])
            list_4 = eval(lines[i+3])
            list_5 = eval(lines[i+4])
            a1 ,b1= calculate_mean_variance(list_1)
            a2 ,b2= calculate_mean_variance(list_2)
            a3 ,b3= calculate_mean_variance(list_3)
            a4 ,b4= calculate_mean_variance(list_4)
            a5 ,b5= calculate_mean_variance(list_5)
            print(f"均值为{a1}，方差为{b1}")
            print(f"均值为{a2}，方差为{b2}")
            print(f"均值为{a3}，方差为{b3}")
            print(f"均值为{a4}，方差为{b4}")
            print(f"均值为{a5}，方差为{b5}")
            print("@@@@@@@@@@@@@@@@@@@@@@@@@")




    except Exception as e:
        tool.send_email("1902900584@qq.com", "异常中断提醒", "邮件的内容")
    finally:
        tool.send_email("1902900584@qq.com", "正常运行结束提醒", "邮件的内容")