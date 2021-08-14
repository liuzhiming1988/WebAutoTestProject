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
from urllib.parse import urlencode
from utils.logger import Logger
from utils.common import *
from urllib3 import encode_multipart_formdata
import random


class HttpBase:
    """封装http基础方法"""
    def __init__(self):
        self.__HEADERS = None
        self.__PROTOCOL = None
        self.__DOMAIN = None
        self.__PORT = None
        self.__BOUNDARY = None
        self.logger = Logger().logger

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
        return self.__DOMAIN

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

    # @property
    # def boundary(self):
    #     return self.__BOUNDARY
    #
    # @boundary.setter
    # def boundary(self, value):
    #     if isinstance(value, str):
    #         self.__BOUNDARY = value.lower()
    #     else:
    #         print("Error：类型错误，请输入str类型")

    @timer
    def do_post(self, path, data, headers_=None):
        # response = ""
        if self.port is None:
            url = self.protocol + "://" + self.domain + path
        else:
            url = self.protocol + "://" + self.domain + self.port + path

        if headers_ is None:
            headers_ = self.headers

        if "json" in headers_["Content-Type"]:
            data = json.dumps(data, indent=5)
        elif "multipart" in headers_["Content-Type"]:
            pass
        # elif "urlencoded" in headers_["Content-Type"] or self.headers is None:
        else:
            data = urlencode(data)

        self.logger.info("{}请求信息：\nheaders={}\nbody={}".format(url, headers_, data))

        try:
            response = requests.post(url, data=data, headers=headers_)
        except requests.exceptions.ConnectionError:
            text = "URL:{};域名连接失败，请检查服务域名和端口信息是否正确".format(url)
            self.logger.error(text)
            return False

        if response.status_code == 200:
            if "json" in response.headers["Content-Type"]:
                self.logger.info("{}响应信息：\nheaders={}\nresponse_body={}".format(
                    url, self.json_format(dict(response.headers)), self.json_format(json.loads(response.text))))
                return response.json()
            else:
                try:
                    self.logger.info("{}响应信息：\nheaders={}\nresponse_body={}".format(
                        url, self.json_format(dict(response.headers)), self.json_format(json.loads(response.text))))
                    return response.json()
                except Exception as e:
                    self.logger.warning("尝试以json格式打印返回数据时出错，异常信息：\n{}".format(e))
                    self.logger.info("{}响应信息：\nheaders={}\nresponse_body={}".format(
                        url, response.headers, response.text))
                    return response.text
        else:
            self.logger.error("请求失败，响应内容为：{}".format(response))
            return False

    def do_get(self, path):

        requests.get(self.protocol+self.domain+self.port+path)

    def json_format(self, body):
        """
        格式化json字符串，并显示汉字字符，格式缩进更美观
        :param body:
        :return:
        """
        str = json.dumps(body, sort_keys=True, indent=4, ensure_ascii=False)
        # self.logger.info(str)
        return str


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