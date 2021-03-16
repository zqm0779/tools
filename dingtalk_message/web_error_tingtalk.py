# -*- coding: utf-8 -*-
"""
@Time ： 2021/3/12
@Auth ： zhangqimin
@File ：web_error_tingtalk.py
@IDE ：PyCharm

"""
"""
python+requests实现网站异常钉钉报警
产品官网的持续运行至关重要，不能出现无法访问等致命错误，所以需要时刻检测网站是否正常，通过像网站发送get请求的方式，根据返回的状态码来判断网页是否能正常访问，若有异常第一时间发送钉钉消息，通知相关同事。

"""

import requests
import json
import time
import datetime
import logging
import os
# parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# log_path = parent + '\\' + 'log' +'\\' + 'check_log.txt'
# if not os.path.exists(log_path):
#     os.makedirs(log_path)
logfile = 'check_log.txt'
#已官网测试网址
urls = [
    'https://wx.guorou.net/my-lesson',
    'https://wx.guorou.net/1'
]
#获取当前时间日期
curr_time = datetime.datetime.now()
#检测函数，默认超时为20s
def check_url_state(url, timeout=20):
    try:
        # 对网站发送get请求，并返回状态码
        r = requests.get(url, timeout=timeout)
        return r.status_code
    except requests.exceptions.RequestException as e:
        logging.error(e)
        return "timeout"
#钉钉报警函数，通过机器人发送信息
def send_ding(text):
    import requests
    # 钉钉群机器人的webhook地址
    url = "https://oapi.dingtalk.com/robot/send?access_token=db1eda13a8445db1ea6d26af9d188d32be1f12e72261916e294ec4273643f625"
    payload = "{\r\n    \"msgtype\": \"text\", \r\n    \"text\": {\r\n        \"content\": \"" + text + "\"\r\n    }\r\n}"
    payload = payload.encode('utf-8')
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text.encode('utf8'))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - [%(levelname)s] - %(filename)s - %(message)s',
                        filename=logfile,
                        filemode='a')
    for url in urls:
        if check_url_state(url) !=200 :
            time_str = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
            content = '测试网址访问报错啦：{} went wrong'.format(url) + '\n'
            send_ding(content)
            logging.warning(content)
        else:
            print("ok:", url)
            logging.info('%s', url)




