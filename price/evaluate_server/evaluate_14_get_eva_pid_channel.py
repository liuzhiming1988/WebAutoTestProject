#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 估价服务 - 14-判断是否是估价2.0的Pid或渠道接口 - http://wiki.huishoubao.com/index.php?s=/138&page_id=2808
    入参：pid：pid  |  channelId：渠道ID（当前只有pid，渠道ID请赋值为空””）
    出参：evaFlags：估价2.0标记，1-代表使用估价2.0，0-代表不是使用估价2.0
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def get_eva_pid_channel(pid,channelId):
    param = {"_head":{"_interface":"get_eva_pid_channel","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"1525332832","_invokeId":"SALESDETECT152533283241636","_callerServiceId":"212013","_groupNo":"1"},"_param":{"pid":pid,"channelId":channelId}}

    secret_key = "CtN4bZr7qYyxygRyP5T0VWMEvWhpH0uf"
    callerserviceid = "212013"
    # eva_query 估价查询服务
    url = "http://evaserver.huishoubao.com/eva_query/get_eva_pid_channel"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # get_eva_pid_channel(pid='',channelId='')
    # get_eva_pid_channel(pid='202104281435',channelId='')
    # get_eva_pid_channel(pid='',channelId='40000001')
    # get_eva_pid_channel(pid='1001',channelId='40000001')
    get_eva_pid_channel(pid='1234',channelId='40000001')
    get_eva_pid_channel(pid='1234',channelId='1234')