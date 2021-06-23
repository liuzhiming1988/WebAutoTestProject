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
        self.HEADERS = None
        self.PROTOCOL = None
        self.DOMAIN = None
        self.PORT = None
        self.METHOD = None
        self.PATH = None
        self.BODY = None

    def do_post(self, path, data):
        if self.PORT is None:
            url = self.PROTOCOL + "://" + self.DOMAIN + path
        else:
            url = self.PROTOCOL + "://" + self.DOMAIN + self.PORT + path
        self.logger.info("Url:{}".format(url))
        self.logger.info("body = {}".format(json.dumps(data)))
        response = requests.post(url, data=json.dumps(data), headers = self.HEADERS)
        self.logger.info("{}---response：{}".format(url,response))
        return response

    def do_get(self):
        requests.get(self.PROTOCOL+self.DOMAIN+self.PORT+self.PATH)


class HttpException:

    pass


if __name__ == '__main__':
    HttpBase().do_post()