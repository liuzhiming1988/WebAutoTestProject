#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务- 32.1.帮买根据产品ID获取市场价和帮买价  +  bm_get_product_show_price - http://wiki.huishoubao.com/index.php?s=/105&page_id=6027
    server-bangmai_pro_eva
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def bm_get_product_show_price( pid, productId ):
    param = {"_head":{"_interface":"bm_get_product_show_price","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"","_invokeId":"","_callerServiceId":"110001","_groupNo":"1"},"_param":{ "pid":pid, "productId":productId }}

    secret_key = "c36691ced620bf82ad3fc4642f8a6427"
    callerserviceid = "110001"
    url = "http://bmserver.huishoubao.com/bangmai/bm_get_product_show_price"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # bm_get_product_show_price(pid='', productId='')
    # bm_get_product_show_price(pid='1405', productId='')
    # bm_get_product_show_price(pid='111111111111', productId='')
    # bm_get_product_show_price(pid='', productId='23007')
    # bm_get_product_show_price(pid='1405', productId='111111111')
    # bm_get_product_show_price(pid='1405', productId='41567')
    bm_get_product_show_price(pid='1001', productId='41567#54791#63330#60430')

'''
测试
select Fproduct_id, Fmarket_price, Fhelp_buying_price, Fvisible from t_bangmai_product tbp where tbp.Fvisible=1 and tbp.Fproduct_id in (41567);
'''