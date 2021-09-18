#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 27.产品SKU基础信息分类拉取- http://wiki.huishoubao.com/index.php?s=/105&page_id=5563

    1-对应服务：server-base_product（base_product）  |  2-对应URL：http://prdserver.huishoubao.com
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print
from price.dingdingTalk_push_demo import dingdingTalk_push_run

def get_sku_list(skuType, pageIndex, pageSize, keyword, valid):
    param = {"_head":{"_interface":"get_sku_list","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"","_invokeId":"","_callerServiceId":"112002","_groupNo":"1"},"_param":{"skuType":skuType, "pageIndex":pageIndex, "pageSize":pageSize, "keyword":keyword, "valid":valid}}

    secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
    callerserviceid = "112002"
    url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)
    # dingdingTalk_push_run(msg='接口响应『json』格式数据：\n{0} 接口响应时长：{1}秒'.format(respone.text, respone.elapsed.total_seconds()), is_at_all=False, at_mobiles=["13423814297"])

if __name__ == '__main__':
    # get_sku_list(skuType='101',pageIndex='0',pageSize='500',keyword='',valid='1') # 手机	101	颜色
    # get_sku_list(skuType='102',pageIndex='0',pageSize='500',keyword='',valid='1') # 手机	102	机身内存
    # get_sku_list(skuType='103',pageIndex='0',pageSize='500',keyword='',valid='1') # 手机	103	型号
    # get_sku_list(skuType='104',pageIndex='0',pageSize='500',keyword='',valid='1') # 手机	104	官换机
    # get_sku_list(skuType='105',pageIndex='0',pageSize='500',keyword='',valid='1') # 手机	105	购买渠道
    # get_sku_list(skuType='106',pageIndex='0',pageSize='500',keyword='',valid='1') # 手机	106	存储容量
    # get_sku_list(skuType='107',pageIndex='0',pageSize='500',keyword='',valid='1') # 手机	107	制式
    get_sku_list(skuType='108',pageIndex='0',pageSize='500',keyword='',valid='1') # 手机	108	保修期

    # get_sku_list(skuType='201',pageIndex='0',pageSize='500',keyword='',valid='1') # 笔记本	201	显卡
    # get_sku_list(skuType='202',pageIndex='0',pageSize='500',keyword='',valid='1') # 笔记本	202	硬盘
    # get_sku_list(skuType='203',pageIndex='0',pageSize='500',keyword='',valid='1') # 笔记本	203	内存
    # get_sku_list(skuType='204',pageIndex='0',pageSize='500',keyword='',valid='1') # 笔记本	204	处理器
    # get_sku_list(skuType='205',pageIndex='0',pageSize='500',keyword='',valid='1') # 笔记本	205	颜色

    # get_sku_list(skuType='301',pageIndex='0',pageSize='500',keyword='',valid='1') # 平板	301	颜色
    # get_sku_list(skuType='302',pageIndex='0',pageSize='500',keyword='',valid='1') # 平板	302	内存
    # get_sku_list(skuType='303',pageIndex='0',pageSize='500',keyword='',valid='1') # 平板	303	官换机
    # get_sku_list(skuType='304',pageIndex='0',pageSize='500',keyword='',valid='1') # 平板	304	购买渠道
    # get_sku_list(skuType='305',pageIndex='0',pageSize='500',keyword='',valid='1') # 平板	305	存储容量
    # get_sku_list(skuType='306',pageIndex='0',pageSize='500',keyword='',valid='1') # 平板	306	保修期
    # get_sku_list(skuType='307',pageIndex='0',pageSize='500',keyword='',valid='1') # 平板	307	网络模式
    # get_sku_list(skuType='308',pageIndex='0',pageSize='500',keyword='',valid='1') # 平板	308	尺寸