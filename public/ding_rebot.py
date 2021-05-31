#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : ding_rebot.py
@Author  : liuzhiming
@Time    : 2021/5/28 19:31
"""

import hmac
import hashlib
import base64
import time
import requests
import json

timestamp = str(int(round(time.time()*1000)))
print(timestamp)
app_secret = 'this is a secret'
app_secret_enc = app_secret.encode('utf-8')
string_to_sign = '{}\n{}'.format(timestamp, app_secret)
string_to_sign_enc = string_to_sign.encode('utf-8')
hmac_code = hmac.new(app_secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
sign = base64.b64encode(hmac_code).decode('utf-8')
print(sign)

web_hook=''
url = web_hook+'&timestamp='+timestamp+'&sign='+sign
HEADERS = {'Content-Type': 'application/json'}
data = {
    "msgtype": "text",
    "text": {
        "content": "这是一个消息，群机器人新建成功了，这里随便输入你想要发送的消息"
    }
}

res = requests.post(url=url, headers=HEADERS, json=json.dumps(data))
print(res.text)
