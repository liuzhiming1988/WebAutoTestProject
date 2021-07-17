#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : hsb_pro_api.py
@Author  : liuzhiming
@Time    : 2021/6/7 18:50
"""

from utils.common import *
from base.pro_api_base import ProApiBase
import requests
import json
from urllib.parse import urlencode
from urllib import parse
from utils.pmysql import Pmysql
from utils.logger import Logger
import time


class HsbProApi:

    def __init__(self):
        self.logger = Logger().logger
        self.mark = True
        self.temp = {}

        # 实例化专业版api client
        self.pro_client = ProApiBase()
        self.pro_client.protocol = "https"
        self.pro_client.domain = "hsbpro.huishoubao.com"
        self.pro_client.headers = {
        "Content-Type": "application/json; charset=utf-8"
    }

    def login(self, phone=None, sms_code=None):
        if phone is None:
            phone = "18676702152"
            sms_code = "666666"

        interface = "login_captcha"
        param = {
            "phone": phone,
            "captcha": sms_code,
            "permissions": "0"
        }
        res = self.pro_client.pro_post(interface, param)
        if res["_data"]["_errCode"] == "0":
            self.temp = merge_dict(self.temp, res["_data"]["data"])
        else:
            self.mark = False
            self.logger.error("登录失败，_errCode：{} _errStr：{}".format(res["_data"]["_errCode"], res["_data"]["_errStr"]))




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
    pro = HsbProApi()
    pro.login()

