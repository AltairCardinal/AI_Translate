import json
import requests
import sys
from string import Template
import ollama

# prompt = "将输入内容中的英文部分翻译为中文后输出，翻译时用词要简洁、符合计算机游戏编程术语。输出结果中除了翻译内容外不要有任何的额外描述或是进一步的询问。这是输入内容："

prompt = Template("""
    接下来我会输入一段需要翻译的文本，文本来自电影字幕，将其翻译为中文。注意，只需要回答对需要翻译的文本的翻译，不需要包含任何额外输出。
    需要翻译的文本：$eng
    """
)

prompt_sys = '你是一个专业翻译助手，将所有用户输入翻译为中文。保持格式不变、原意准确、除了翻译内容外不要进行任何额外输出'

url_generate = "http://localhost:11434/api/generate"

def get_response(url, data):
    response = requests.post(url, json=data)
    print(response.text)
    response_dict = json.loads(response.text)
    response_content = response_dict["response"]
    return response_content

def translate_by_requests(eng):
    data = {
    "model": "llama3.2:3b",
    "prompt": prompt.substitute(eng=eng),
    "stream": False
    }
    res = get_response(url_generate,data)
    return res

def translate(_c):
    response = ollama.chat(model='llama3.1', messages=[
        {
            'role': 'system',
            'content': prompt_sys,
        },
        {
            'role': 'user',
            'content': _c,
        },
    ])
    return response['message']['content']

def main():
    while True:
        user_input = input('请输入待翻译内容：')
        if user_input.lower() == 'exit':
            print('退出程序')
            break
        else:
            print(translate(user_input))

if __name__ == "__main__":
    main()