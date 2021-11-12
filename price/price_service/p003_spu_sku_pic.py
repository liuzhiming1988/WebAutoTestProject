#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : p003_spu_sku_pic.py
@Author  : liuzhiming
@Time    : 2021/9/26 14:25
"""

# wiki: http://wiki.huishoubao.com/web/#/138?page_id=16042
# http://prdserver.huishoubao.com/base_product_v3/spu_sku_pic

import requests
import json
from price.hsb_MD5_Enerypt import get_price_headers, res_print
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test, hsb_eva_ipProxy_k8s_test


def v3_spu_sku_pic(product_id, sku_items):
    url = "http://prdserver.huishoubao.com/base_product_v3/spu_sku_pic"
    param = {
                "_head": {
                    "_interface": "spu_sku_pic",
                    "_msgType": "request",
                    "_remark": "",
                    "_version": "0.01",
                    "_timestamps": "1632448718",
                    "_invokeId": "HsbApiAgent16324487181227",
                    "_callerServiceId": "212011",
                    "_groupNo": "1"
                },
                "_param": {
                    "productId": product_id,
                    "skuItem": sku_items
                }
            }
    print("url：{}，请求参数\n{}".format(url, json.dumps(param)))
    res = requests.post(url, json=param, headers=get_price_headers(param), proxies=hsb_eva_ipProxy_test())
    res_print(res, "2")  # 打印输出响应结果，非1数字打印json格式


if __name__ == '__main__':
    v3_spu_sku_pic(product_id="41567", sku_items=["42"])
