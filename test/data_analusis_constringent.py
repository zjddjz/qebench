from bdb import effective

import operate_excel
import tool


def save_concise(model_name, a, b, c,d,e):
    with open('D:/study/PyCharm/WorkHouse/pycharmtest/test/file/concise.txt', 'a', encoding='utf-8') as f:
        f.write(f"这是{model_name}模型的简洁性得分")
        f.write('\n')
        f.write(str(a))
        f.write('\n')
        f.write(str(b))
        f.write('\n')
        f.write(str(c))
        f.write('\n')
        f.write(str(d))
        f.write('\n')
        f.write(str(e))
        f.write('\n')

def save_constringent(model_name, a, b, c, d, e):
    with open('D:/study/PyCharm/WorkHouse/pycharmtest/test/file/constringent.txt', 'a', encoding='utf-8') as f:
        f.write(f"这是{model_name}模型的敛合性得分")
        f.write('\n')
        f.write(str(a))
        f.write('\n')
        f.write(str(b))
        f.write('\n')
        f.write(str(c))
        f.write('\n')
        f.write(str(d))
        f.write('\n')
        f.write(str(e))
        f.write('\n')

def calculate_concise(model_name,file_path,sheet_name,column_x,column_y,column_effective):
    b_1 = []
    c_1 = []
    d_1 = []
    e_1 = []
    b_2 = []
    c_2 = []
    d_2 = []
    e_2 = []
    for question_id in range(1,526):
        x = operate_excel.read_excel(file_path, sheet_name, question_id, column_x)
        #如果x不为空且不等于0
        if type(x) != float and x != 0:
            y = operate_excel.read_excel(file_path, sheet_name, question_id, column_y)
            effective = eval(operate_excel.read_excel(file_path, sheet_name, question_id, column_effective))
            distinct_effective = list(set(effective))
            num = operate_excel.read_excel(file_path, "benchmark", question_id, 7)
            concise = y/x
            s = len(distinct_effective)/num
            constringent = s + concise -1
            # 如果question_id的范围在1到200
            if 1 <= question_id <= 200:
                b_1.append(concise)
                b_2.append(constringent)
            elif 201 <= question_id <= 400:
                c_1.append(concise)
                c_2.append(constringent)
            elif 401 <= question_id <= 500:
                d_1.append(concise)
                d_2.append(constringent)
            else:
                e_1.append(concise)
                e_2.append(constringent)
    a_1 = b_1+c_1+d_1+e_1
    a_2 = b_2+c_2+d_2+e_2
    save_concise(model_name, a_1, b_1, c_1, d_1, e_1)
    save_constringent(model_name, a_2, b_2, c_2, d_2, e_2)


if __name__ == '__main__':
    try:
        calculate_concise("DeepSeek_V3.2_Exp",
                          "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark.xlsx",
                          "DeepSeek_V3.2_Exp", 2, 3, 4)
        calculate_concise("DeepSeek_V3.2_Exp_reasoner",
                          "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_DeepSeek_V3.2_Exp_reasoner.xlsx",
                          "DeepSeek_V3.2_Exp_reasoner", 3, 4, 5)
        calculate_concise("dou_bao_seed_1_6_thinking_25071",
                          "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_dou_bao_seed_1_6_thinking_25071.xlsx",
                          "dou_bao_seed_1_6_thinking_25071", 3, 4, 5)
        calculate_concise("glm_4_5v",
                          "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_glm_4_5v.xlsx",
                          "glm_4_5v", 3, 4, 5)
        calculate_concise("glm_4_6",
                          "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_glm_4_6.xlsx",
                          "glm_4_6", 3, 4, 5)
        calculate_concise("qwen3_max",
                          "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_qwen3_max.xlsx",
                          "qwen3_max", 2, 3, 4)
        calculate_concise("qwen3_next_80b_a3b_thinking",
                          "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_qwen3_next_80b_a3b_thinking.xlsx",
                          "qwen3_next_80b_a3b_thinking", 3, 4, 5)
        calculate_concise("gpt_5_high",
                          "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_gpt_5_high.xlsx",
                          "gpt_5_high", 2, 3, 4)
        calculate_concise("o4_mini_high",
                          "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_o4_mini_high.xlsx",
                          "o4_mini_high", 2, 3, 4)
        calculate_concise("claude_sonnet_4_5_thinking",
                          "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_claude_sonnet_4_5_thinking.xlsx",
                          "claude_sonnet_4_5_thinking", 3, 4, 5)
        calculate_concise("gemini_2_5_pro",
                          "C:/Users/19029/Desktop/explainBenchmark/explainBenchmark_gemini_2_5_pro.xlsx",
                          "gemini_2_5_pro", 2, 3, 4)



    except Exception as e:
        # 捕获所有常规异常
        #print(f"捕获到异常: {type(e).__name__}: {e}")
        tool.send_email("1902900584@qq.com", "异常中断提醒", "邮件的内容")
    finally:
        tool.send_email("1902900584@qq.com", "正常运行结束提醒", "邮件的内容")