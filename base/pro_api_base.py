#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : pro_api_base.py
@Author  : liuzhiming
@Time    : 2021/6/25 下午9:50
"""
from base.http_base import HttpBase
import time
import random
import json


class ProApiBase(HttpBase):

    def __init__(self):
        super().__init__()
        self.timestamp = str(int(time.time()))

    def getProData(self, _interface, _param):
        # 构建字典请求体
        formData = {
            "_head": {
                "_remark": "",
                "_appVersion": "5.0.0",
                "_version": "0.01",
                "_groupNo": "1",
                "longitude": 113.94299928073816,
                "latitude": 22.532460629273437,
                "_interface": _interface,
                "_timestamps": self.timestamp,
                "_invokeId": "iOS_C854F1C2-5E70-44D3-853C-655BBA17E54E_{0}".format(self.timestamp),
                "_msgType": "request",
                "channelStr": "appstore",
                "_callerServiceId": "111111"
            },
            "_param": _param
        }

        return formData


if __name__ == '__main__':
    pro_client = ProApiBase()
    path = "/hsbpro"
    pro_client.headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8"
    }
    pro_client.protocol = "https"
    pro_client.domain = "hsbpro.huishoubao.com"
    _interface = "get_merchant_info"
    _param = {
            "login_token": "4512751100206992728bcfb5e6d8f458",
            "merchantId": "220395845",
            "permissions": "0",
            "queryType": "tagInfo"
    }
    data = pro_client.getProData(_interface, _param)

    pro_client.do_post(path, data)

