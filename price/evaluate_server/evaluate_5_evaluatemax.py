#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 估价服务 - 5.估价最高价接口  - 【帮卖】配合帮卖进行系统精准估价升级，迭代有使用 - http://wiki.huishoubao.com/web/#/138?page_id=2215
    服务：rpc_evaluate_server

    入参：channelid：渠道ID，10000031（只有平台时可为空），是 | productid：估价产品ID，17，是 | userid：登录用户ID，未登录用户可为空，是
        platformid：平台ID，1-2C、2-2B、3-微回收，是 | maxpricetype：最高价类型ID，1-平台最compare_price_task_result高价、2-渠道最高价，3-统一估计，4-用户估价，是
        pdtSkuMap：获取SKU组合的最高价，key-sku问题项ID、value-sku答案项ID，否 | evaItem：选择的估价选项，key-sku问题项ID、value-sku答案项ID，否
'''

import requests,json
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def evaluatemax(maxpricetype, channelid, platformid, productid):
    param = {"head":{"interface":"evaluatemax","msgtype":"request","remark":"","version":"0.01"},"params":{"channelid":channelid,"ip":"127.0.0.1","maxpricetype":maxpricetype, "platformid":platformid,"productid":productid,"userid":"1311"}}
    url = "http://evaserver.huishoubao.com/rpc/evaluate"
    headers = {"Content-Type":"application/json"}
    respone = requests.post(url, data=json.dumps(param), headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    ''' 1. 平台最高价（备注：渠道ID和平台ID至少传一个（优先取平台ID属性）） '''
    evaluatemax(maxpricetype='4', channelid="10000255", platformid='10', productid="41567")
    # evaluatemax(maxpricetype='1', channelid="40000001", platformid='1', productid="38201")
    # evaluatemax(maxpricetype='1', channelid="40000001", platformid='', productid="38201")

    ''' 2. 渠道最高价，开启了差值调价，有穷举价格（备注：渠道ID必传，平台ID可传可不传（不影响结果）） '''
    # evaluatemax(maxpricetype='2', channelid="40000001", platformid='', productid="38201")
    # evaluatemax(maxpricetype='2', channelid="40000001", platformid='1', productid="38201")

    ''' 3. 统一估价最高价（渠道ID和平台ID至少传一个（至于传哪个，都不影响结果）） '''
    # evaluatemax(maxpricetype='3', channelid="", platformid='1', productid="38201") # 传平台ID，不传渠道ID
    # evaluatemax(maxpricetype='3', channelid="40000001", platformid='1', productid="38201") # 渠道ID和平台ID同传
    # evaluatemax(maxpricetype='3', channelid="40000001", platformid='', productid="38201") # 传渠道ID，不传平台ID

    ''' 4. 用户估最高价（备注：渠道ID必传，平台ID可传可不传（不影响结果））'''
    # evaluatemax(maxpricetype='4', channelid="40000001", platformid='1', productid="38201") # 渠道ID和平台ID都传
    # evaluatemax(maxpricetype='4', channelid="40000001", platformid='', productid="38201") # 只传渠道ID

''' https://www.yuque.com/mikingzhang/hsb2020/pov83z '''