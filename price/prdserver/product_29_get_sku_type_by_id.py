#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 29.根据传递的问题项或答案项ID返回所属SKU类别  - http://wiki.huishoubao.com/index.php?s=/105&page_id=5586

    1-对应服务：server-base_product（base_product） |  2-对应URL：http://prdserver.huishoubao.com

    入参：aIdArray：sku答案项数组（与 问题项数组 不能同时为空）
        qIdArray：sku问题项数组（与 答案项数组 不能同时为空）
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def get_sku_type_by_id(aIdArray, qIdArray):
    param = {"_head":{"_interface":"get_sku_type_by_id","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"","_invokeId":"","_callerServiceId":"112002","_groupNo":"1"},"_param":{"aIdArray":aIdArray, "qIdArray":qIdArray}}

    secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
    callerserviceid = "112002"
    url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # get_sku_type_by_id(aIdArray=[], qIdArray=[])
    # get_sku_type_by_id(aIdArray=['12','13','14'], qIdArray=[])
    # get_sku_type_by_id(aIdArray=['12','13','2020'], qIdArray=[])
    # get_sku_type_by_id(aIdArray=['547','548','12'], qIdArray=[])
    # get_sku_type_by_id(aIdArray=[], qIdArray=['7','11','16'])
    # get_sku_type_by_id(aIdArray=[], qIdArray=['503','504','505'])
    get_sku_type_by_id(aIdArray=[], qIdArray=['671','672','673'])