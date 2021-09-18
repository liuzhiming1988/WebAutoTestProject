#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 30.帮买产品列表获取 - http://wiki.huishoubao.net/index.php?s=/105&page_id=6025  -  server-bangmai_pro_eva
    入参：pid	：必传 pid  |  classId：类目ID  |  brandId：品牌ID
keyword	否	string	关键字
    # pageIndex：分页的页码；   pageSize：每页的数量
    # 1、当答案项不存在时,childs 空数组输出
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def bm_search_product_list(pid, classId, brandId, keyword):
    param = {"_head":{"_interface":"bm_search_product_list","_msgType":"request","_remark":"hello","_version":"0.01","_timestamps":"123","_invokeId":"111","_callerServiceId":"110001","_groupNo":"1"},"_param":{"pid":pid,"classId":classId,"brandId":brandId,"keyword":keyword,"pageIndex":"0","pageSize":"10"}}

    secret_key = "c36691ced620bf82ad3fc4642f8a6427"
    callerserviceid = "110001"
    url = "http://bmserver.huishoubao.com/bangmai/bm_search_product_list"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # bm_search_product_list(pid='', classId='', brandId='', keyword='')
    # bm_search_product_list(pid='1405', classId='', brandId='', keyword='')
    # bm_search_product_list(pid='1001', classId='', brandId='', keyword='')
    # bm_search_product_list(pid='111111111111', classId='', brandId='', keyword='')
    # bm_search_product_list(pid='1405', classId='1', brandId='', keyword='')
    # bm_search_product_list(pid='1405', classId='1', brandId='2', keyword='')
    bm_search_product_list(pid='1405', classId='1', brandId='2', keyword='iPhone x')