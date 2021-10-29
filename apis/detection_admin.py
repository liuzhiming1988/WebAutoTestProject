#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : detection_admin.py
@Author  : liuzhiming
@Time    : 2021/7/9 14:11
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
from utils import common


class DetectionClient:

    def __init__(self):
        self.logger = Logger().logger
        self.detection_client = HttpBase()
        self.detection_client.headers = HEADERS_JSON
        self.detection_client.protocol = PROTOCAL_DETECTION
        self.detection_client.domain = DOMAIN_DETECTION
        self.times = str(int(time.time()))
        self.time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 定义接口返回字典格式，各接口使用时可deep copy后再进行赋值
        self.result = {
            "test_result": "success",  # 测试结果：success or fail
            "mark_text": "",        # 提示语
            "raw_data": ""  # 原始响应信息
        }
        # 定义一个字典，来接收临时变量
        self.temp = {}
        self.mark = True
        self.mark_text = ""

    def get_auth(self):
        """从amc系统获取loginToken，userId，userName信息"""
        ac = AmcClient()
        auth_info = ac.login()    # login()返回的是一个字典
        self.temp = dict(self.temp, **auth_info)
        info = ac.get_user_info(self.temp["loginToken"], self.temp["loginUserId"])
        self.temp = dict(self.temp, **info)

    def result_creator(self, name, res):
        """构造测试结果"""
        if res:
            result = copy.deepcopy(self.result)
            result["raw_data"] = res
            err_str = res["_data"]["_errStr"]
            err_code = res["_data"]["_errCode"]
            if err_code == "0":
                result["mark_text"] = "{}:{}".format(name, err_str)
            else:
                result["mark_text"] = "{}:{}".format(name, err_str)
                result["test_result"] = "fail"
                self.mark = False
            result = json.dumps(result, indent=5, ensure_ascii=False)
            return result
        else:
            return False

    @staticmethod
    def get_options_select(options):
        """从获取的检测项中获取选中项参数"""
        select_ids = []   # 选中的id列表

        for option in options:
            y = len(option["item"])
            option_list = option["item"]
            del option_list[1:y]
            item_son = option_list[0]
            del item_son["item"]
            del item_son["singleFlag"]
            value = option["item"][0]["id"]
            select_ids.append(value)

        return options, select_ids

    @staticmethod
    def get_sku_list(detect_select):
        """从sku列表中随机选中7项"""
        sku_list = detect_select[3:10]
        print("获取到的sku_list为：{}".format(sku_list))
        return sku_list

    def get_detect_info(self, bar_code):
        """获取条码的检测模板信息"""
        if isinstance(bar_code, str):
            pass
        else:
            return False
        path = "/getDetectInfo"
        body = {
            "_head": {
                "_interface": path
            },
            "_param": {
                "seriesNum": bar_code,
                "detType": 0,
                "user_id": self.temp["loginUserId"],
                "userId": self.temp["loginUserId"],
                "login_token": self.temp["loginToken"]
            }
        }
        res = self.detection_client.do_post(path, body)
        res_final = self.result_creator("获取条码的检测信息", res)
        result_text = res["_data"]["_errStr"]

        if result_text == "success":
            self.temp = dict(self.temp, ** res["_data"]["_data"])
        else:
            pass
        return res_final

    def search_product(self, name=None):
        if name is None:
            name = self.temp["productId"]
        path = "/getNoEvaProCommon"
        body = {
            "_head": {
                "_interface": "getNoEvaProCommon"
            },
            "_param": {
                "keyword": name,
                "channelId": self.temp["channelId"],
                "classId": "",
                "user_id": self.temp["loginUserId"],
                "userId": self.temp["loginUserId"],
                "login_token": self.temp["loginToken"]
            }
        }
        res = self.detection_client.do_post(path, body)
        res_final = self.result_creator("查询机型", res)
        if res_final:
            self.temp = dict(self.temp, ** res["_data"]["_data"])
        return res_final

    def get_detect_option(self):
        """获取检测模板选项信息-新标准检测"""
        path = "/getDetectOptionTmp"
        body = {
            "_head": {
                "_interface": path
            },
            "_param": {
                "partnerCode": self.temp["partnerCode"],
                "productId": self.temp["productId"],
                "classId": self.temp["classId"],
                "orderId": self.temp["orderId"],
                "detTpl": 2,
                "channelId": self.temp["channelId"],
                "isOverInsurance": 0,
                "user_id": self.temp["loginUserId"],
                "userId": self.temp["loginUserId"],
                "login_token": self.temp["loginToken"]
            }
        }
        res = self.detection_client.do_post(path, body)
        res_final = self.result_creator("获取检测选项", res)
        if res_final:
            self.temp = common.merge_dict(self.temp, res["_data"]["_data"])
        return res_final

    def get_product_evaluate(self, options, sku_list):
        "获取估价ID"
        path = "/productEvaluate"
        body = {
            "_head": {
                "_interface": "productEvaluate"
            },
            "_param": {
                "aIdList": "",
                "channelId": self.temp["channelId"],
                "cIdList": "",
                "detTpl": self.temp["detTpl"],
                "engineerOptions": options,
                "isOverInsurance": "0",
                "login_token": self.temp["loginToken"],
                "optionList": [],
                "orderId": self.temp["orderId"],
                "partnerCode": self.temp["partnerCode"],
                "productId": self.temp["productId"],
                "seriesNum": self.temp["seriesNum"],
                "skuList": sku_list,
                "user_id": self.temp["loginUserId"],
                "userId": self.temp["loginUserId"]
            }
        }
        res = self.detection_client.do_post(path, body)
        err_code = res["_data"]["_errCode"]
        if err_code == "0":
            res_final = self.result_creator("获取估价ID", res)
            self.temp = dict(self.temp, ** res["_data"]["_data"])
        else:
            self.mark = False
            self.mark_text = res["_data"]["_errStr"]


    def get_sku_id(self, sku_list):
        """获取sku id"""
        path = "/getSkuId"
        body = {
            "_head": {
                "_interface": path
            },
            "_param": {
                "login_token": self.temp["loginToken"],
                "productId": self.temp["productId"],
                "skuList": sku_list,
                "user_id": self.temp["loginUserId"],
                "userId": self.temp["loginUserId"]
            }
        }
        res = self.detection_client.do_post(path, body)
        res_final = self.result_creator("获取sku id", res)
        if res_final:
            self.temp = dict(self.temp, ** res["_data"]["_data"])
        return res_final

    def get_warehouse_type(self, select_detect_ids):
        """获取商品上架标签"""
        path = "/GetWarehouseType"
        body = {
            "_head": {
                "_interface": path
            },
            "_param": {
                "brandId": self.temp["fbrand_id"],
                "classId": self.temp["classId"],
                "detectPrice": self.temp["detectPrice"][:-2],
                "detectTpl": "2",
                "login_token": self.temp["loginToken"],
                "productId": self.temp["productId"],
                "detectSelect": select_detect_ids,
                "user_id": self.temp["loginUserId"],
                "userId": self.temp["loginUserId"]
            }
        }
        res = self.detection_client.do_post(path, body)
        res_final = self.result_creator("获取上架标签warehouse_type", res)
        if res_final:
            self.temp = common.merge_dict(self.temp, res["_data"]["_data"])
        return res_final

    def get_level(self, detect_select):
        """获取销售等级"""
        path = "/getGoodsLevelInfo"
        body = {
            "_head": {
                "_interface": path
            },
            "_param": {
                "channelId": self.temp["channelId"],
                "cIdList": [],
                "detTpl": 2,
                "orderId": self.temp["orderId"],
                "partnerCode": self.temp["partnerCode"],
                "login_token": self.temp["loginToken"],
                "productId": self.temp["productId"],
                "aIdList": detect_select,
                "user_id": self.temp["loginUserId"],
                "userId": self.temp["loginUserId"]
            }
        }
        res = self.detection_client.do_post(path, body)
        res_final = self.result_creator("获取销售等级level info", res)
        if res_final:
            self.temp = common.merge_dict(self.temp, res["_data"]["_data"])
        return res_final

    def add_detect_info(self, det_ids, detect_options, select_id_list, sku_li):
        """提交检测结果"""
        path = "/addDetectInfo"
        body = {
            "_head": {
                "_interface": "PlatXianyuDetect.Detect.addDetectInfo"
            },
            "_param": {
                "brandId": self.temp["fbrand_id"],
                "brandName": self.temp["fbrand_name"],
                "classId": self.temp["fclass_id"],
                "className": self.temp["fclass_name"],
                "productId": self.temp["fproduct_id"],
                "productLogo": self.temp["fproduct_logo"],
                "productName": self.temp["fproduct_name"],
                "systemId": 1,
                "detTpl": 2,
                "detOrderType": self.temp["detOrderType"],
                "channelFlag": self.temp["channelFlag"],
                "channelName": self.temp["channelName"],
                "channelId": self.temp["channelId"],
                "detSource": self.temp["detSource"],
                "srcPid": self.temp["srcPid"],
                "seriesNum": self.temp["seriesNum"],
                "detectInfoId": self.temp["detectInfoId"],
                "orderNum": self.temp["orderNum"],
                "orderId": self.temp["orderId"],
                "detCode": "",
                "recordId": "",
                "grade": "",
                "imei": self.temp["imei"],
                "productSn": "",
                "detectIsPass": "0",
                "detIds": det_ids,
                "detIds2": [],
                "detNormIds": select_id_list,
                "detEvaluateSnapshot": [],
                "detEvaluateSnapshot2": [],
                "detectOptions": detect_options,
                "evaluateId": self.temp["evaluateId"],
                "detectPrice": self.temp["detectPrice"],
                "recyclePrice": self.temp["recyclePrice"],
                "sellPriceMax": self.temp["sellPriceMax"],
                "adjustPrice": self.temp["adjustPrice"],
                "skuId": self.temp["skuId"],
                "verdict": "",
                "osVersion": "",
                "allegeResult": "",
                "startTime": self.time_str,
                "endTime": self.time_str,
                "warehouseLabel": self.temp["warehouseType"],
                "detType": self.temp["detType"],
                "partnerCode": self.temp["partnerCode"],
                "goodsLevel": {
                    "level": self.temp.get("level","Null"),
                    "levelName": self.temp["levelName"],
                    "levelDesc": self.temp["levelDesc"],
                    "levelLabel": self.temp["levelLabel"]
                },
                "chargedStatus": "1",
                "chargedCount": "-1",
                "userName": self.temp["email"],
                "realName": self.temp["user_name"],
                "isDisassembly": "0",
                "isPass": "0",
                "skuOptions": sku_li,
                "spotCheckParam": {
                    "byRecordId": "",
                    "spotType": "1",
                    "objectivityErrorSum": 1,
                    "objectivitySum": 37,
                    "subjectivityErrorSum": 0,
                    "subjectivitySum": 14,
                    "subjectivityMustSum": 5,
                    "subjectivityMustErrorSum": 0,
                    "moneyError": -17800
                },
                "user_id": self.temp["loginUserId"],
                "userId": self.temp["loginUserId"],
                "login_token": "9a4e75182f4bd234bbc99ac6ed054afd"
            }
        }
        res = self.detection_client.do_post(path, body)
        res_final = self.result_creator("提交检测结果", res)
        return res_final

    def clear_option(self, bar_code=None):
        if bar_code is None:
            bar_code = self.temp["seriesNum"]

        if isinstance(bar_code, str):
            pass
        else:
            return False
        path = "/addClearOption"
        body = {
            "_head": {
                "_interface": "addClearOption"
            },
            "_param": {
                "seriesNum": bar_code,
                "optionId": "26",
                "optionName": "已清除",
                "user_id": self.temp["loginUserId"],
                "userId": self.temp["loginUserId"],
                "login_token": self.temp["loginToken"],
                "userName": self.temp["email"]
            }
        }
        res = self.detection_client.do_post(path, body)
        res_final = self.result_creator("检测成功，提交清除【已清除】", res)
        return res_final


if __name__ == '__main__':
    series_num = "ZY0101210708000031"
    detection = DetectionClient()
    detection.get_auth()
    # mock, 调试阶段去除每次都要登录
    # detection.temp = {
    #     'loginToken': '9a4e75182f4bd234bbc99ac6ed054afd',
    #     'loginUserId': '1930',
    #     'user_name': '刘志明_TEST',
    #     'email': 'test_liuzhiming@huishoubao.com.cn'
    # }

    test = detection.get_detect_info(series_num)
    print(test)

    # detection.search_product()
    # detection.get_detect_option()
    # # 获取检测选项
    # options = detection.temp["options"]
    # # 获取选中的选项
    # options_select = detection.get_options_select(options)
    # engineer_options = options_select[0]
    # # 获取选中的id列表
    # select_ids = options_select[1]
    # # 获取选中的sku列表，七项
    # sku_list = detection.get_sku_list(select_ids)
    # detection.get_sku_id(sku_list)
    # detection.get_product_evaluate(engineer_options, sku_list)
    # detection.get_level(select_ids)
    # # print(detection.temp["level"])
    # product_info = detection.temp["product_info"]
    # product_id = detection.temp["productId"]
    # for product in product_info:
    #     for i in range(len(product_info)):
    #         fproduct = product_info[i]
    #         fproduct_id = fproduct["fproduct_id"]
    #         if fproduct_id == product_id:
    #             detection.temp = dict(detection.temp, **fproduct)
    #             break
    #         else:
    #             pass
    # detection.get_warehouse_type(select_ids)
    # detIds = []
    # detectEvaluateOptionIds = detection.temp["detectEvaluateOptionIds"]
    # for id_ in detectEvaluateOptionIds:
    #     dict_temp = {
    #         "id": id_,
    #         "mp": []
    #     }
    #     detIds.append(dict_temp)
    #
    # detection.add_detect_info(detIds, engineer_options, select_ids, sku_list)
    # detection.clear_option(series_num)
    # detection.logger.info(json.dumps(detection.temp, indent=6))


    # print(info)
