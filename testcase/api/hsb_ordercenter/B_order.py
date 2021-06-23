#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
@File    : B_order.py
@Author  : liuzhiming
@Time    : 2021/6/2 15:11
"""
import hashlib
import time
import requests
import json
import pprint
from concurrent.futures import ThreadPoolExecutor
import random
from pprint import PrettyPrinter
from collections import OrderedDict
from urllib3 import encode_multipart_formdata


def md5_encrypt(str):
    m = hashlib.md5()
    m.update(str.encode("utf-8"))
    return m.hexdigest()


class OrderCenter:
    def __init__(self):
        self.msgType = "request"
        self.timestamps = str(int(time.time()))
        self.secret_key = "ohHmcePiHr2hkXIeBlvleHyfuuSkPP2h"
        self.url = "http://bangmai.order.huishoubao.com"
        self.server_id = "112002"
        self.invokeId = "saleApiFront15836365228184"

    def B_placeBusinessOrder(self, deviceNumber):
        '''B端帮卖精准下单'''
        data = {
            "_head": {
                "_interface": "placeBusinessOrder",
                "_msgType": self.msgType,
                "_remark": "【测试】选择比努力重要",
                "_version": "0.01",
                "_timestamps": self.timestamps,
                "_invokeId": self.invokeId,
                "_callerServiceId": self.server_id,
                "_groupNo": "1"
            },
            "_param": {
                "channelInfo": {
                    "pid": "1660",
                    "destPid": "1660",
                    "channelId": "10000253"
                },
                "recycleInfo": {
                    "businessAttribute": "1",
                    "deliveryMode": "1",
                    "paymentMode": "1",
                    "businessType": "1"
                },
                "goodInfo": {
                    "evaluateId": "200435704",
                    "productId": "41567"
                },
                "accountInfo": {
                    "accountType": "9",
                    "account": "oqQel5BU3ycM3Tbg5MVNp-by02d0",
                    "wechatOpenId": "oqQel5BU3ycM3Tbg5MVNp-by02d0"
                },
                "sendMsgFlag": "0",
                "publishType": "2",
                "userId": "602793866",
                "userTel": "13049368516",
                "deviceNumber": str(deviceNumber),
                "referencePrice": "71300",
                "merchantId": "6744",
                "merchantName": "清风"
            }
        }

        ShujuData = json.dumps(data) + "_" + self.secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8",
                   "HSB-OPENAPI-SIGNATURE": md5_encrypt(ShujuData),
                   "HSB-OPENAPI-CALLERSERVICEID": self.server_id}
        url = self.url + "/bangMai/placeBusinessOrder"
        print(url)
        respone = requests.post(url, data=json.dumps(data), headers=headers)
        requests.post(url, data=json.dumps(data), headers={'Connection':'close'})
        print((respone.content).decode("utf-8"))
        return respone.json()


if __name__ == "__main__":
    # oc = OrderCenter()
    # oc.B_placeBusinessOrder("qingfeng_test20210602")

    pa = {
            "addrId":"1",
            "address": "科技南路9号",
            "areaCode": "440305",
            "areaName": "南山区",
            "cityName": "深圳市",
            "houseNumber": "8",
            "isDefault": "1",
            "landmark": "金地威新软件科技园2期",
            "latitude": "22.528",
            "longitude": "113.949",
            "pid": "1260",
            "platform": "7",
            "provinceName": "广东省",
            "tel":"13049368516",
            "timestamp": "1622702714",
            "token": "0a8d6f342ba872d25ae008a65fd1ff55",
            "uid": "602809804",
            "userName": "留学生",
            "uuid": "28887EA52156419080B8B873FF258772",
            "version": "4007002",
            "versionName": "15"
    }
    # "sign": "619d956dfc8e88704f7fe2d7b7a4ca966d46e3c0",
    # m = encode_multipart_formdata(pa,boundary="Boundary+30F6D62471EF7480")
    # HEARDERS = {"Content-Type": "multipart/form-data; boundary=Boundary+30F6D62471EF7480"}
    # url = "https://api.huishoubao.com/V1/optimize/modAddress"
    # response = requests.post(url,data=m[0],headers=HEARDERS)
    # print(response.request.body)
    # print(response.text)

