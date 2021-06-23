#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : own_order.py
@Author  : liuzhiming
@Time    : 2021/6/3 19:48
"""

from utils.common import *
from base.own_api_base import OwnApiBase
from urllib3 import encode_multipart_formdata
import requests
from utils.logger import Logger


class OwnOrder(OwnApiBase):

    logger = Logger().logger

    def get_evaluate(self, loginToken, uuid):
        path = self.domain+"/api/product/evaluate"
        select = """["12","17","37","44","1113","83","79","5531","3247","62"]"""

        data={
            "productId": "38200",
            "select": select,
            "recycleType": "6",
            "token": loginToken,
            "uid": uuid
        }
        data=dict(data, **self.get_common_args())
        data=get_signData(data)
        print(self.json_format(data))
        bd = self.boundary
        data_res = encode_multipart_formdata(data, boundary=bd)
        response = requests.post(path, data=data_res[0], headers=self.get_headers_multipart(bd))
        info = self.json_format(response.json())
        print("接口{0}的返回结果是\n{1}".format(path, info))
        evaluateId = json.loads(response.text)["_data"]["evaluateid"]
        print(evaluateId)
        return evaluateId

    def place_order(self, loginToken, uuid):
        path = self.domain+"/V1/order/placeOrder"
        data={
            "address": "科苑闲鱼1",
            "city": "",
            "county": "",
            "evaluateid": self.get_evaluate(loginToken, uuid),
            "payType": "26",
            "province": "",
            "recycleType": "6",
            "regionId": "440305",
            "storeId": "669",
            "tel": "13049368516",
            "time": "2021-06-04 10:00-12:00",
            "token": loginToken,
            "uid": uuid,
            "userName": ""
        }
        data=dict(data, **self.get_common_args())
        data=get_signData(data)
        print(self.json_format(data))
        bd = self.boundary
        data_res = encode_multipart_formdata(data, boundary=bd)
        response = requests.post(path, data=data_res[0], headers=self.get_headers_multipart(bd))
        info = self.json_format(response.json())
        print("接口{0}的返回结果是\n{1}".format(path, info))

