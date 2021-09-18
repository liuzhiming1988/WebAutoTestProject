#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 估价服务-7-估价逆向运算接口 - http://wiki.huishoubao.com/index.php?s=/138&page_id=2217
	1. 对应服务 rpc_evaluate_server（服务器应用名：rpc_evaluate_server）
'''

import requests, json, os
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def evaluatereverse():
    param = {"head":{"version":"0.01","msgtype":"request","interface":"evaluatereverse","remark":""},"params":{"ip":"127.0.0.1","productitems":{},"userid":"12345678","evaprice":"40100","rickguarantee":"0","select":["111","122","132"]}}
    url = "http://evaserver.huishoubao.com/rpc/evaluate"
    headers = {"Content-Type":"application/json;charset=UTF-8"}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    evaluatereverse()