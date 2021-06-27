#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : own_api_base.py
@Author  : liuzhiming
@Time    : 2021/6/3 20:02
"""
import random
import time
import hashlib
import json
from urllib3 import encode_multipart_formdata
from urllib import parse
import requests
from base.http_base import HttpBase


class OwnApiBase(HttpBase):

    def __init__(self):
        super().__init__()
        self.domain = "https://api.huishoubao.com"
        self.pid = "1260"
        self.platform = "7"
        self.timestamp = str(int(time.time()))
        self.version = "4007002"
        self.versionName = "15"
        self.uuid = "28887EA52156419080B8B873FF258772"
        self.boundary = "Boundary+30F6D62471EF{0}".format(random.randint(1000,9999))
        self.headers_urlencoded = {
            "Content-Type":  "application/x-www-form-urlencoded; charset=utf-8"
        },
        self.headers_json = {
            "Content-Type": "application/json; charset=utf-8"
        }
        self.own_signKey = 'b7cab12b2b81385dd2cccb8ce67e4998'

    def md5_encrypt(self, str):
        m = hashlib.md5()
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    def get_common_args(self):
        common_args = {
            "pid": self.pid,
            "platform": self.platform,
            "timestamp": self.timestamp,
            "uuid": self.uuid,
            "version": self.version,
            "versionName": self.versionName
        }
        return common_args

    def get_headers_multipart(self, boundary):
        headers = {"Content-Type": "multipart/form-data; boundary={0}".format(boundary)}
        return headers

    def get_headers_json(self, body, secret_key="ohHmcePiHr2hkXIeBlvleHyfuuSkPP2h", server_id="112002"):
        """
        获取公共头部
        :param body: 传入参数字典
        :param secret_key:
        :param server_id:
        :return:
        """
        data = json.dumps(body) + "_" + secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8",
                   "HSB-OPENAPI-SIGNATURE": self.md5_encrypt(data),
                   "HSB-OPENAPI-CALLERSERVICEID": server_id}
        return headers

    def get_signData(self, data):
        """
        回收宝自有sign规则，将所有的参数名进行排序，然后按照参数名+参数值进行拼接，最后拼接上key值，再进行sha1加密（utf-8编码），再hexdigest加密
        :param data: 传入一个字典，不包含签名
        :return:
        签名
        """

        str1 = ""
        # 将传入的字典进行排序并拼接
        for i in sorted(data):
            # print(i)
            str1 += i + data[i]
        # 拼接上key
        str1 += self.own_signKey
        # 进行加密
        s = hashlib.sha1()
        s.update(str1.encode("utf-8"))
        sign = s.hexdigest()
        data["sign"] = sign
        return data


