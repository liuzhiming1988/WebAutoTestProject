#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : hsb_sale.py
@Author  : liuzhiming
@Time    : 2021/6/7 19:47
"""
from base.own_api_base import HsbApiBase
import requests
import json
from urllib import parse
from public.pmysql import Pmysql
import time


class HsbSale(HsbApiBase):

    def sale_post(self, url, data):
        res = requests.post


    def login(self, phone, passwd):
        """
        曲线救国，从竞拍PC网站登录，获取token，然后给小程序中的接口使用
        :param phone:
        :param passwd:
        :return:
        """
        url = "https://saleapi.huishoubao.com/front/user?i=user_login"
        data = {
            "head": {
                "version": "0.01",
                "msgtype": "request",
                "interface": "user_login",
                "remark": ""
            },
            "params": {
                "login_token": "",
                "time": self.timestamp,
                "system": "SALESAPP",
                "loginType": 1,
                "account": phone,
                "password": passwd,
                "verifyType": "1",
                "sign": "fdhakhgklngbfk78hHjgfd"
            }
        }

        res = requests.post(url, data=json.dumps(data), headers=self.headers_json).text
        res_data = json.loads(res)
        login_token = res_data["body"]["data"]["login_token"]
        user_id = res_data["body"]["data"]["userId"]
        print(self.json_format(res_data))
        return login_token

    def create_order(self, login_token):
        """
        精准发布，帮卖订单
        :return:
        """
        url = "https://saleapi.huishoubao.com/front/bm2border?i=create_order"
        data = {
            "head": {
                "interface": "create_order"
            },
            "params": {
                "code": "0432cyll2kjna748QBml2dsSvm22cylG",
                "type": 1,
                "product_qty": 1,
                "eva_id": "210650179",
                "pro_id": 41567,
                "reference_price": "170900",
                "login_token": login_token,
                "clientType": "sapp",
                "clientVersion": "2.10.11",
                "clientId": "c3dd830871bc5d63d5227308a0a34055"
            }
        }
        res = requests.post(url, data=json.dumps(data), headers=self.headers_json).text
        res_data = json.loads(res)
        order_number = res_data["body"]["data"]["orderId"]
        print(self.json_format(res_data))
        return order_number

    def delivery(self, order_id):
        url = "https://saleapi.huishoubao.com/front/bm2border?i=shipping_self_delivery"
        data = {
            "head": {
                "interface": "shipping_self_delivery"
            },
            "params": {
                "orderId": order_id,
                "type": 1,
                "expressCompany": "顺丰速运",
                "expressNumber": "SF666168{0}".format(order_id),
                "login_token": "1a07e89cfade39f31901f8bad1f0d847",
                "clientType": "sapp",
                "clientVersion": "2.10.11",
                "clientId": "c3dd830871bc5d63d5227308a0a34055"
            }
        }
        pp = self.json_format(data)
        print(pp)
        res = requests.post(url, data=json.dumps(data), headers=self.headers_json).text
        res_data = json.loads(res)
        print(self.json_format(res_data))



if __name__ == '__main__':
    login_token = HsbSale().login("13049368516", "123456")
    list = []
    for i in range(5):
        res = HsbSale().create_order(login_token)
        list.append(res)

    print(list)
    for order_id in list:
        HsbSale().delivery(order_id)

