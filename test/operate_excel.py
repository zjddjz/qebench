import os
import pandas as pd
from aiohttp.hdrs import CONTENT_TYPE
import model

# 读取 Excel文件中sheet_name表第row行第column列
def read_excel(file_path, sheet_name, row, column):
    # 参数验证
    if not isinstance(row, int) or not isinstance(column, int):
        raise TypeError("row和column必须是整数")
    if row < 0 or column < 0:
        raise ValueError("row和column必须是非负整数")
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
        # 边界检查
        if row >= len(df) or column >= len(df.columns):
            raise IndexError(f"索引超出范围: 请求的位置({row}, {column})超出了数据范围({len(df)}, {len(df.columns)})")
        content = df.iloc[row, column]
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"文件未找到: {file_path}")
    except PermissionError:
        raise PermissionError(f"没有权限访问文件: {file_path}")
    except Exception as e:
        raise Exception(f"读取Excel文件时发生错误: {str(e)}")


# 往excel文件中sheet_name表第row行第column列写content)
def write_excel(file_path, sheet_name, row, column, content):
    # 参数验证
    if not isinstance(file_path, str) or not file_path:
        raise ValueError("file_path 不能为空")
    if not isinstance(sheet_name, str) or not sheet_name:
        raise ValueError("sheet_name 不能为空")
    if not isinstance(row, int) or row < 0:
        raise ValueError("row必须是整数")
    if not isinstance(column, int) or column < 0:
        raise ValueError("column必须是整数")
    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件 {file_path} 不存在")
    try:
        # 读取Excel文件
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
        # 扩展DataFrame以适应新的行列索引
        while len(df) <= row:
            df.loc[len(df)] = [None] * len(df.columns) if len(df.columns) > 0 else [None]
        while len(df.columns) <= column:
            df[len(df.columns)] = None
        # 写入内容
        df.iloc[row, column] = content
        # 保存回原文件
        with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
    except Exception as e:
        raise Exception(f"Error writing to Excel file: {str(e)}")
#测试答案
"""
这是glm的回答

在M煤矿采空区建设地下水库具有多方面的重要意义：  
1. **水资源储存与调控**：该地区属温带大陆性季风气候，降水季节分配不均，地下水库可储存丰水期降水及地下水，调节水资源的时空分布，缓解干旱区水资源短缺问题。  
2. **水质净化与保护**：尽管采空区水体含地表污染物，但地下环境可通过地层过滤、吸附等作用自然净化水质，建设水库后可通过人工干预（如沉淀、生物降解）进一步提升水质，为安全用水提供保障。  
3. **地质环境稳定**：采空区易引发地面沉降、塌陷等地质灾害，蓄水后水体压力可支撑上层岩层，减少地层变形，降低安全隐患。  
4. **生态与经济价值**：稳定的地下水库可为周边农业灌溉、工业生产及居民生活提供可靠水源，促进区域可持续发展；同时，改善局部水文条件，维护生态系统平衡。  

综上，建设地下水库实现了水资源的合理利用、环境保护与灾害防治的多重目标，符合干旱区可持续发展的需求。  

本题的答案是  
<|begin_of_box|>在M煤矿采空区建设地下水库，可储存调节水资源以缓解短缺，通过地层净化改善水质，支撑地层结构防止沉降，并为生产生活提供稳定水源，实现资源利用与环境保护的双重效益。<|end_of_box|>
这是deepseek的回答
{"X": 4, "Y": 3, "effective": [2, 3, 1]}

进程已结束，退出代码为 0
"""

