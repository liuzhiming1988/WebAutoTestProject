#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 14.获取估价选项库接口  - http://wiki.huishoubao.com/index.php?s=/105&page_id=2023

    1-对应服务：server-base_product（base_product）  |  2-对应URL：http://prdserver.huishoubao.com

    入参：classId：类目，不同类目有不同的选项库；1-手机，2-笔记本，3-平板，5-智能手表
        platform：估价平台（可为空：空默认全部） 2C-1、2B-2、微回收-3、转转-4、vivo-5、闲鱼验机-6

    pageIndex：分页的页码； pageSize：每页的数量;    当答案项不存在时,childs 空数组输出
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def get_eva_item(classId,platform):
    param = {"_head":{"_interface":"get_eva_item","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"1525332832","_invokeId":"SALESDETECT152533283241636","_callerServiceId":"112002","_groupNo":"1"},"_param":{"classId":classId,"pageIndex":"0","pageSize":"500","platform":platform}}

    secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
    callerserviceid = "112002"
    url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # get_eva_item(classId='', platform='')
    # get_eva_item(classId='1', platform='')
    # get_eva_item(classId='2', platform='')
    # get_eva_item(classId='3', platform='')
    # get_eva_item(classId='1', platform='1')
    # get_eva_item(classId='1', platform='2')
    # get_eva_item(classId='1', platform='10')
    # get_eva_item(classId='1', platform='20210326')
    get_eva_item(classId='20210326', platform='20210326')