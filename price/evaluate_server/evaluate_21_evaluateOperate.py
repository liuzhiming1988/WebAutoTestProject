#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 估价服务 - 21.运营估价接口 - http://wiki.huishoubao.com/web/#/138?page_id=11997

    入参：cookies：用户浏览器使用的cookies （必填） | pid：回收宝对外入口ID （必填） | channelid：渠道ID（渠道ID赋值：代表使用2B估价模型） （有pid时可为空）（必填）
        productid：估价产品ID（必填） | userid：登录用户ID（未登录用户可为空）（必填） | isBottomPrice：是否获取保底价,1是,默认为否 （非必填）
        operPrice：估价模型价格 （必填） | standPrice：标准价 （必填）
    出参：quotation：估算价格 单位:分 | bottomPrice：保底价/起拍价,单位为分,isBottomPrice不为1时,返回空, isBottomPrice为1时 存在
'''

import requests, json, time
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_baseprice_ipProxy_test, hsb_baseprice_ipProxy_dev, hsb_response_print

''' 运营估价接口 '''
def evaluateOperate(channelid, operPrice, pid, productid, standPrice):
    param = {"head":{"interface":"evaluateOperate","msgtype":"request","remark":"","version":"0.01"},"params":{"channelid":channelid,"cookies":"server-evaluate_detect-1596074817","ip":"127.0.0.1", "isBottomPrice":"1", "operPrice":operPrice, "pid":pid, "productid":productid, "standPrice":standPrice,"userid":"0"}}
    url = "http://evaserver.huishoubao.com/rpc/evaluate"
    headers = {"Content-Type": "application/json;charset=UTF-8"}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_baseprice_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # 请求方：server-evaluate_detect、server-bangmai_pro_eva    响应方：rpc_evaluate_server
    # evaluateOperate(channelid='', operPrice='317500', pid='', productid='60292', standPrice='218000')
    # evaluateOperate(channelid='10000254', operPrice='317500', pid='', productid='60292', standPrice='218000')
    # evaluateOperate(channelid='', operPrice='317500', pid='11012', productid='60292', standPrice='218000')
    # evaluateOperate(channelid='10000254', operPrice='317500', pid='1001', productid='60292', standPrice='218000')
    evaluateOperate(channelid='111111111111', operPrice='317500', pid='11012', productid='60292', standPrice='218000')

'''
【运营估价记录】: 
用户id: 0
用户ip: 127.0.0.1
产品id: 60292
渠道id: 10000254
PID: 
运营价: 317500
基准价: 218000
最终价格:317500
渠道加成价格:0
渠道加成版本: 
保底价格:327500
outdata={"body":{"data":{"bottomPrice":"327500","chanAddPrice":"0","chanAddVersion":"","quotation":"317500"},"ret":"0","retcode":"0","retinfo":"成功"},"head":{"interface":"evaluateOperate","msgtype":"response","remark":"","version":"0.01"}}
'''