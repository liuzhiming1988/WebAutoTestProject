#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 5-可估价产品最高最低价获取  -  http://wiki.huishoubao.com/index.php?s=/105&page_id=1594
    1-对应服务：server-base_product（base_product） | 2-对应URL http://prdserver.huishoubao.com

    list：要查询的产品id数组 该数组大小限制在100个以内，超出按数组下标取前100个返回
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test, hsb_response_print

def eva_price_get(channel_id, pid, list):
    param = { "_head":{ "_interface":"eva_price_get", "_msgType":"request", "_remark":"hello", "_version":"0.01", "_timestamps":"123", "_invokeId":"111", "_callerServiceId":"112002", "_groupNo":"1"}, "_param":{"channel_id":channel_id, "pid":pid, "list":list }}

    secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
    callerserviceid = "112002"
    url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
    md5value = json.dumps(param) + "_" + secret_key
    headers = { "Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid }
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    eva_price_get(channel_id="40000001", pid="", list=["30834","30748","30749"])
    # eva_price_get(channel_id="", pid="20201014", list=["41567"])
    # eva_price_get(channel_id="20201014", pid="", list=["41567"])
    # eva_price_get(channel_id="40000001", pid="", list=["20201014"])
    # eva_price_get(channel_id="40000001", pid="", list=["41567", "63330"])
    # eva_price_get(channel_id="10000255", pid="", list=["41567"])
    # eva_price_get(channel_id="", pid="1001", list=["41567"])
    # eva_price_get(channel_id="10000255", pid="", list=["41567", "63330"])
    # eva_price_get(channel_id="", pid="", list=["41567", "63330"])
