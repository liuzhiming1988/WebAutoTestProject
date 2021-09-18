#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 估价服务  -  4-真实估价接口（无运营和补贴） - http://wiki.huishoubao.com/index.php?s=/138&page_id=2214
	1. 对应服务 rpc_evaluate_server（服务器应用名：rpc_evaluate_server）
'''
import requests, json, os
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def evaluatereal(pid, productid, select):
    param = {"head":{"version":"0.01","msgtype":"request","interface":"evaluatereal","remark":""},"params":{"ip":"127.0.0.1","cookies":"123456", "pid":pid, "productid":productid, "select":select, "userid":"1311" }}
    headers = {"Content-Type":"application/json;charset=UTF-8"}
    url = "http://evaserver.huishoubao.com/rpc/evaluate"     # 大质检 /rpc/evaluate
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # evaluatereal(pid='1190', productid='18', select=["36","29","20"])
    # evaluatereal(pid='', productid='41567', select=[])
    # evaluatereal(pid='1001', productid='41567', select=[])
    # evaluatereal(pid='1001', productid='41567', select=["23"])
    evaluatereal(pid='1001', productid='41567', select=["83","61","66","236","59","5530","3242","56","13","1091","7642","6931","38","5535","23","223","1634","21","1078","2171","17","3245"])