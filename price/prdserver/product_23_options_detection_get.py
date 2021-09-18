#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 23.根据检测细化项ID查询问题答案项 - http://wiki.huishoubao.com/index.php?s=/105&page_id=3855

    1-对应服务：server-base_product（base_product）  |  2-对应URL：http://prdserver.huishoubao.com

    入参：detectionId：检测细化项id，以#号分割，例如 12#89#76
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def options_detection_get(detectionId):
    param = {"_head":{"_interface":"options_detection_get","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"123","_invokeId":"111","_callerServiceId":"112002","_groupNo":"1"},"_param":{"detectionId":detectionId}}

    secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
    callerserviceid = "112002"
    url = "http://prdserver.huishoubao.com/product/options_detection_get"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    '''业务入口：估价系统后台 - 选项库 - 问题项 - 查看问题项详情 - 查看答案项详情 '''
    # options_detection_get(detectionId='')
    # options_detection_get(detectionId='243')
    # options_detection_get(detectionId='11111111111')
    options_detection_get(detectionId='243#244#245')
    # options_detection_get(detectionId='355#354')
    # options_detection_get(detectionId='')
    # options_detection_get(detectionId='auto_test')