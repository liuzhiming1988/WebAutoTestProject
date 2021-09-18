#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 42.通过 skuId 或者 barcode 获取spu信息  -  http://wiki.huishoubao.com/index.php?s=/105&page_id=7571
	1. 对应服务 server-base_product（服务器应用名：base_product）
    2. 对应URL http://prdserver.huishoubao.com

    功能入口：价格后台 - 新产品库 - SPU列表 - sku_id/barcode查询
    入参：queryType：（必填）1-通过productId,skuId；2-通过barcode查询 | productId：必传,默认值0,barcode跟productId,skuId二选一
        skuId：必传,默认值0,barcode跟productId,skuId二选一 | barcode：必传,默认值0,barcode跟productId,skuId二选一
    出参：producId：产品ID | productName：产品名称 | productValid：产品状态，1-启用 0-禁用 | classId：类目ID | className：类目名称
        brandId：品牌ID | brandName：品牌名称 | skuId：skuId | skuInfo：json数组,格式见下面请求示例 | skuValid：sku状态，1-启用 0-禁用 | barcode：barcode
'''

import hashlib, requests,json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def get_spusku_info(queryType, productId, skuId, barcode):
    param = {"_head":{"_interface":"get_spusku_info","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"123","_invokeId":"111","_callerServiceId":"112002","_groupNo":"1"},"_param":{"queryType":queryType, "productId":productId, "skuId":skuId, "barcode":barcode}}

    secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
    callerserviceid = "112002"
    url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # 通过productId,skuId，外部调用，传参还是原样 productId='41567', skuId='54591'
    # get_spusku_info(queryType='', productId='', skuId='', barcode='')
    # get_spusku_info(queryType='1', productId='', skuId='', barcode='')
    # get_spusku_info(queryType='1', productId='41567', skuId='', barcode='')
    # get_spusku_info(queryType='1', productId='41567', skuId='41567_11111111111', barcode='')
    # get_spusku_info(queryType='1', productId='41567', skuId='41567_277184', barcode='')
    # get_spusku_info(queryType='3', productId='41567', skuId='41567_277184', barcode='')
    # get_spusku_info(queryType='1', productId='41567', skuId='41567_277184', barcode='111111111')
    # get_spusku_info( queryType='1', productId='1', skuId='167', barcode='0' )

    # 通过productId,skuId，价格后台，价格前端调用传参  productId='41567', skuId='41567_54591'
    # get_spusku_info( queryType='1', productId='41567', skuId='41567_54591', barcode='0')

    # 内外部调用，通过barcode查询  queryType='2'，barcode='202004201615'  场景：barcode不存在，返回SUCCEED正常
    # get_spusku_info( queryType='2', productId='41567', skuId='41567_277184', barcode='' )
    # get_spusku_info( queryType='2', productId='41567', skuId='41567_277184', barcode='111111111111' )
    get_spusku_info( queryType='2', productId='41567', skuId='41567_277184', barcode='202105070001' )

'''
测试
skuid信息可以从 F:\git\python\hsb_project\product_server\product_36_2_FuZhu_spu_sku_option_combination_get.py  获取
'''