#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : hsb_app_api.py
@Author  : liuzhiming
@Time    : 2021/6/3 19:48
"""

from utils.common import *
from base.own_api_base import OwnApiBase
from urllib3 import encode_multipart_formdata
import requests
import random
from utils.logger import Logger, LoggerV2
import json
import time
import requests


class HsbAppApi:
    """
    回收宝APP相关接口集合
    """
    def __init__(self):
        # 实例化自有服务的http_client
        self.http_client = OwnApiBase()
        self.http_client.protocol = "https"
        self.http_client.domain ="api.huishoubao.com"

        self.temp = {}
        self.logger = LoggerV2()
        self.time = "{} 17:00-18:00".format(DATE_NOW)
        self.mark = True
        self.mark_text = ""

    def get_select(self):
        """从itemList中获取选中项,默认选中第一条"""
        x = 0    # 控制默认选中第几项
        select_ = []
        select_name = []
        item_list = self.temp["item_list"]
        for option in item_list:
            questions = option["questions"]
            id_ = questions[x]["id"]
            name_ = questions[x]["name"]
            select_.append(id_)
            select_name.append(name_)
        self.temp["select_"] = json.dumps(select_)   # 将list转换为str
        self.temp["selectName"] = select_name
        self.logger.debug(json.dumps(self.temp, indent=4, ensure_ascii=False))

    def login(self, phone=None, sms_code=None):
        if phone is None:
            phone = "18676702152"
            sms_code = "666666"
        path = "/api/user/login"
        body = {
            "loginType": "2",
            "tel": phone,
            "code": sms_code,
            "token": ""
        }
        res = self.http_client.own_post(path, body)
        self.temp = merge_dict(self.temp, res["_data"])
        if res["_errCode"] != "0":
            self.mark = False
            self.mark_text = "登录失败，_errCode：{} _errStr：{}".format(res["_errCode"],res["_errStr"])
            self.logger.error(self.mark_text)

    def get_balance_info(self, login_token=None, user_id=None):
        """
        获取钱包信息
        :return:
        """
        if login_token is None:
            login_token = self.temp["token"]
            user_id = self.temp["eid"]
        path = "/case/wallet/getBalanceInfo"
        body = {
            "token": login_token,
            "uid": user_id
        }
        res = self.http_client.own_post(path, body)
        return

    def get_address(self, x=0):
        """获取收货地址,x代表取第几条地址，默认取第一条地址信息"""
        path = "/V1/optimize/getAddressList"
        body = {
            "pageIndex": "1",
            "pageSize": "10",
            "recycleWay": "2",
            "token": self.temp["token"],
            "uid": self.temp["eid"]
        }
        res = self.http_client.own_post(path, body)
        self.temp = dict(self.temp, **res["_data"]["list"][0])  # 默认取第一条地址信息

    def get_procduct_list(self):
        """
        获取机型列表
        :return:
        """
        path = "/api/product/getProductList"
        body = {
            "brandId": "-1",
            "classId": "1",
            "pageIndex": "1",
            "pageSize": "100",
            "token": self.temp["token"],
            "uid": self.temp["eid"]
        }
        res = self.http_client.own_post(path, body)
        self.temp["productList"] = res["_data"]["productList"]

    def extract_product(self):
        """
        从temp的productList将支持的机型提取出来，只展示name和id
        :return:
        """
        my_dict = {}
        for product in self.temp["productList"]:
            p_key = product["productId"]
            p_value = product["productName"]
            my_dict[p_key] = p_value
        print(json.dumps(my_dict, indent=5, ensure_ascii=False))

    def get_service_time(self):
        """获取顺丰服务-上门时间"""
        path = "/V1/optimize/getServiceTime"
        body = {
            "token": self.temp["token"],
            "uid": self.temp["eid"]
        }
        res = self.http_client.own_post(path, body)
        sf_list = res["_data"]["sf"]
        service_time = "{} {}".format(sf_list[1]["time"], sf_list[1]["value"][0])
        self.temp["service_time"] = service_time

    def get_product_param(self, product_id):
        """根据产品id，获取检测选项"""
        path = "/api/product/getProductParam"
        body = {
            "productId": product_id,
            "token": self.temp["token"],
            "uid": self.temp["eid"]
        }
        res = self.http_client.own_post(path, body)
        item_list = res["_data"]["itemList"]
        self.temp["item_list"] = item_list

    def get_evaluate(self, product_id):
        """获取估价信息"""
        path = "/api/product/evaluate"
        body = {
            "productId": product_id,
            "select": self.temp["select_"],
            "recycleType": "6",
            "token": self.temp["token"],
            "uid": self.temp["eid"]
        }
        res = self.http_client.own_post(path, body)
        self.temp = merge_dict(self.temp, res["_data"])

    def get_evaluate_result(self):
        """
        获取活动信息
        :return:
        """
        path = "/api/product/getEvaluateResult"
        body = {
            "evaluateid": self.temp["evaluateid"],
            "token": self.temp["token"],
            "uid": self.temp["eid"]
        }
        res = self.http_client.own_post(path, body)

    def get_allow_coupon_list(self, product_id, recycle_type=1):
        """
        获取满加券信息
        recycle_type: 1. 2. 3.
        """
        if isinstance(recycle_type, int):
            recycle_type = str(recycle_type)
        if recycle_type not in ["1", "2", "3"]:
            err_text = "recycle_type参数只能是1、2、3"
            self.logger.error(err_text)
            return

        path = "/V1/coupon/getAllowCouponList"
        p_dict = [{"proId": product_id, "price": self.temp["quotation"], "num": "1"}]
        product_list = json.dumps(p_dict)
        body = {
            "productList": product_list,
            "recycleType": recycle_type,
            "token": self.temp["token"],
            "uid": self.temp["eid"]
        }
        res = self.http_client.own_post(path, body)

    def get_price_history(self, product_id):
        """
        获取商品的历史价格信息
        :param product_id:
        :return:
        """
        path = "/V1/optimize/getPriceHistory"
        body = {
            "price": self.temp["quotation"],
            "productId": product_id,
            "token": self.temp["token"],
            "uid": self.temp["eid"]
        }
        res = self.http_client.own_post(path, body)

    def get_store_list(self):
        """获取附近店铺列表"""
        path = "/api/xianyu/getStoreList"
        body = {
            "areaId": "440305",
            "latitude": "22.529",
            "longitude": "113.948",
            "pageIndex": "1",
            "pageSize": "10",
            "token": self.temp["token"],
            "uid": self.temp["eid"]
        }
        res = self.http_client.own_post(path, body)
        self.temp["storeList"] = res["_data"]["storeList"]

    def place_order_sending(self):
        """下单-顺丰邮寄"""
        path = "/V1/order/placeOrder"
        body = {
            "address": self.temp["address"],
            "city": self.temp["cityName"],
            "county": self.temp["areaName"],
            "evaluateid": self.temp["evaluateid"],
            "payType": "26",
            "province": self.temp["provinceName"],
            "recycleType": "1",
            "regionId": self.temp["cityCode"],
            "tel": self.temp["tel"],
            "time": self.temp["service_time"],
            "token": self.temp["token"],
            "uid": self.temp["eid"],
            "userName": self.temp["userName"]
        }
        res = self.http_client.own_post(path, body)
        err_code = res["_errCode"]
        if err_code == "0":
            self.temp = dict(self.temp, **res["_data"])
            order_id = res["_data"]["orderid"]
            order_num = res["_data"]["orderNum"]
            self.mark_text = "下单成功，订单ID：【{}】订单编号：【{}】".format(order_id, order_num)
        else:
            self.mark_text = "下单失败，请检查日志"
        # self.logger.debug(json.dumps(self.temp, indent=4, ensure_ascii=False))

    def place_order_door(self, loginToken, uuid):
        """上门回收"""
        if loginToken is None:
            loginToken = self.temp["token"]
        if uuid is None:
            uuid = self.temp["eid"]
        path = "/V1/order/placeOrder"
        body={
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
        res = self.http_client.own_post(path, body)

    def place_order_store(self):
        """下单-到店回收"""
        path = "/V1/optimize/getAddressList"
        body = {
            "pageIndex": "1",
            "pageSize": "10",
            "recycleWay": "",
            "token": "",
            "uid": ""
        }


if __name__ == '__main__':
    # num = 10
    # product_id = "30749"
    # 所有机型的id列表
    # 校验登录成功或失败
    own = HsbAppApi()
    # own.get_honor_order_list()
    own.login()
    # own.get_balance_info()
    # own.get_procduct_list()
    # own.extract_product()
    # if own.mark:
    #     own.get_service_time()
    #     own.get_address()
    #     own.get_store_list()
    #     for x in range(num):
    #         own.get_product_param(product_id)
    #         own.get_select()
    #         own.get_evaluate(product_id)
    #         own.get_allow_coupon_list(product_id,5)
    #         own.get_price_history(product_id)
    #         own.get_evaluate_result()
    #         own.place_order_sending()

