#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : amc_client.py
@Author  : liuzhiming
@Time    : 2021/7/7 16:28
"""
from base.http_base import HttpBase
from urllib.parse import urlencode
import requests
from apis.amc_settings import *
import json
import time


class AmcClient:

    amc_client = HttpBase()
    amc_client.headers = HEADERS_FORM
    amc_client.protocol = PROTOCAL_AMC
    amc_client.domain = DOMAIN_AMC
    times = str(int(time.time()))

    def login(self, username=USERNAME_AMC, password=PASSWORD_AMC):
        path = "/login"
        forms = {
            "system_id": "32",
            "jump_url": "",
            "username": username,
            "password": password
        }
        res = self.amc_client.do_post(path, forms)
        amc_token = res["body"]["data"]["login_token"]
        amc_user_id = res["body"]["data"]["user_id"]
        login_info = {
            "amc_token": amc_token,
            "amc_user_id": amc_user_id
        }
        print("返回结果是：{}".format(login_info))
        return login_info

    amc_client.headers = HEADERS_JSON

    def get_user_info(self, token, user_id):
        path = "/logininfo"
        body = {
            "head": {
                "version": "0.01",
                "msgtype": "request",
                "interface": "logininfo",
                "remark": ""
            },
            "params": {
                "login_system_id": "1",
                "login_token": token,
                "login_user_id": user_id
            }
        }
        res = self.amc_client.do_post(path, body)
        user_name = res["body"]["data"]["user_info"]["real_name"]

        return user_name


if __name__ == '__main__':
    # aa = AmcClient().amc_login()
    # print(aa["amc_token"])
    ac = AmcClient()
    info = ac.login()
    ac.get_user_info(info["amc_token"], info["amc_user_id"])
