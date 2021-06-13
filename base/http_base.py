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

class HttpBase:

    def __init__(self):
        self.HEADERS = None
        self.PROTOCOL = None
        self.DOMAIN = None
        self.PORT = None
        self.METHOD = None
        self.PATH = None
        self.BODY = None


    def do_post(self):
        pass

    def do_get(self):
        requests.get(self.PROTOCOL+self.DOMAIN+self.PORT+self.PATH)


class HttpException:

    pass


if __name__ == '__main__':
    res = requests.get("http://api.huishoubao.com/v5/HsbTool/env").text
    print(res)