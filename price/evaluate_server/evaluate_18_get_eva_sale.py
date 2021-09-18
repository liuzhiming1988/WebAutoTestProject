#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 估价服务 - 18.帮卖用户估价（定价） - http://wiki.huishoubao.com/index.php?s=/138&page_id=9626  '''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def get_eva_sale( channelId, productId, select ):
    param = {"_head":{"_interface":"get_eva_sale","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"1525332832","_invokeId":"SALESDETECT152533283241636","_callerServiceId":"110025","_groupNo":"1"},"_param":{"cookies":"1111","ip":"127.0.0.1","pid":"1001","channelId":channelId, "productId":productId, "select":select, "userId":"o"}}
    secret_key = "5157c30f296407311b0a0b0194803340"
    callerserviceid = "110025"
    url = "http://bmserver.huishoubao.com/bangmai/get_eva_sale"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    get_eva_sale(channelId="10000254", productId="41567", select=["12","17","38","42","1083","63","77","73","71","83","223","65","59","55","2171","3246","1078","23","20"])