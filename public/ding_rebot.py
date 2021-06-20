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


class DingRebot:

    def __init__(self):
        self.timestamp = str(int(round(time.time()*1000)))
        self.app_secret = 'SEC0aa8af9aeda9cf0ef086841224ec23dce15abab2222814d5047181acdc6d5765'
        self.web_hook = 'https://oapi.dingtalk.com/robot/send?access_token=8d62616f9b791b5bfcd7404d3ac013c181c462be0da7fb99c411aad3b792d95d'
        self.HEADERS = {'Content-Type': 'application/json;charset=utf-8'}

    def get_url(self):
        app_secret_enc = self.app_secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(self.timestamp, self.app_secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(app_secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = base64.b64encode(hmac_code).decode('utf-8')
        # print(sign)
        url = self.web_hook + '&timestamp=' + self.timestamp + '&sign=' + sign
        return url

    def send_text(self, text):
        """
        发送文本消息
        :param text:
        :return:
        """
        data = {
            "msgtype": "text",
            "text": {
                "content": text   # 消息内容
            },
            "at": {
                "atMobiles": [  # 此处为需要@什么人。填写具体用户
                    # "13049368516"
                ],
                "isAtAll": False  # 此处为是否@所有人
            }
        }

        res = requests.post(self.get_url(), data=json.dumps(data), headers=self.HEADERS)
        print(res.text)

    def send_link(self, link):
        """
        发送链接消息，传入一个字典，需包含title，text，picUrl，messageUrl
        :return:
        """
        data = {
            "msgtype": "link",
            "link": link
        }
        res = requests.post(self.get_url(), data=json.dumps(data), headers=self.HEADERS)
        print(res.text)


if __name__ == '__main__':
    DR = DingRebot()
    DR.send_text("测试：我是一个毫无感情的机器人")
    link = {
        "title": "钉钉机器人",
        "text": "--2021年6月5号，",
        "messageUrl": "http://www.baidu.com"
    }
    DR.send_link(link)
