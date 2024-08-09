'''推送消息到各种平台'''
import os

import requests
from dotenv import load_dotenv

from get_notice import make_wechat_message

load_dotenv()

APPTOKEN = os.getenv('APPTOKEN')
UIDS = os.getenv('UIDS').split(',')

url = "https://wxpusher.zjiecode.com/api/send/message"

def send_message_by_wxpusher(summary, message, link):
    '''通过wxpusher平台发送消息'''
    # message 为 None 时,没有新消息，不发送
    if message is None:
        print("没有新消息，不发送")
        return
    
    json_data = {
    "appToken": APPTOKEN,
    "content": message,
    "summary": summary,
    "contentType": 1,
    "uids": UIDS,
    "url": link, # 原文链接，可选参数
    "verifyPay": False,
    }
    
    response = requests.post(url, json=json_data, timeout=5)
    print(response.json())

if __name__ == '__main__':
    summary, message, length, link = make_wechat_message()
    send_message_by_wxpusher(summary, message, link)
