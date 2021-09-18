#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 估价服务 - 6-估价最高价接口（渠道加成、渠道分成价格） - http://wiki.huishoubao.net/index.php?s=/138&page_id=2216
	1. 对应服务 rpc_evaluate_server（服务器应用名：rpc_evaluate_server）

	channelid：渠道ID  |  platformid：平台ID  |  productid：产品ID
'''

import requests, json, os
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def eva_max_price(channelid, platformid, productid):
    param = {"head":{ "interface":"eva_max_price", "msgtype":"request", "remark":"", "version":"0.01"}, "params":{"channelid":channelid, "platformid":platformid, "productid":productid}}
    url = "http://evaserver.huishoubao.com/rpc/evaluate"
    headers = {"Content-Type":"application/json;charset=UTF-8"}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    eva_max_price(channelid="", platformid='1', productid="41567")
    eva_max_price(channelid="40000001", platformid='', productid="41567")
    eva_max_price(channelid="40000001", platformid='1', productid="41567")
    eva_max_price(channelid="40000001", platformid='2', productid="41567")
    eva_max_price(channelid="40000001", platformid='10', productid="41567")
    eva_max_price(channelid="40000001", platformid='20210326', productid="41567")
    eva_max_price(channelid="20210326", platformid='1', productid="41567")
    eva_max_price(channelid="20210326", platformid='20210326', productid="41567")