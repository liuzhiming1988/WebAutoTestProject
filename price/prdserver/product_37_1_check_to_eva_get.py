#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 37.2.标准检测选项映射估价选项搜索接口 - http://wiki.huishoubao.com/index.php?s=/105&page_id=6762

    1-检测映射服务（wiki项目：产品服务）：eva_detect
    2-对应服务：server-evaluate_detect（服务器应用名：server-evaluate_detect）
    3-对应URL http://codserver.huishoubao.com

    "checkAnswerId":"91#675#31"
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def check_to_eva_get(checkAnswerId):
    param = {"_head":{"_interface":"check_to_eva_get","_msgType":"request","_remark":"hello","_version":"0.01","_timestamps":"123","_invokeId":"111","_callerServiceId":"112006","_groupNo":"1"},"_param":{"checkAnswerId":checkAnswerId}}

    secret_key = "gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU"
    callerserviceid = "112006"
    url = "http://codserver.huishoubao.com/detect/check_to_eva_get"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # check_to_eva_get(checkAnswerId='')
    # check_to_eva_get(checkAnswerId='1')
    # check_to_eva_get(checkAnswerId='1111111111')
    # check_to_eva_get(checkAnswerId='91')
    # check_to_eva_get(checkAnswerId='91#675#31')
    # check_to_eva_get(checkAnswerId='91#675#11111111111111')
    check_to_eva_get(checkAnswerId='91#675#a111111')
    check_to_eva_get(checkAnswerId='000000')