#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 估价服务 - 16-时间段内根据机况估价 - http://wiki.huishoubao.com/index.php?s=/138&page_id=5554
    入参：productId	是	字符串	产品Id
platformId	是	字符串	产品平台Id, 统一估计为 “0”
beginTime	是	字符串	开始时间, 格式 “2019-02-23 00:00:00”
endTime	是	字符串	结束时间, 格式 “2019-02-23 00:00:00”
option	是	数组	选项Id数组
'''

import requests, json, datetime
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def eva_period(option,platformId,productId):
    param = {"head":{"interface":"eva_period","msgtype":"request","remark":"","version":"0.01"},"params":{
        "beginTime":datetime.datetime.combine(datetime.date.today() - datetime.timedelta(days=365),datetime.time.min).strftime('%Y-%m-%d %H:%M:%S'),
        "endTime":datetime.datetime.combine(datetime.datetime.now(), datetime.time.max).strftime('%Y-%m-%d %H:%M:%S'),
        "interface":"eva_period","option":option,"platformId":platformId,"productId":productId,"server":"eva_server","url":"/rpc/evaluate"}}
    url = "http://evaserver.huishoubao.com/rpc/evaluate"
    headers = {"Content-Type":"application/json"}
    respone = requests.post(url, data=json.dumps(param), headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    eva_period(productId='4006',option=["23"],platformId='1')
    eva_period(productId='4006',option=["23","24","25","2021"],platformId='1')
    eva_period(productId='4006',option=["2021"],platformId='1')
    eva_period(productId='4006',option='',platformId='1')
    eva_period(productId='4006',option=["23"],platformId='2')
    eva_period(productId='4006',option=["23"],platformId='10')
    eva_period(productId='4006',option='',platformId='')
    eva_period(productId='',option='',platformId='')