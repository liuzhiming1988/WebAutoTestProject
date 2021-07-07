#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : wms_admin.py
@Author  : liuzhiming
@Time    : 2021/7/7 15:52
"""

import requests
import json
from base.http_base import HttpBase
from urllib.parse import urlencode
from apis.amc_settings import *
from apis.amc_client import AmcClient
import time


class WmsClient:

    wms_client = HttpBase()
    wms_client.headers = HEADERS_JSON
    wms_client.protocol = PROTOCAL_WMS
    wms_client.domain = DOMAIN_WMS

    ac = AmcClient()
    login_info = ac.login()
    TOKEN = login_info["amc_token"]
    USER_ID = login_info["amc_user_id"]
    USER_NAME = ac.get_user_info(TOKEN, USER_ID)

    times = str(int(time.time()))

    wms_path = "/admin/handle"


    def get_user_info(self):
        path = "/admin/getLoginUserInfo"
        body = {
            "_head":{
                "_version": "0.01",
                "_msgType": "request",
                "_timestamps": self.times,
                "_interface":"loginuserinfo",
                "_remark":""
            },
            "_param":{
                "loginUserId": self.USER_ID,
                "loginToken": self.TOKEN
            }
        }
        res = self.wms_client.do_post(path, body)
        user_name = res["_data"]["_data"]["userInfo"]["real_name"]

        return user_name


    def sign(self, logistics_num):
        """
        签收
        :return:
        """
        body = {
            "_head": {
                "_version": "0.01",
                "_msgType": "request",
                "_timestamps": self.times,
                "_interface": "PlatWms.Parcel.Sign",
                "_remark": ""
            },
            "_param": {
                "loginUserId": "1930",
                "loginToken": self.TOKEN,
                "depotId": "1",
                "logisticsId": "1",
                "paymentMethod": "1",
                "logisticsNum": logistics_num,
                "userId": self.USER_ID,
                "userName": self.USER_NAME
            }
        }
        self.wms_client.do_post(self.wms_path, body)

    def unpack(self, logistics_num):
        body = {
            "_head": {
                "_version": "0.01",
                "_msgType": "request",
                "_timestamps": self.times,
                "_interface": "PlatWms.Parcel.Unpack",
                "_remark": ""
            },
            "_param":{
                "loginUserId": self.USER_ID,
                "loginToken": self.TOKEN,
                "depotId":"1",
                "logisticsNum": logistics_num,
                "productType": "1",
                "num": "1",
                "userId": self.USER_ID,
                "userName": self.USER_NAME
            }
        }
        self.wms_client.do_post(self.wms_path, body)











if __name__ == '__main__':
    wms = WmsClient()
    sf = "SF12345678"
    wms.sign(sf)
    wms.unpack(sf)

