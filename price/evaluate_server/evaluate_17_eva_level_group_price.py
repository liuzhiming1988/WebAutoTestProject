#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 估价服务 - 17-时间段内获取等级价格 - http://wiki.huishoubao.com/index.php?s=/138&page_id=5558
    入参：productId：产品Id  |  platformId：产品平台Id, 统一估计为 “0”  |  beginTime：开始时间, 格式 “2019-02-23 00:00:00”
        endTime：结束时间, 格式 “2019-02-23 00:00:00”  |  levelGroup：等级值  |  skuItemIds：sku选项Id数组
'''

import requests, json, datetime
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def eva_level_group_price(skuItemIds,levelGroup,platformId,productId):
    param = {"head":{"interface":"eva_level_group_price", "msgtype":"request", "remark":"", "version":"0.01" }, "params":{
        "beginTime":datetime.datetime.combine(datetime.date.today() - datetime.timedelta(days=365),datetime.time.min).strftime('%Y-%m-%d %H:%M:%S'),
        "endTime":datetime.datetime.combine(datetime.datetime.now(), datetime.time.max).strftime('%Y-%m-%d %H:%M:%S'),
        "interface":"eva_level_group_price", "skuItemIds":skuItemIds, "levelGroup":levelGroup, "platformId":platformId, "productId":productId, "server":"eva_server", "url":"/rpc/evaluate" } }
    url = "http://evaserver.huishoubao.com/rpc/evaluate"
    headers = {"Content-Type":"application/json"}
    respone = requests.post(url, data=json.dumps(param), headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # skuItemIds 可参考接口43
    eva_level_group_price(skuItemIds=['12', '1083', '1091', '18', '36'],levelGroup='20',platformId='1',productId='41567')
    eva_level_group_price(skuItemIds=['14', '1633', '42', '18', '36'],levelGroup='20',platformId='1',productId='41567')
    eva_level_group_price(skuItemIds=['14', '1633', '42', '18', '36'],levelGroup='60',platformId='1',productId='41567')
    eva_level_group_price(skuItemIds=['14', '1633', '42', '18', '36'],levelGroup='100',platformId='1',productId='41567')
    eva_level_group_price(skuItemIds=['14', '1633', '42', '18', '36'], levelGroup='20', platformId='2',productId='41567')
    eva_level_group_price(skuItemIds=['14', '1633', '42', '18', '36'], levelGroup='80', platformId='1',productId='41567')
    eva_level_group_price(skuItemIds=['14', '1633', '42', '18', '36'], levelGroup='100', platformId='2',productId='41567')