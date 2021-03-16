# -*- coding: utf-8 -*-
"""
@Time ： 2021/3/11
@Auth ： zhangqimin
@File ：send_message_dingtalk.py
@IDE ：PyCharm

"""
import requests
import json
def send_message(cont):
    message = {
        "msgtype": "text",
        "text": {
            "content": cont
        }
    }
    url = ""
    headers = {
        "Content-Type": "application/json"
    }
    requests.post(url=url, data=json.dump(message), headers=headers)

if __name__ == '__main__':
    send_message("测试报告")