#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 12_1.热门类目获取  -  http://wiki.huishoubao.net/index.php?s=/105&page_id=1623
    base_product

    pageIndex：分页的页码 |  pageSize：每页的数量 | 当答案项不存在时,childs 空数组输出
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def classhotget(pid, channel_id):
    param = {"_head":{"_interface":"classhotget","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"1234567980","_invokeId":"111","_callerServiceId":"112002","_groupNo":"123"},"_param":{"pid":pid,"channel_id":channel_id}}

    secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
    callerserviceid = "112002"
    url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    classhotget(pid='1660', channel_id='')
    classhotget(pid='', channel_id='10000305')
    classhotget(pid='', channel_id='')
    classhotget(pid='20210326', channel_id='')
    classhotget(pid='1001', channel_id='10000305')

    ''' 出现，线上ok，但测试环境调用返回异常时，有可能是新增渠道未同步所致，可将线上渠道数据同步至测试环境'''
    # classhotget(pid='1790', channel_id='10000305')    # 同时传 pid 和 channel_id

    # classhotget(pid='1789', channel_id='') # 只传 pid

    # classhotget(pid='', channel_id='10000305') # 只传 channel_id（不支持）