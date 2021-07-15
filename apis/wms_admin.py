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
from apis.admin_settings import *
from apis.amc_client import AmcClient
import time
from utils.logger import Logger
import copy


class WmsClient:

    def __init__(self):
        self.logger = Logger().logger
        self.wms_client = HttpBase()
        self.wms_client.headers = HEADERS_JSON
        self.wms_client.protocol = PROTOCAL_WMS
        self.wms_client.domain = DOMAIN_WMS
        self.times = str(int(time.time()))
        self.wms_path = "/admin/handle"
        # 定义接口返回字典格式，各接口使用时可deep copy后再进行赋值
        self.result = {
            "test_result": "success",  # 测试结果：success or fail
            "mark_text": "",        # 提示语
            "raw_data": ""  # 原始响应信息
        }
        # 定义一个字典，来接收临时变量
        self.g = {}
        self.mark = True
        self.mark_text = ""

    def result_creator(self, name, res):
        """构造测试结果"""
        if res:
            result = copy.deepcopy(self.result)
            result["raw_data"] = res
            err_str = res["_data"]["_errStr"]
            err_code = res["_data"]["_errCode"]
            if err_code == "0":
                result["mark_text"] = "{}:{}".format(name, err_str)
                self.mark = True
            else:
                result["mark_text"] = "{}:{}".format(name, err_str)
                result["test_result"] = "fail"
                self.mark_text += "错误码：{}，错误描述：{}<br />".format(err_code,err_str)
                self.mark = False
            result = json.dumps(result, indent=5, ensure_ascii=False)
            return result
        else:
            return False

    def get_auth(self):
        """从amc系统获取loginToken，userId，userName信息"""
        ac = AmcClient()
        auth_info = ac.login()    # login()返回的是一个字典
        self.g = dict(self.g, **auth_info)
        name_info = ac.get_user_info(self.g["loginToken"], self.g["loginUserId"])
        self.g = dict(self.g, **name_info)

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
                "loginUserId": self.g["loginUserId"],
                "loginToken": self.g["loginToken"],
                "depotId": "1",
                "logisticsId": "1",
                "paymentMethod": "1",
                "logisticsNum": logistics_num,
                "userId": self.g["loginUserId"],
                "userName": self.g["user_name"]
            }
        }
        res = self.wms_client.do_post(self.wms_path, body)
        if res:
            res_final = self.result_creator("签收物流单", res)
            return res_final
        else:
            return res

    def unpack(self, logistics_num, num=1):
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
                "num": num,
                "userId": self.g["loginUserId"],
                "userName": self.g["user_name"]
            }
        }
        res = self.wms_client.do_post(self.wms_path, body)
        if res:
            res_final = self.result_creator("签收物流单", res)
            return res_final
        else:
            return res

    def receive_search(self, logistics_num):
        """按物流单号搜索，从返回的多条记录中找出对应的回收单，如果返回结果是0，则提示"""
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
        if res:
            res_final = self.result_creator("到货回收-匹配订单", res)
            err_code = res["_data"]["_errCode"]
            text = ""
            if err_code == "0":
                total = res["_data"]["_data"]["pageInfo"]["total"]
                if int(total) > 0:
                    match_mark = True
                    for x in range(int(total)):
                        number = res["_data"]["_data"]["orderList"][x]["logisticsNumber"]
                        if number == logistics_num:
                            match_mark = False
                            res_final = res["_data"]["_data"]["orderList"][x]    # 取出符合条件的订单的信息
                            self.g["parcelId"] = res["_data"]["_data"]["parcelId"]
                            # 将符合条件的信息拼接到g变量中
                            self.g = dict(self.g, **res_final)
                            text += "，已匹配到订单：{}".format(res_final)
                            self.logger.info(text)
                            break
                    if match_mark:
                        text += "返回订单数量：{}，匹配到可收货订单为0，无法进行回收，请检查！！！<br /><hr />".format(int(total))
                        self.mark_text += text
                        self.mark = False
                else:
                    text += "匹配到可收货订单为0，无法进行回收，请检查！！！<br /><hr />"
                    self.mark_text += text
                    self.mark = False
                self.logger.info(self.mark_text)
                return res_final
            else:
                self.mark_text += "<br /><hr />"
        else:
            return res

    def get_order_product(self, order_id=None):
        """获取订单对应的产品信息"""
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
        if res:
            res_final = self.result_creator("获取订单对应的产品信息", res)
            res = res["_data"]["_data"]["orderProductList"][0]
            self.g = dict(self.g, **res)
            return res_final
        else:
            return res


    def get_product_code(self, order_id=None):
        """确认商品"""
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
        if res:
            res_final = self.result_creator("确认商品", res)
            res = res["_data"]["_data"]["data"][0]
            self.g = dict(self.g, **res)
            return res_final
        else:
            return res

    def bind_order(self):
        """无配件收货"""
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
                "userName": self.g["user_name"],
                "userId": self.g["loginUserId"]
            }
        }
        res = self.wms_client.do_post(self.wms_path, body)
        if res:
            err_str = res["_data"]["_errStr"]
            if err_str == "success":
                text = "物流单号【{}】的测试结果为：{}<br /><hr />".format(self.g["logisticsNumber"], err_str)
                self.mark_text += text
                self.logger.info(text)
            res_final = self.result_creator("无配件收货", res)
            return res_final
        else:
            return res


if __name__ == '__main__':
    wms = WmsClient()
    sf = "SF1030345882516"
    wms.get_auth()
    try:
        wms.sign(sf)
        wms.unpack(sf)
        wms.receive_search(sf)
        wms.get_order_product()
        wms.get_product_code()
        wms.bind_order()
    except Exception as e:
        pass
    finally:
        print(wms.mark_text)
