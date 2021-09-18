#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 11.热门品牌获取  - http://wiki.huishoubao.net/index.php?s=/105&page_id=1622

    1-对应服务：server-base_product（base_product）  |  2-对应URL：http://prdserver.huishoubao.com
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def brandhotget(pid, channel_id, classid):
    param = {"_head":{"_interface":"brandhotget", "_msgType":"request", "_remark":"hello", "_version":"0.01", "_timestamps":"123", "_invokeId":"111", "_callerServiceId":"112002", "_groupNo":"1"},"_param":{"pid":pid, "channel_id":channel_id, "classid":classid, "pageindex":"1", "pagesize":"100"}}

    secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
    callerserviceid = "112002"
    url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # brandhotget(pid='', channel_id='',classid='')
    brandhotget(pid='1660', channel_id='',classid='1')
    # brandhotget(pid='0', channel_id='10000060',classid='1')
    # brandhotget(pid='1377', channel_id='',classid='3')
    # brandhotget(pid='auto_test', channel_id='',classid='1')