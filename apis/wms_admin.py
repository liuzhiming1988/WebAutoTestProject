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

    # 定义一个字典，来接收临时变量
    # g = {}

    ac = AmcClient()
    g = ac.login()    # login()返回的是一个字典
    g["user_name"] = ac.get_user_info(g["loginToken"], g["loginUserId"])

    times = str(int(time.time()))

    wms_path = "/admin/handle"

    def get_user_info(self):
        path = "/admin/getLoginUserInfo"
        body = {
            "_head": {
                "_version": "0.01",
                "_msgType": "request",
                "_timestamps": self.times,
                "_interface":"loginuserinfo",
                "_remark":""
            },
            "_param": {
                "loginUserId": self.g["loginUserId"],
                "loginToken": self.g["loginToken"]
            }
        }
        res = self.wms_client.do_post(path, body)
        user_name = res["_data"]["_data"]["userInfo"]["real_name"]
        self.g["user_name"] = user_name

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
                "loginToken": self.g["loginToken"],
                "depotId": "1",
                "logisticsId": "1",
                "paymentMethod": "1",
                "logisticsNum": logistics_num,
                "userId": self.g["loginUserId"],
                "userName": self.g["user_name"]
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
                "loginUserId": self.g["loginUserId"],
                "loginToken": self.g["loginToken"],
                "depotId":"1",
                "logisticsNum": logistics_num,
                "productType": "1",
                "num": "1",
                "userId": self.g["loginUserId"],
                "userName": self.g["user_name"]
            }
        }
        self.wms_client.do_post(self.wms_path, body)

    def receive_search(self, logistics_num):
        body = {
            "_head": {
                "_version": "0.01",
                "_msgType": "request",
                "_timestamps": self.times,
                "_interface": "PlatWms.Parcel.ReceiveSearch",
                "_remark": ""
            },
            "_param": {
                "loginUserId": self.g["loginUserId"],
                "loginToken": self.g["loginToken"],
                "receiveType": "1",
                "depotId": "1",
                "orderSystemId": "1",
                "orderSystemType": "1",
                "logisticsNum": logistics_num,
                "searchType": "0",
                "keywords": ""
            }
        }
        res = self.wms_client.do_post(self.wms_path, body)
        total = res["_data"]["_data"]["pageInfo"]["total"]
        if int(total) > 0:
            for x in range(int(total)):
                number = res["_data"]["_data"]["orderList"][x]["logisticsNumber"]

                if number == logistics_num:
                    res_final = res["_data"]["_data"]["orderList"][x]    # 取出符合条件的订单的信息
                    parcelId = res["_data"]["_data"]["parcelId"]
                    # 将第一条订单的信息拼接到g变量中
                    self.g = dict(self.g, **res_final)
                    self.g["parcelId"] = parcelId
                    text = "已搜索到订单：{}".format(res_final)
                    print(text)
                    return text
        else:
            text = "可回收收货订单为0，无法进行回收，请检查！！！"
            print(text)
            return text

    def get_order_product(self, order_id=None):
        if order_id is None:
            order_id = self.g["orderId"]
        body = {
             "_head": {
                  "_version": "0.01",
                  "_msgType": "request",
                  "_timestamps": self.times,
                  "_interface": "PlatWms.Parcel.GetOrderProduct",
                  "_remark": ""
             },
             "_param": {
                  "loginUserId": self.g["loginUserId"],
                  "loginToken": self.g["loginToken"],
                  "orderId": order_id,
                  "orderSystemId": "1"
             }
        }
        res = self.wms_client.do_post(self.wms_path, body)
        res = res["_data"]["_data"]["orderProductList"][0]
        self.g = dict(self.g, **res)

    def get_product_code(self, order_id=None):
        if order_id is None:
            order_id = self.g["orderId"]
        body = {
             "_head": {
                  "_version": "0.01",
                  "_msgType": "request",
                  "_timestamps": self.times,
                  "_interface": "PlatWms.Parcel.GetProductCode",
                  "_remark": ""
             },
             "_param": {
                  "loginUserId": self.g["loginUserId"],
                  "loginToken": self.g["loginToken"],
                  "orderChannelId": self.g["orderChannelId"],
                  "number": 1,
                  "depotId": "1",
                  "type": "01",
                  "orderChannelType": "1",
                  "groupCode": "",
                  "orderIdArr": [
                       order_id
                  ]
             }
        }
        res = self.wms_client.do_post(self.wms_path, body)
        res = res["_data"]["_data"]["data"][0]
        self.g = dict(self.g, **res)

    def bind_order(self):
        product_info = {
            "productId": self.g["productId"],
            "productCode": self.g["productCode"],
            "classId": self.g["classId"],
            "brand": self.g["brand"],
            "model": self.g["model"],
            "imei": self.g["imei"]
        }

        product_info = """[{}]""".format(json.dumps(product_info, ensure_ascii=False))

        body = {
            "_head": {
                "_version": "0.01",
                "_msgType": "request",
                "_timestamps": self.times,
                "_interface": "PlatWms.Parcel.BindOrder",
                "_remark": ""
            },
            "_param": {
                "loginUserId": self.g["loginUserId"],
                "loginToken": self.g["loginToken"],
                "receiveType": "1",
                "logisticsNum": self.g["logisticsNumber"],
                "depotId": "1",
                "orderSystemId": self.g["orderSystemId"],
                "orderSystemType": "1",
                "orderChannelId": self.g["orderChannelId"],
                "orderChannelType": self.g["orderChannelType"],
                "orderId": self.g["orderId"],
                "orderSn": self.g["orderSn"],
                "orderWeb": self.g["orderWeb"],
                "orderPhone": self.g["orderPhoneEncrypt"],
                "num": self.g["num"],
                "parcelId": self.g["parcelId"],
                "productInfo": product_info,
                "partsCode": "",
                "partsInfo": "",
                "userName": "刘志明_TEST",
                "userId": "1930"
            }
        }
        res = self.wms_client.do_post(self.wms_path, body)
        err_str = res["_data"]["_errStr"]
        print("物流单号【{}】的测试结果为：{}".format(self.g["logisticsNumber"], err_str))



if __name__ == '__main__':
    wms = WmsClient()
    sf = "SF1020091936096"
    wms.sign(sf)
    wms.unpack(sf)
    wms.receive_search(sf)
    wms.get_order_product()
    wms.get_product_code()
    wms.bind_order()
    # print(wms.g)
