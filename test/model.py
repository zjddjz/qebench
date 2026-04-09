from anthropic import Anthropic
from openai import OpenAI
from zai import ZhipuAiClient
import base64
import requests
import json
from google import genai
from google.genai import types
# 转化为base64
def base64_image(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

#访问api_key
def get_api_key(model_name):
    with open('file/api_key.txt', 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith(model_name+'_api_key:'):
                # 提取冒号后的值并去除空白字符
                return line.split(':', 1)[1].strip()
    return None  # 如果没找到返回None

#使用DeepSeek_V3.2_Exp模型(输入：拼装好的提示词：输出：按照提示词输出)
def deepseek_chat(text):
    from openai import OpenAI
    client = OpenAI(api_key = get_api_key("deepseek"), base_url = "https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": text},
        ],
        stream=False
    )
    return  response.choices[0].message.content

#使用DeepSeek_V3.2_Exp推理版模型(输入：拼装好的提示词：输出：按照提示词输出)
def deepseek_reasoner(text):
    from openai import OpenAI
    client = OpenAI(api_key = get_api_key("deepseek"), base_url = "https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=[
            {"role": "user", "content": text},
        ],
        stream=False
    )
    return  response.choices[0].message.reasoning_content , response.choices[0].message.content

#使用dou_bao-seed-1-6-thinking-250715模型(输入：拼装好的提示词;图片列表；输出：按照提示词输出)
def dou_bao_seed_1_6_thinking_250715(text, image_url_list):
    message = []
    #输入message中的图片个数
    if len(image_url_list) == 0:
        message = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text}
                ]
            }
        ]
    elif len(image_url_list) == 1:
        # 需注意：传入Base64编码前需增加前缀 data:image/{图片格式};base64,{Base64编码}：
        # PNG图片："url":  f"data:image/png;base64,{base64_image}"
        # JPEG图片："url":  f"data:image/jpeg;base64,{base64_image}"
        # WEBP图片："url":  f"data:image/webp;base64,{base64_image}"
        message = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url":  f"data:image/png;base64,{base64_image(image_url_list[0])}"
                        },
                    },
                    {"type": "text", "text": text}
                ]
            }
        ]
    elif len(image_url_list) == 2:
        message = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url":  f"data:image/png;base64,{base64_image(image_url_list[0])}"
                        }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url":  f"data:image/png;base64,{base64_image(image_url_list[1])}"
                        },
                    },
                    {"type": "text", "text": text}
                ]
            }
        ]
    elif len(image_url_list) == 3:
        message = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url":  f"data:image/png;base64,{base64_image(image_url_list[0])}"
                        }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url":  f"data:image/png;base64,{base64_image(image_url_list[1])}"
                        }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url":  f"data:image/png;base64,{base64_image(image_url_list[2])}"
                        }
                    },
                    {"type": "text", "text": text}
                ]
            }
        ]

    client = OpenAI(
        # Make sure the environment variable "ARK_API_KEY" has been set.
        api_key=get_api_key("doubao"),
        # The base URL for model invocation .
        base_url="https://ark.cn-beijing.volces.com/api/v3",
    )
    completion = client.chat.completions.create(
        # Get Model ID: https://www.volcengine.com/docs/82379/1330310 .
        model="doubao-seed-1-6-thinking-250715",
        messages = message,
    )
    return completion.choices[0].message.reasoning_content , completion.choices[0].message.content

#qwen3_max大模型
def qwen3_max(text, image_url_list):
    message = []
    # 输入message中的图片个数
    if len(image_url_list) == 0:
        message = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text}
                ]
            }
        ]
    elif len(image_url_list) == 1:
        # 需注意：传入Base64编码前需增加前缀 data:image/{图片格式};base64,{Base64编码}：
        # PNG图片："url":  f"data:image/png;base64,{base64_image}"
        # JPEG图片："url":  f"data:image/jpeg;base64,{base64_image}"
        # WEBP图片："url":  f"data:image/webp;base64,{base64_image}"
        message = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image(image_url_list[0])}"
                        },
                    },
                    {"type": "text", "text": text}
                ]
            }
        ]
    elif len(image_url_list) == 2:
        message = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image(image_url_list[0])}"
                        }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image(image_url_list[1])}"
                        },
                    },
                    {"type": "text", "text": text}
                ]
            }
        ]
    elif len(image_url_list) == 3:
        message = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image(image_url_list[0])}"
                        }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image(image_url_list[1])}"
                        }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image(image_url_list[2])}"
                        }
                    },
                    {"type": "text", "text": text}
                ]
            }
        ]
    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=get_api_key("qwen"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        #qwen3-max、qwen3-next-80b-a3b-thinking
        model="qwen3-max",  # 此处以qwen-vl-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=message ,
        # 由于 enable_thinking 非 OpenAI 标准参数，需要通过 extra_body 传入
        #extra_body={"enable_thinking": True},
        )
    return completion.choices[0].message.content

#qwen3_max大模型
def qwen3_next_80b_a3b_thinking(text, image_url_list):
    message = []
    # 输入message中的图片个数
    if len(image_url_list) == 0:
        message = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text}
                ]
            }
        ]
    elif len(image_url_list) == 1:
        # 需注意：传入Base64编码前需增加前缀 data:image/{图片格式};base64,{Base64编码}：
        # PNG图片："url":  f"data:image/png;base64,{base64_image}"
        # JPEG图片："url":  f"data:image/jpeg;base64,{base64_image}"
        # WEBP图片："url":  f"data:image/webp;base64,{base64_image}"
        message = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image(image_url_list[0])}"
                        },
                    },
                    {"type": "text", "text": text}
                ]
            }
        ]
    elif len(image_url_list) == 2:
        message = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image(image_url_list[0])}"
                        }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image(image_url_list[1])}"
                        },
                    },
                    {"type": "text", "text": text}
                ]
            }
        ]
    elif len(image_url_list) == 3:
        message = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image(image_url_list[0])}"
                        }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image(image_url_list[1])}"
                        }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image(image_url_list[2])}"
                        }
                    },
                    {"type": "text", "text": text}
                ]
            }
        ]
    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=get_api_key("qwen"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        #qwen3-max、qwen3-next-80b-a3b-thinking
        model="qwen3-next-80b-a3b-thinking",  # 此处以qwen-vl-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=message ,
        # 由于 enable_thinking 非 OpenAI 标准参数，需要通过 extra_body 传入
        #extra_body={"enable_thinking": True},
        )
    return completion.choices[0].message.reasoning_content, completion.choices[0].message.content

#glm_4_6大模型
def glm_4_6(text):
    client = ZhipuAiClient(api_key=get_api_key("glm"))

    response = client.chat.completions.create(
        model="glm-4.6",
        messages=[
            {"role": "user", "content": text}
        ],
        thinking={
            "type": "enabled",  # 启用深度思考模式
        },
        max_tokens=65536,  # 最大输出 tokens
        temperature=1.0  # 控制输出的随机性
    )
    return response.choices[0].message.reasoning_content, response.choices[0].message.content

#glm_4_5v大模型
def glm_4_5v(text,image_url_list):
    message = []
    # 输入message中的图片个数
    if len(image_url_list) == 0:
        message = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text}
                ]
            }
        ]
    elif len(image_url_list) == 1:
        # 需注意：传入Base64编码前需增加前缀 data:image/{图片格式};base64,{Base64编码}：
        # PNG图片："url":  f"data:image/png;base64,{base64_image}"
        # JPEG图片："url":  f"data:image/jpeg;base64,{base64_image}"
        # WEBP图片："url":  f"data:image/webp;base64,{base64_image}"
        message = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image(image_url_list[0])}"
                        },
                    },
                    {"type": "text", "text": text}
                ]
            }
        ]
    elif len(image_url_list) == 2:
        message = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image(image_url_list[0])}"
                        }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image(image_url_list[1])}"
                        },
                    },
                    {"type": "text", "text": text}
                ]
            }
        ]
    elif len(image_url_list) == 3:
        message = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image(image_url_list[0])}"
                        }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image(image_url_list[1])}"
                        }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image(image_url_list[2])}"
                        }
                    },
                    {"type": "text", "text": text}
                ]
            }
        ]
    client = ZhipuAiClient(api_key=get_api_key("glm"))
    response = client.chat.completions.create(
        model="glm-4.5v",  # 填写需要调用的模型名称
        messages=message,
        thinking={
            "type": "enabled"
        }
    )
    return response.choices[0].message.reasoning_content, response.choices[0].message.content


#ERNIE X1.1-Preview大模型
def ernie_x_1_1_preview(text):
    url = "https://qianfan.baidubce.com/v2/chat/completions"

    payload = json.dumps({
        "model": "ernie-x1.1-preview",
        #"model": "deepseek-v3.1-250821",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": text
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer bce-v3/ALTAK-aX7GJgJvWAwFBnADdWAxk/a0112628f1f28eecc7abb5a99e7496aecb466e3f'#Bearer+key
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    # 将响应的JSON字符串转换为json格式
    response_json = response.json()
    print(type(response_json))
    print(response_json['choices'][0]['message']['content'])
    #print(response_json['choices'][0]['message']['reasoning_content'])
    #return response_json['choices'][0]['message']['reasoning_content'], response_json['choices'][0]['message']['content']

def gpt_5_high(text ,image_url_list):
    input = []
    # 输入message中的图片个数
    if len(image_url_list) == 0:
        input = [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": text},
                ]
            }
        ]
    elif len(image_url_list) == 1:
        # 需注意：传入Base64编码前需增加前缀 data:image/{图片格式};base64,{Base64编码}：
        # PNG图片："url":  f"data:image/png;base64,{base64_image}"
        # JPEG图片："url":  f"data:image/jpeg;base64,{base64_image}"
        # WEBP图片："url":  f"data:image/webp;base64,{base64_image}"
        input = [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": text},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{base64_image(image_url_list[0])}",
                    },
                ]
            }
        ]
    elif len(image_url_list) == 2:
        input = [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": text},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{base64_image(image_url_list[0])}",
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{base64_image(image_url_list[1])}",
                    },
                ]
            }
        ]
    elif len(image_url_list) == 3:
        input = [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": text},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{base64_image(image_url_list[0])}",
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{base64_image(image_url_list[1])}",
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{base64_image(image_url_list[2])}",
                    },
                ]
            }
        ]
    client = OpenAI(api_key = get_api_key("aihub"), base_url="https://aihubmix.com/v1")
    response = client.responses.create(
        model="gpt-5",
        input= input,
        reasoning={"effort": "high"}
    )
    return response.output_text

def o4_mini_high(text ,image_url_list):
    input = []
    # 输入message中的图片个数
    if len(image_url_list) == 0:
        input = [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": text},
                ]
            }
        ]
    elif len(image_url_list) == 1:
        # 需注意：传入Base64编码前需增加前缀 data:image/{图片格式};base64,{Base64编码}：
        # PNG图片："url":  f"data:image/png;base64,{base64_image}"
        # JPEG图片："url":  f"data:image/jpeg;base64,{base64_image}"
        # WEBP图片："url":  f"data:image/webp;base64,{base64_image}"
        input = [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": text},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{base64_image(image_url_list[0])}",
                    },
                ]
            }
        ]
    elif len(image_url_list) == 2:
        input = [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": text},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{base64_image(image_url_list[0])}",
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{base64_image(image_url_list[1])}",
                    },
                ]
            }
        ]
    elif len(image_url_list) == 3:
        input = [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": text},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{base64_image(image_url_list[0])}",
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{base64_image(image_url_list[1])}",
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{base64_image(image_url_list[2])}",
                    },
                ]
            }
        ]
    client = OpenAI(api_key = get_api_key("aihub"), base_url="https://aihubmix.com/v1")
    response = client.responses.create(
        model="o4-mini",
        input= input,
        reasoning={"effort": "high"}
    )
    print(str(response))
    return response.output_text

def claude_sonnet_4_5_thinking(text ,image_url_list):
    content = []
    client = Anthropic(
        api_key=get_api_key("aihub"),  # 换成你在 AiHubMix 生成的密钥
        base_url="https://aihubmix.com"
    )

    # 输入message中的图片个数
    if len(image_url_list) == 0:
        content = [
            {
                "type": "text",
                "text": text
            }
        ]
    elif len(image_url_list) == 1:
        content = [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": base64_image(image_url_list[0]),
                },
            },
            {
                "type": "text",
                "text": text
            }
        ]
    elif len(image_url_list) == 2:
        content = [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": base64_image(image_url_list[0]),
                },
            },
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": base64_image(image_url_list[1]),
                },
            },
            {
                "type": "text",
                "text": text
            }
        ]
    elif len(image_url_list) == 3:
        content = [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": base64_image(image_url_list[0]),
                },
            },
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": base64_image(image_url_list[1]),
                },
            },
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": base64_image(image_url_list[2]),
                },
            },
            {
                "type": "text",
                "text": text
            }
        ]

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=16000,
        thinking={
            "type": "enabled",
            "budget_tokens": 10000
        },
        messages=[
            {
                "role": "user",
                "content": content
            }
        ]
    )
    thinking_text = ""
    text = ""
    for block in response.content:
        if block.type == "thinking":
            thinking_text = block.thinking
        elif block.type == "text":
            text = block.text
    return thinking_text, text

def gemini_2_5_pro(text ,image_url_list):
    message = []
    # 输入message中的图片个数
    if len(image_url_list) == 0:
        message = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text}
                ]
            }
        ]
    elif len(image_url_list) == 1:
        # 需注意：传入Base64编码前需增加前缀 data:image/{图片格式};base64,{Base64编码}：
        # PNG图片："url":  f"data:image/png;base64,{base64_image}"
        # JPEG图片："url":  f"data:image/jpeg;base64,{base64_image}"
        # WEBP图片："url":  f"data:image/webp;base64,{base64_image}"
        message = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image(image_url_list[0])}"
                        },
                    },
                    {"type": "text", "text": text}
                ]
            }
        ]
    elif len(image_url_list) == 2:
        message = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image(image_url_list[0])}"
                        }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image(image_url_list[1])}"
                        },
                    },
                    {"type": "text", "text": text}
                ]
            }
        ]
    elif len(image_url_list) == 3:
        message = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image(image_url_list[0])}"
                        }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image(image_url_list[1])}"
                        }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image(image_url_list[2])}"
                        }
                    },
                    {"type": "text", "text": text}
                ]
            }
        ]

    client = OpenAI(
        api_key=get_api_key("aihub"),  # 换成你在 AiHubMix 生成的密钥
        base_url="https://aihubmix.com/v1"
    )
    response = client.chat.completions.create(
        model = "gemini-2.5-pro",
        messages = message,
    )
    return response.choices[0].message.content

def gpt_5_2(text ,image_url_list):
    input = []
    # 输入message中的图片个数
    if len(image_url_list) == 0:
        input = [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": text},
                ]
            }
        ]
    elif len(image_url_list) == 1:
        # 需注意：传入Base64编码前需增加前缀 data:image/{图片格式};base64,{Base64编码}：
        # PNG图片："url":  f"data:image/png;base64,{base64_image}"
        # JPEG图片："url":  f"data:image/jpeg;base64,{base64_image}"
        # WEBP图片："url":  f"data:image/webp;base64,{base64_image}"
        input = [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": text},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{base64_image(image_url_list[0])}",
                    },
                ]
            }
        ]
    elif len(image_url_list) == 2:
        input = [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": text},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{base64_image(image_url_list[0])}",
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{base64_image(image_url_list[1])}",
                    },
                ]
            }
        ]
    elif len(image_url_list) == 3:
        input = [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": text},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{base64_image(image_url_list[0])}",
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{base64_image(image_url_list[1])}",
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{base64_image(image_url_list[2])}",
                    },
                ]
            }
        ]
    client = OpenAI(api_key = get_api_key("aihub"), base_url="https://aihubmix.com/v1")
    response = client.responses.create(
        model="gpt-5.2",
        input= input,
        reasoning={"effort": "high"}
    )
    return response.output_text


if __name__ == '__main__':
    prompt = ("我要从易用性（易操作、易部署、易与其他系统集成）、可扩展性和友好性三个方面写一篇关于大模型可用性测评的报告，帮我总结一下目前测评上述维度的基准或数据集，以及如何对大模型进行测评的。")
    x = gpt_5_2(prompt, [])
    print(x)