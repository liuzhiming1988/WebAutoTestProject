#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : get_balance.py
@Author  : liuzhiming
@Time    : 2021/6/4 11:40
"""

from utils.common import *
from base.own_api_base import HsbApiBase
from urllib3 import encode_multipart_formdata
import requests


class GetBalanceInfo(HsbApiBase):

    def get_balance_info(self, loginToken, uid):
        path = self.domain + "/api/wallet/getBalanceInfo"
        data = {
            "token": loginToken,
            "uid": uid
        }
        data = dict(data, **(self.get_common_args()))
        data = get_signData(data)
        print((self.json_format(data)))
        bd = self.boundary
        data_res = encode_multipart_formdata(data, boundary=bd)
        response = requests.post(path, data=data_res[0], headers=self.get_headers_multipart(bd))
        info = self.json_format(response.json())
        print("接口{0}的返回结果是\n{1}".format(path, info))

