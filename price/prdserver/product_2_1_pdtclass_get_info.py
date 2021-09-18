#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 2.获取类目列表 -  http://wiki.huishoubao.com/index.php?s=/105&page_id=1591

    1-产品中心服务：product_center
    2-对应服务：server-base_product（base_product）
    3-对应URL http://prdserver.huishoubao.com
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print
from price.dingdingTalk_push_demo import dingdingTalk_push_run

def pdtclass_get_info(fvalid, fkeys, fpageindex, fpagesize):
    param = {"_head":{"_interface":"pdtclass_get_info","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"123","_invokeId":"111","_callerServiceId":"112002","_groupNo":"1"},"_param":{"fvalid":fvalid,"fkeys":fkeys,"fpageindex":fpageindex,"fpagesize":fpagesize}}

    secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
    callerserviceid = "112002"
    url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)
    dingdingTalk_push_run(msg='您调用的是『HSB-价格FT-测试环境』，HOSTS指向IP为：『{0}』\n\n 接口响应『json』格式数据：\n{1} 接口响应时长：{2}秒'.format(
        hsb_eva_ipProxy_test()['http'], respone.text, respone.elapsed.total_seconds()), is_at_all=False,at_mobiles=["13423814297"])

if __name__ == '__main__':
    pdtclass_get_info(fvalid="1", fkeys="", fpageindex="0", fpagesize="10")
    # pdtclass_get_info(fvalid="1", fkeys="", fpageindex="0", fpagesize="10")
    # pdtclass_get_info(fvalid="1", fkeys="手机", fpageindex="0", fpagesize="10")
    # pdtclass_get_info(fvalid="1", fkeys="笔记本", fpageindex="0", fpagesize="10")
    # pdtclass_get_info(fvalid="1", fkeys="我是随便的一个搜索关键字", fpageindex="0", fpagesize="100")
