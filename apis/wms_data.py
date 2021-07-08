#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : wms_data.py
@Author  : liuzhiming
@Time    : 2021/7/8 14:25
"""
import json
import requests


url  = """http://wms-wwwapi.huishoubao.com.cn/admin/handle"""
headers = {'Content-Type': 'application/json;charset=UTF-8'}
body={
  "_head": {
    "_interface": "PlatWms.Parcel.BindOrder",
    "_msgType": "request",
    "_remark": "",
    "_timestamps": "1625735553",
    "_version": "0.01"
  },
  "_param": {
    "depotId": "1",
    "loginToken": "8495e3b8fd6bcfbda8115ded3a308190",
    "loginUserId": "1930",
    "logisticsNum": "SF1334448372757",
    "num": "1",
    "orderChannelId": "10000060",
    "orderChannelType": "1",
    "orderId": "7634420",
    "orderPhone": "MTg2NzY3MDIxNTI=",
    "orderSn": "210708126000008",
    "orderSystemId": "1",
    "orderSystemType": "1",
    "orderWeb": "回收宝APP-2C",
    "parcelId": "11235",
    "partsCode": "",
    "partsInfo": "",
    "productInfo": "[{\"productId\": \"5517661\", \"productCode\": \"ZY0101210708000021\", \"classId\": \"01\", \"brand\": \"苹果\", \"model\": \"iPhone 6\", \"imei\": \"\"}]",
    "receiveType": "1",
    "userId": "1930",
    "userName": "刘志明_TEST"
  }
}
body = json.dumps(body)
res = requests.post(url,body,headers=headers)
print(res.text)