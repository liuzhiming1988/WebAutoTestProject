#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 12.2 热门机型获取  - http://wiki.huishoubao.com/index.php?s=/105&page_id=9961
    base_product
    pageIndex：分页的页码 | pageSize：每页的数量 | 当答案项不存在时,childs 空数组输出
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def producthotget(pid, channel_id, classId):
    param = {"_head":{"_interface":"producthotget","_msgType":"request","_remark":"hello","_version":"0.01","_timestamps":"123","_invokeId":"111","_callerServiceId":"112002","_groupNo":"1"},"_param":{"pid":pid,"channelId":channel_id,"classId":classId,"pageIndex":"1","pageSize":"100"}}

    secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
    callerserviceid = "112002"
    url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # producthotget(pid='', channel_id='', classId='1')
    # producthotget(pid='101', channel_id='', classId='1')
    # producthotget(pid='', channel_id='10000346', classId='1')
    # producthotget(pid='2052', channel_id='10000346', classId='1')
    # producthotget(pid='2052', channel_id='10000346', classId='')
    producthotget(pid='2052', channel_id='10000346', classId='2')
    producthotget(pid='2052', channel_id='10000346', classId='3')
    # producthotget(pid='0', channel_id='10000121', classId='1')
    # producthotget(pid='0', channel_id='10000016', classId='1')
    # producthotget(pid='2052', channel_id='10000346', classId='1')
    # 自有-VIVO&回收宝合作   channel_id='10000121'   63823	vivo iQOO Neo 855竞速版