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


class DetectionClient:

    def __init__(self):
        self.logger = Logger().logger
        self.detection_client = HttpBase()
        self.detection_client.headers = HEADERS_JSON
        self.detection_client.protocol = PROTOCAL_DETECTION
        self.detection_client.domain = DOMAIN_DETECTION
        self.times = str(int(time.time()))
        # 定义接口返回字典格式，各接口使用时可deep copy后再进行赋值
        self.result = {
            "test_result": "success",  # 测试结果：success or fail
            "mark_text": "",        # 提示语
            "raw_data": ""  # 原始响应信息
        }
        # 定义一个字典，来接收临时变量
        self.g = {}

    def get_auth(self):
        """从amc系统获取loginToken，userId，userName信息"""
        ac = AmcClient()
        auth_info = ac.login()    # login()返回的是一个字典
        self.g = dict(self.g, **auth_info)
        info = ac.get_user_info(self.g["loginToken"], self.g["loginUserId"])
        self.g = dict(self.g, **info)

    def get_detect_info(self, bar_code):
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
                "user_id": self.g["loginUserId"],
                "userId": self.g["loginUserId"],
                "login_token": self.g["loginToken"]
            }
        }
        res = self.detection_client.do_post(path, body)
        res_final = self.result_creator("获取条码的检测信息", res)
        if res_final:
            self.g = dict(self.g, ** res)
        return res_final

    def clear_option(self, bar_code=None):
        if bar_code is None:
            bar_code = self.g["seriesNum"]

        if isinstance(bar_code, str):
            pass
        else:
            return False
        path = "/addClearOption"
        body = {
            "_head": {
                "_interface": path
            },
            "_param": {
                "seriesNum": bar_code,
                "optionId": "26",
                "optionName": "已清除",
                "user_id": self.g["loginUserId"],
                "userId": self.g["loginUserId"],
                "login_token": self.g["loginToken"],
                "userName": self.g["email"]
            }
        }

        res = self.detection_client.do_post(path, body)

        res_final = self.result_creator("检测后进行清除", res)
        return res_final

    def result_creator(self, name, res):
        if res:
            result = copy.deepcopy(self.result)
            result["raw_data"] = res
            err_str = res["_data"]["_errStr"]
            err_code = res["_data"]["_errCode"]
            if err_code == "0":
                result["mark_text"] = "{}:条码【{}】，{}".format(name, series_num, err_str)
            else:
                result["mark_text"] = "{}:条码【{}】，{}".format(name, series_num, err_str)
                result["test_result"] = "fail"
            result = json.dumps(result, indent=5, ensure_ascii=False)
            return result
        else:
            return False




if __name__ == '__main__':
    series_num = "ZY0101210708000027"
    detection = DetectionClient()
    detection.get_auth()
    info = detection.get_detect_info(series_num)
    detection.clear_option(series_num)
    print(info)
