#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 10.获取所有的回收类型 - http://wiki.huishoubao.com/index.php?s=/105&page_id=1599

    1-对应服务：server-base_product（base_product）  |  2-对应URL：http://prdserver.huishoubao.com
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def pdt2_conf():
    param = {"_head":{"_interface":"pdt2_conf","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"123","_invokeId":"111","_callerServiceId":"112002","_groupNo":"1"},"_param":{"cmd":"021"}}

    secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
    callerserviceid = "112002"
    url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    pdt2_conf()