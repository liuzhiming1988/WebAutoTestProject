#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 31.帮买根据产品ID获取SKU信息 - http://wiki.huishoubao.com/index.php?s=/105&page_id=6026
    server-bangmai_pro_eva
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def bm_get_product_sku(pid, productId):
    param = {"_head":{"_interface":"bm_get_product_sku","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"","_invokeId":"","_callerServiceId":"110001","_groupNo":"1"},"_param":{"pid":pid,"productId":productId}}
    secret_key = "c36691ced620bf82ad3fc4642f8a6427"
    callerserviceid = "110001"
    url = "http://bmserver.huishoubao.com/bangmai/bm_get_product_sku"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # bm_get_product_sku(pid='', productId='')
    # bm_get_product_sku(pid='', productId='38201')
    # bm_get_product_sku(pid='1405', productId='')
    # bm_get_product_sku(pid='1001', productId='41567')
    # bm_get_product_sku(pid='11111111111', productId='41567')
    bm_get_product_sku(pid='1405', productId='38201')
    # bm_get_product_sku(pid='1405', productId='11111111111111')

'''
测试
select Fsku_info, Fvisible from t_bangmai_product tbp where tbp.Fproduct_id = 38201;
select t_a.Fid as Faid, t_a.Fname as Faname, t_q.Fid as Fqid, t_q.Fname as Fqname  from t_eva_item_base as t_a, t_eva_item_base as t_q  where t_a.Fpid=t_q.Fid and t_a.Flevel=3 and t_q.Flevel=2 and t_a.Fid in (1083,1114,17,18,36,37,38);
'''