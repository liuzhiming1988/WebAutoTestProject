#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : 3_10_recycle_current_evaluate.py
@Author  : liuzhiming
@Time    : 2021/10/20 10:46
"""

import requests
import json
import os
from random import randint
from price.hsb_MD5_Enerypt import get_price_headers, res_print
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test, hsb_response_print
import operator

"""
检测模板获取现网回收价
【wiki】 http://wiki.huishoubao.com/web/#/138?page_id=16163
EvaluateCheckV3

"""


def recycle_current_evaluate(product_id, channel_id, pid, check_type, opts, skus):
    url = "http://codserver.huishoubao.com/detect_v3/recycle_current_evaluate"
    param = {
        "_head": {
            "_interface": "recycle_current_evaluate",
            "_msgType": "request",
            "_remark": "",
            "_version": "0.01",
            "_timestamps": "1525332832",
            "_invokeId": "152533283241636",
            "_callerServiceId": "216002",
            "_groupNo": "1"
        },
        "_param": {
            "productId": product_id,
            "channelId": channel_id,
            "pid": pid,
            "checkType": check_type,
            "optItem": opts,
            "skuItem": skus,
            "userId": "1895",
            "ip": "127.0.0.1",
            "freqLimitType": "0"
        }
    }
    print("请求参数：\n{}".format(json.dumps(param)))
    res = requests.post(url, json=param, headers=get_price_headers(param), proxies=hsb_eva_ipProxy_test())
    res_print(res)  # 打印输出响应结果，非1数字打印json格式

    res = res.json()
    options_list = []  # 估价明细选项
    for item in res["_data"]["_data"]["evaItemList"]:
        aId = item["ansId"]
        options_list.append(aId)

    base_list = []  # 定价选项
    base_defualt_list = []    # 定价选项（默认项标识）
    for item in res["_data"]["_data"]["baseItemList"]:
        aId = item["ansId"]
        base_list.append(aId)
        if item["isDefault"] == "1":
            base_defualt_list.append(aId)

    print("======转换后的估价明细选项为：\n{}\n".format(options_list))
    print("======转换后的定价明细选项（全部）为：\n{}\n".format(base_list))
    print("======转换后的定价明细选项(带默认标识)为：\n{}\n".format(base_defualt_list))



if __name__ == '__main__':

    skus = ['12', '17', '36', '42', '130', '1083', '2236']
    opts = ['9031', '9035', '9042', '9053', '9769', '9086', '9090', '9094', '9098', '9103', '9110', '9112', '9015',
            '9022', '9025', '9056', '9058', '9059', '9065', '9068', '9072', '9074', '9076', '9077', '9080', '9081',
            '7574', '9083', '9088', '9118', '9191']

    recycle_current_evaluate(product_id="41567", channel_id="10000060", pid="1196", check_type="3", opts=opts, skus=skus)

    """
    param='{"_head": {"_interface": "recycle_current_evaluate", "_msgType": "request", "_remark": "", "_version": "0.01", "_timestamps": "1525332832", "_invokeId": "152533283241636", "_callerServiceId": "216002", "_groupNo": "1"}, "_param": {"productId": "41567", "channelId": "10000060", "pid": "1196", "checkType": "1", "optItem": ["9031", "9035", "9042", "9053", "9769", "9086", "9090", "9094", "9098", "9103", "9110", "9112", "9015", "9022", "9025", "9056", "9058", "9059", "9065", "9068", "9072", "9074", "9076", "9077", "9080", "9081", "7574", "9083", "9088", "9118", "9191"], "skuItem": ["12", "17", "36", "42", "130", "1083", "2236"], "userId": "1895", "ip": "127.0.0.1", "freqLimitType": "0"}}'
md5value=`echo -n $param'_rAfnRwyWfh2N9vXVgWwdpJxaXgOCd8af' | md5sum`;
md5value=`echo ${md5value:0:32}`;
curl  -H "HSB-OPENAPI-SIGNATURE:$md5value" -H 'HSB-OPENAPI-CALLERSERVICEID:216002' -d "$param" http://codserver.huishoubao.com/detect_v3/recycle_current_evaluate
    
    """

