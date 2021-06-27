#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : http_base.py
@Author  : liuzhiming
@Time    : 2021/6/11 15:04
"""

import requests
import json
from urllib import parse
from utils.logger import Logger
from utils.common import *


class HttpBase:

    logger = Logger().logger

    def __init__(self):
        self.__HEADERS = None
        self.__PROTOCOL = None
        self.__DOMAIN = None
        self.__PORT = None

    @property
    def protocol(self):
        return self.__PROTOCOL

    @protocol.setter
    def protocol(self, value):
        if isinstance(value, str):
            if value.lower() in ["http", "https"]:
                self.__PROTOCOL = value.lower()
            else:
                print("error: 协议错误，只允许输入http或https")
        else:
            print("Error：类型错误，请输入str类型")

    @property
    def domain(self):
        return  self.__DOMAIN

    @domain.setter
    def domain(self, value):
        if isinstance(value, str):
            self.__DOMAIN = value
        else:
            print("Error: 不是str类型")

    @property
    def port(self):
        return self.__PORT

    @port.setter
    def port(self, value):
        if isinstance(value, str):
            self.__PORT = value
        else:
            print("Error: 不是str类型")

    @property
    def headers(self):
        return self.__HEADERS

    @headers.setter
    def headers(self, value):
        if isinstance(value, dict):
            self.__HEADERS = value
        else:
            print("Error: 不是dict类型")

    @timer
    def do_post(self, path, data):
        if self.port is None:
            url = self.protocol + "://" + self.domain + path
        else:
            url = self.protocol + "://" + self.domain + self.port + path

        self.logger.info("{}请求信息：\nheaders={}\nbody={}".format(url,self.headers,self.json_format(data)))

        response = requests.post(url, data=json.dumps(data), headers = self.headers)
        self.logger.info("{}响应信息：\nheaders={}\nresponse_body={}".format(
            url, self.json_format(dict(response.headers)), self.json_format(json.loads(response.text))))

        # self.logger.info(self.json_format(response.headers))
        return response

    def do_get(self, path):
        requests.get(self.protocol+self.domain+self.port+path)

    @staticmethod
    def json_format(body):
        """
        格式化json字符串，并显示汉字字符，格式缩进更美观
        :param body:
        :return:
        """
        return json.dumps(body, sort_keys=True, indent=2, ensure_ascii=False)


class HttpException:

    pass


if __name__ == '__main__':
    pro_client = HttpBase()
    path = "/hsbpro"

    data = {
  "_head": {
    "_appVersion": "5.0.0",
    "_callerServiceId": "111111",
    "_groupNo": "1",
    "_interface": "get_merchant_info",
    "_invokeId": "iOS_C6E0E068-F2F5-4FE2-934C-BD39CB2DF5E2_1624618031",
    "_msgType": "request",
    "_remark": "",
    "_timestamps": "1624618031",
    "_version": "0.01",
    "channelStr": "appstore",
    "latitude": 22.53245630905639,
    "longitude": 113.94294365618332
  },
  "_param": {
    "login_token": "4512751100206992728bcfb5e6d8f458",
    "merchantId": "220395845",
    "permissions": "0",
    "queryType": "tagInfo"
  }
}
    pro_client.headers = {
            "Content-Type":  "application/x-www-form-urlencoded; charset=utf-8"
        }

    pro_client.protocol = "https"
    pro_client.domain = "hsbpro.huishoubao.com"
    pro_client.do_post(path, data)
    # dict_h = pro_client.headers
    # print(type(dict_h))