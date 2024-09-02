import json
import requests
import sys
from string import Template


# prompt = "将输入内容中的英文部分翻译为中文后输出，翻译时用词要简洁、符合计算机游戏编程术语。输出结果中除了翻译内容外不要有任何的额外描述或是进一步的询问。这是输入内容："

prompt = Template("""
    接下来我会输入一段需要翻译的文本以及相关信息，文本来自UE引擎中的函数分类，相关信息为函数分类中的函数名称及所属类，请根据它的相关信息为我提供它的翻译

    需要翻译的文本：$main

    <以下是相关信息>
    所属类：$sub1
    分类中的函数名称：$sub2

    注意，只需要回答对需要翻译的文本的翻译，不需要包含任何额外输出。回答必须使用简短的中文名词。
    """
)

url_generate = "http://localhost:11434/api/generate"

def get_response(url, data):
    response = requests.post(url, json=data)
    response_dict = json.loads(response.text)
    response_content = response_dict["response"]
    return response_content

def translate(main,sub1,sub2):
    data = {
    "model": "llama3.1:8b",
    "prompt": prompt.substitute(main=main, sub1=sub1, sub2=sub2),
    "stream": False
    }
    res = get_response(url_generate,data)
    return res

def main():
    args = sys.argv
    print(translate(args[1], args[2], args[3]))

if __name__ == "__main__":
    main()