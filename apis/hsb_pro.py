#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : hsb_pro.py
@Author  : liuzhiming
@Time    : 2021/6/7 18:50
"""

from base.own_api_base import OwnApiBase
import requests
import json
from urllib import parse
from utils.pmysql import Pmysql
import time


class HsbPro(OwnApiBase):

    def pro_get_login_captcha(self, phone):
        url = "https://hsbpro.huishoubao.com/hsbpro"
        interface = "get_login_captcha"
        param = {
            "phone": phone,
            "roleVerify": "0",
            "permissions": "0"
        }
        self.pro_post(url, interface, param)
        # 强制等待两秒钟，待数据库生成短信验证码
        time.sleep(2)


    def pro_get_smsCode(self, phone):
        self.pro_get_login_captcha(phone)
        sql = "SELECT s.content FROM hjxpushdb.sms_log_202106 s WHERE s.phone = {0} ORDER BY s.update_time DESC limit 1".format(phone)
        text = Pmysql().execute_sql(sql)
        # 从短信内容中获取验证码
        smsCode = text[0][0].split("验证码为：")[1][:6]
        print("获取到的验证码是：{0}".format(smsCode))
        return smsCode

    def pro_login(self, phone):
        url = "https://hsbpro.huishoubao.com/hsbpro"
        interface = "login_captcha"
        param = {
            "phone": phone,
            "captcha": self.pro_get_smsCode(phone),
            "permissions": "0"
        }
        res_data = self.pro_post(url, interface, param)
        login_token = res_data["_data"]["data"]["login_token"]
        user_id = res_data["_data"]["data"]["user_id"]
        user_name = res_data["_data"]["data"]["user_name"]
        role = res_data["_data"]["data"]["roleList"][0]
        merchant_id = res_data["_data"]["data"]["merchant_id"]

        return login_token, user_id, user_name, role, merchant_id

    def get_message_list(self, phone):
        url = "https://hsbpro.huishoubao.com/hsbpro"
        interface = "get_message_list"
        param = {
            "pageSize": "20",
            "permissions": "0",
            "pageIndex": "0"
        }
        self.pro_post(url, interface, param)


if __name__ == '__main__':
    p = "13049368516"
    pro = HsbPro()
    pro.get_message_list(p)
    pro.pro_login(p)
