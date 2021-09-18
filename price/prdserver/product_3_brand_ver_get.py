#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang



''' 产品服务 - 3-获取品牌列表 - http://wiki.huishoubao.com/index.php?s=/105&page_id=1592

    1-产品中心服务：product_center
    2-对应服务：server-base_product（base_product）
    3-对应URL http://prdserver.huishoubao.com

    fkeys:关键字；可以是品牌id或名称 可为空;   fversions:2代表估价2.0版本品牌信息;
    fvalid:“1”:启用 “0”:”禁用”;   fpageindex:起始页面（从0开始）;  fpagesize:每页数量，（最大限额500
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def brand_ver_get(fkeys, fvalid, fpageindex, fpagesize):
    param = {"_head":{"_interface":"brand_ver_get","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"1439261904","_invokeId":"SALE15216018033998","_callerServiceId":"112002","_groupNo":"1"},"_param":{"fkeys":fkeys, "fvalid":fvalid, "fpageindex":fpageindex, "fpagesize":fpagesize, "fversions":"2"}}

    secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
    callerserviceid = "112002"
    url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # brand_ver_get(fkeys='苹果', fvalid='', fpageindex='0', fpagesize='100')
    brand_ver_get(fkeys='222', fvalid='',  fpageindex='0', fpagesize='100')
    # brand_ver_get(fkeys='苹果', fvalid='',  fpageindex='0', fpagesize='100')
    # brand_ver_get(fkeys='苹果', fvalid='1',  fpageindex='0', fpagesize='100')
    # brand_ver_get(fkeys='我是随便的一个搜索关键字', fvalid='',  fpageindex='0', fpagesize='100')