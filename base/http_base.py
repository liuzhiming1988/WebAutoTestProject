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
            self.__PORT = value
        else:
            print("Error: 不是dict类型")

    def do_post(self, path, data):
        if self.port is None:
            url = self.protocol + "://" + self.domain + path
        else:
            url = self.protocol + "://" + self.domain + self.port + path
        self.logger.info("Url:{}".format(url))
        self.logger.info("body = {}".format(json.dumps(data)))
        response = requests.post(url, data=json.dumps(data), headers = self.headers)
        self.logger.info("{}---response：{}".format(url,response))
        return response

    def do_get(self, path):
        requests.get(self.protocol+self.domain+self.port+path)


class HttpException:

    pass


if __name__ == '__main__':
    a = HttpBase()
    print(a.headers)
    a.domain = "www.bai.com"
    print(a.domain)
    b = HttpBase()
    print(b.domain)