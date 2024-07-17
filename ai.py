import json
import requests
import sys
from string import Template

url_generate = "http://localhost:11434/api/generate"

def get_response(url, data):
    response = requests.post(url, json=data)
    response_dict = json.loads(response.text)
    response_content = response_dict["response"]
    return response_content

def ask_ai(s):
    data = {
    "model": "llama3:8b",
    "prompt": s,
    "stream": False
    }
    res = get_response(url_generate,data)
    return res

def main():
    args = sys.argv
    print(ask_ai(args[1]))

if __name__ == "__main__":
    main()