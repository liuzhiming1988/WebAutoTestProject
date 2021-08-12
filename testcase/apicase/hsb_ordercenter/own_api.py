#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : own_api.py
@Author  : liuzhiming
@Time    : 2021/6/3 16:10
"""
import requests
import time
from utils.common import *
import random
from urllib3 import encode_multipart_formdata
from utils.pmysql import Pmysql
import pytest
import time
import json
from base.own_api_base import OwnApiBase


class OwnApi(OwnApiBase):

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

    def get_headers(self, boundary):
        headers = {"Content-Type": "multipart/form-data; boundary={0}".format(boundary)}
        return headers

    def get_login_smscode(self, phone):
        path = self.domain + "/apicase/user/getCode"
        data = {
            "tel": phone,
            "token": ""
        }
        # 将公共参数合并进来
        data = dict(data, **self.get_common_args())
        # 获取签名后的参数
        data = get_signData(data)
        bd = self.boundary
        # 将参数转换成encode_multipart_formdata对应的格式
        data_res = encode_multipart_formdata(data,boundary=bd)
        response = requests.post(path, data=data_res[0], headers=self.get_headers(bd))
        # 美化返回的json
        info = self.json_format(response.json())
        print("接口{0}的返回结果是\n{1}".format(path,info))
        assert "成功" in response.text
        # 强制等待两秒钟，待数据库生成短信验证码
        time.sleep(2)
        sql = "SELECT s.content FROM hjxpushdb.sms_log_202106 s WHERE s.phone = {0} ORDER BY s.update_time DESC limit 1".format(phone)
        text = Pmysql().execute_sql(sql)
        # 从短信内容中获取验证码
        smsCode = text[0][0].split("验证码是")[1][:6]
        # print("获取到的验证码是：{0}".format(smsCode))
        return smsCode

    @timer
    def own_login(self, phone, sms_code="auto"):
        """"""
        if sms_code == "auto":
            sms_code = self.get_login_smscode(phone)
        path = self.domain + "/apicase/user/login"
        data = {
            "code": sms_code,
            "loginType": "2",
            "tel": phone,
            "token": ""
        }
        data = dict(data, **self.get_common_args())
        data = get_signData(data)
        bd = self.boundary
        data_res = encode_multipart_formdata(data, boundary=bd)
        response = requests.post(path, data=data_res[0], headers=self.get_headers(bd))
        info = self.json_format(response.json())
        print("接口{0}的返回结果是\n{1}".format(path, info))
        token = json.loads(response.text)["_data"]["token"]
        return token


if __name__ == '__main__':
    oa = OwnApi()
    oa.own_login("13049368516")
    # import yaml
    # path = "D:\\work\\WebAutoTestProject\\testcase\\apicase\\hsb_ordercenter\\ownApi.yaml"
    # logintoken={"loginToken": token}
    # with open(path, "w", encoding="utf-8") as f:
    #     yaml.dump(logintoken, f)
    # with open(path, "r", encoding="utf-8") as f:
    #     print(yaml.safe_load(f)["token"])






