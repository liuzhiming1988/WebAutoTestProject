#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : idle_fish_api.py
@Author  : liuzhiming
@Time    : 2021/8/27 11:16
"""


import requests
import json
import hashlib
from utils.logger import Logger


class FishApi:
    """
    闲鱼已验货无忧购API
    """

    def __init__(self):
        self.KEY = "55b7e99624d212b70c0125461a0d2a30"
        self.SERVICE_ID = "100001"
        self.OS = requests.session()
        self.DOMAIN = "http://xianyu-yiyanhuo-api.hsb.com"
        self.logger = Logger().logger

    @staticmethod
    def get_md5(str):
        """
        接收一个字符串，返回md5值
        :param str:
        :return:
        """
        sign = hashlib.md5()
        sign.update(str.encode("UTF-8"))
        return sign.hexdigest()

    def get_headers(self, param):
        data = json.dumps(param)
        data = data + "_" + self.KEY
        headers = {"Content-Type": "application/json;charset=UTF-8",
                   "HSB-OPENAPI-SIGNATURE": self.get_md5(data),
                   "HSB-OPENAPI-CALLERSERVICEID": self.SERVICE_ID}
        return headers

    def _post(self, url="", param=None):
        headers = self.get_headers(param)
        data = json.dumps(param)
        if "http://" in url:
            pass
        else:
            url = self.DOMAIN + url

        if param is None:
            return "参数不能为空！！！"
        try:
            self.logger.debug("【Start Send Request url】:\n{}".format(url))
            self.logger.debug("【Request Headers】：\n{}".format(headers))
            self.logger.debug("【Request Body】:\n{}".format(json.dumps(param,indent=5,ensure_ascii=False)))
            res = self.OS.post(url, data=data, headers=headers)
            print(res.text)
            res.encoding = res.apparent_encoding
            res = json.dumps(res.json(), indent=4, ensure_ascii=False)
            self.logger.debug("【{}】Response Body:\n{}".format(url, res))
            self.logger.debug("【End The Request】：{}".format(url))
        except Exception as e:
            res = e
        return res


if __name__ == '__main__':
    fish = FishApi()
    para =  {
    "_head": {
        "_interface": "XianYuYiYanHuo.Api.V1.logisticsProgress",
        "_msgType": "request",
        "_remark": "",
        "_version": "0.01",
        "_timestamps": "1439261904",
        "_invokeId": "563447634257324435",
        "_callerServiceId": "210015",
        "_groupNo": "1"
    },
    "_param": {
        "deliveryId": "1",
        "merchantId": "6721",
        "returnId": "1"
    }
}
    fish._post(param=para)
