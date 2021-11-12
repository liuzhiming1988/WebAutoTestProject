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
import random
from utils import IMEI


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

        # 实例化闲鱼小站api client
        self.xzapi = ProApiBase()
        self.xzapi.protocol = "https"
        self.xzapi.domain = "xyxzapi.huishoubao.com"
        self.xzapi.headers = {
            "Content-Type": "application/json; charset=utf-8"
        }

        self.mark_text = ""

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
            self.mark_text = "登录失败，_errCode：{} _errStr：{}".format(res["_data"]["_errCode"], res["_data"]["_errStr"])
            self.logger.warning(self.mark_text)

    def get_merchant_info(self):
        interface = "get_merchant_info"
        param = {
            "merchantId": self.temp["merchant_id"],
            "permissions": "0",
            "login_token": self.temp["login_token"],
            "queryType": "tagInfo"
        }
        res = self.pro_client.pro_post(interface, param)

    def get_login_captcha(self, phone):
        """
        获取登录短信验证码
        :param phone:
        :return:
        """
        interface = "get_login_captcha"
        param = {
            "phone": phone,
            "roleVerify": "0",
            "permissions": "0"
        }
        res = self.pro_client.pro_post(interface, param)

    def pro_get_smsCode(self, phone):
        """
        连接数据库，从数据库中读取短信验证码
        :param phone:
        :return:
        """
        self.get_login_captcha(phone)
        sql = "SELECT s.content FROM hjxpushdb.sms_log_202106 s WHERE s.phone = {0} ORDER BY s.update_time DESC limit 1".format(phone)
        text = Pmysql().execute_sql(sql)
        # 从短信内容中获取验证码
        smsCode = text[0][0].split("验证码为：")[1][:6]
        print("获取到的验证码是：{0}".format(smsCode))
        return smsCode

    def get_message_list(self):
        """
        获取消息列表
        :param phone:
        :return:
        """
        interface = "get_message_list"
        param = {
            "pageSize": "20",
            "permissions": "0",
            "pageIndex": "0"
        }
        res = self.pro_client.pro_post(interface, param)

    def get_store_list(self):
        interface = "get_store_list"
        param = {
            "pageSize": "10",
            "productType": "0",
            "userId": self.temp["channel_user_id"],
            "roleId": self.temp["roleList"][0],
            "permissions": "0",
            "pageIndex": "0",
            "login_token": self.temp["login_token"]
        }
        res = self.xzapi.xz_post(interface, param)
        store_info = res["_data"]["data"]["storeList"][0]  # 取第一条store信息
        print(store_info)
        self.temp = merge_dict(self.temp, store_info)



    def detect_v3_get_sn(self):
        """
        获取sn号
        :return:
        """
        order_num = "merchant_onum_" + \
                    self.temp["channel_user_id"] + "_" + self.pro_client.timestamp+str(random.randint(100, 999))
        self.temp["order_num"] = order_num
        interface = "detect_v3_get_sn"
        param = {
            "orderNum": order_num,
            "clerkId": self.temp["channel_user_id"],
            "permissions": "0",
            "detectMark": "1",
            "login_token": self.temp["login_token"],
            "version": "4"
        }
        res = self.pro_client.pro_post(interface, param)
        self.temp = merge_dict(self.temp, res["_data"]["data"])

    def get_check_option(self, brand_id="2", product_id="38200"):
        """
        获取所有检测选项
        :param brand_id:
        :param product_id:
        :return:
        """
        interface = "get_check_option"
        param = {
            "sn": self.temp["sn"],
            "brandId": brand_id,
            "permissions": "0",
            "productId": product_id,
            "login_token": self.temp["login_token"]
        }
        res = self.pro_client.pro_post(interface, param)
        self.temp = merge_dict(self.temp, res["_data"]["data"])

    def get_basic_selects(self):
        """
        step=1
        :return:
        """
        items = self.temp["basic"]["items"]
        for item in items:
            del item["singleFlag"]
            answers = item["answers"]
            del answers[1:]
            answer = answers[0]
            del answer["isForbid"]
            del answer["markType"]
        self.temp["basic_selects"] = items
        return items

    def get_condition_selects(self):
        """
        step=2
        :return:
        """
        items = self.temp["condition"]["items"]
        for item in items:
            del item["singleFlag"]
            del item["isMultiple"]
            answers = item["answers"]
            del answers[1:]
            answer = answers[0]
            del answer["isForbid"]
        self.temp["condition_selects"] = items
        return items

    def get_function_selects(self):
        """
        step=3
        :return:
        """
        items = self.temp["function"]["items"]
        del items[-1]
        for item in items:
            del item["singleFlag"]
            del item["isMultiple"]
            answers = item["answers"]
            del answers[1:]
            answer = answers[0]
            del answer["isForbid"]
        # print(json.dumps(items, indent=5, ensure_ascii=False))
        self.temp["function_selects"] = items
        return items

    def get_repair_selects(self):
        """
        step=4获取维修情况选项，默认选中第一项
        :return:
        """
        items = self.temp["repair"]["items"]
        for item in items:
            del item["isMultiple"]
            del item["singleFlag"]
            answers = item["answers"]
            del answers[1:]
            answer = answers[0]
            del answer["isForbid"]
        # print(json.dumps(items, indent=5, ensure_ascii=False))
        self.temp["repair_selects"] = items
        return items

    def save_update_check_result(self, check_item, step):
        """
        提交用户选中检测选项
        :param check_item: 选中项
        :param step: 步骤，1、basic 2、condition 3、function 4、repair
        :return:
        """
        if isinstance(step, int):
            step = str(step)
        interface = "save_update_check_result"
        param = {
            "sn": self.temp["sn"],
            "checkItem": check_item,
            "permissions": "0",
            "step": step,
            "login_token": self.temp["login_token"]
        }
        res = self.pro_client.pro_post(interface, param)

    def product_evaluate_merchant_check(self):
        interface = "product_evaluate_merchant_check"
        param = {
            "sn": self.temp["sn"],
            "type": "1",
            "permissions": "0",
            "userId": self.temp["channel_user_id"],
            "login_token": self.temp["login_token"]
        }
        res = self.pro_client.pro_post(interface, param)
        self.temp = merge_dict(self.temp, res["_data"]["data"])

    def get_photo_template(self):
        interface = "get_photo_template"
        param = {
            "sn": self.temp["sn"],
            "permissions": "0",
            "login_token": self.temp["login_token"]
        }
        res = self.pro_client.pro_post(interface, param)

    def get_check_result(self):
        interface = "get_check_result"
        param = {
            "sn": self.temp["sn"],
            "permissions": "0",
            "login_token": self.temp["login_token"]
        }
        res = self.pro_client.pro_post(interface, param)

    def save_photo_merchant_check(self):
        interface = "save_photo_merchant_check"
        param ={
            "sn": self.temp["sn"],
            "permissions": "0",
            "pictures": {
              "repair": [

              ],
              "function": [

              ],
              "realShot": [
                {
                  "positionCode": "positive",
                  "classKey": "key_zm",
                  "uniqueCode": "positive_1",
                  "className": "手机正面",
                  "positionName": "手机正面",
                  "picUrl": "http://s1-1251010403.file.myqcloud.com/xian_yu_x_z/order/order_remark/ios-selfdetection-sn2021071712460494350-positive_1-7271.jpg"
                },
                {
                  "positionCode": "frontBottom",
                  "classKey": "key_zm",
                  "uniqueCode": "frontBottom_1",
                  "className": "手机正面",
                  "positionName": "手机底部",
                  "picUrl": "http://s1-1251010403.file.myqcloud.com/xian_yu_x_z/order/order_remark/ios-selfdetection-sn2021071712460494350-frontBottom_1-12463.jpg"
                },
                {
                  "positionCode": "rightSide",
                  "classKey": "key_zm",
                  "uniqueCode": "rightSide_1",
                  "className": "手机正面",
                  "positionName": "手机右侧",
                  "picUrl": "http://s1-1251010403.file.myqcloud.com/xian_yu_x_z/order/order_remark/ios-selfdetection-sn2021071712460494350-rightSide_1-81484.jpg"
                },
                {
                  "positionCode": "back",
                  "classKey": "key_bm",
                  "uniqueCode": "back_1",
                  "className": "手机背面",
                  "positionName": "手机背面",
                  "picUrl": "http://s1-1251010403.file.myqcloud.com/xian_yu_x_z/order/order_remark/ios-selfdetection-sn2021071712460494350-back_1-99991.jpg"
                },
                {
                  "positionCode": "leftSide",
                  "classKey": "key_zm",
                  "uniqueCode": "leftSide_1",
                  "className": "手机正面",
                  "positionName": "手机左侧",
                  "picUrl" : "http://s1-1251010403.file.myqcloud.com/xian_yu_x_z/order/order_remark/ios-selfdetection-sn2021071712460494350-leftSide_1-27821.jpg"
                },
                {
                  "positionCode": "frontTop",
                  "classKey": "key_zm",
                  "uniqueCode": "frontTop_1",
                  "className": "手机正面",
                  "positionName": "手机顶部",
                  "picUrl": "http://s1-1251010403.file.myqcloud.com/xian_yu_x_z/order/order_remark/ios-selfdetection-sn2021071712460494350-frontTop_1-65548.jpg"
                },
                {
                  "positionCode": "brightScreen",
                  "classKey": "key_zm",
                  "uniqueCode": "brightScreen_1",
                  "className": "手机正面",
                  "positionName": "正面亮屏",
                  "picUrl": "http://s1-1251010403.file.myqcloud.com/xian_yu_x_z/order/order_remark/ios-selfdetection-sn2021071712460494350-brightScreen_1-69933.jpg"
                },
                {
                  "positionCode": "settingPage",
                  "classKey": "key_zm",
                  "uniqueCode": "settingPage_1",
                  "className": "手机正面",
                  "positionName": "设置页",
                  "picUrl": "http://s1-1251010403.file.myqcloud.com/xian_yu_x_z/order/order_remark/ios-selfdetection-sn2021071712460494350-settingPage_1-78520.jpg"
                }
              ]
            },
            "login_token": self.temp["login_token"],
            "userName": self.temp["user_name"]
        }
        res = self.pro_client.pro_post(interface, param)

    def apply_for_create_goods(self, product_id="38200"):
        interface = "apply_for_create_goods"
        imei = IMEI.generate_imei()
        self.temp["IMEI"] = imei
        param = {
            "sn": self.temp["sn"],
            "type": "1",
            "productId": product_id,
            "startPrice": self.temp["referencePrice"],
            "merchantId": self.temp["merchant_id"],
            "imei": imei,
            "storeId": self.temp["storeId"],
            "permissions": "0",
            "userId": self.temp["channel_user_id"],
            "userName": self.temp["phone"],
            "login_token": self.temp["login_token"]
        }
        res = self.pro_client.pro_post(interface, param)
        self.temp = merge_dict(self.temp, res["_data"]["data"])
        try:
            series_num = res["_data"]["data"]["seriesNum"]
            self.mark = True
            self.mark_text = "创建商品成功，商品条码为：【{}】".format(series_num)
        except Exception as e:

            self.mark = False
            self.mark_text = "创建商品失败，错误信息为：【{}】".format(e)


if __name__ == '__main__':
    brand_id = "1"
    product_id = "65783"
    pro = HsbProApi()
    pro.login()
    pro.get_merchant_info()
    # pro.get_login_captcha("13049368516")
    # pro.get_message_list()
    # pro.get_store_list()
    # pro.detect_v3_get_sn()
    # pro.get_check_option(brand_id, product_id)
    # basic_selects = pro.get_basic_selects()
    # condition_selects = pro.get_condition_selects()
    # function_selects = pro.get_function_selects()
    # repair_selects = pro.get_repair_selects()
    # pro.save_update_check_result(basic_selects, 1)
    # pro.save_update_check_result(condition_selects, 2)
    # pro.save_update_check_result(function_selects, 3)
    # pro.save_update_check_result(repair_selects, 4)
    # pro.product_evaluate_merchant_check()
    # pro.get_photo_template()
    # pro.get_check_result()
    # pro.save_photo_merchant_check()
    # pro.apply_for_create_goods(product_id)
    # print(pro.mark_text)
    # print(json.dumps(pro.temp, indent=5, ensure_ascii=False))


