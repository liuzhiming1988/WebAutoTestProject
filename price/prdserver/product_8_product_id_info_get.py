#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 8.获取产品详情 - http://wiki.huishoubao.com/index.php?s=/105&page_id=1597
    1-对应服务：server-base_product（base_product） |  2-对应URL http://prdserver.huishoubao.com

    入参：fproduct_id：（必填）产品id(多个产品用#号分隔)  |  fchannel_id：（非必填）渠道id,非必选项,没有时将不返回最高,最低价
        platformType：（非必填）平台id,非必选项 |   ip：（非必填）用户公网访问IP，例如：10.0.10.62
        evaFlag：（非必填）获取可估价标记，0或1，非必选项 填写渠道id或平台id后再填写该字段有效，优先使用渠道id再使用平台id, 没有时将不返回是否可估价标记
        ignoreMaxPrice：是否忽略最高价，1-忽略最高价  20210810增加字段
    出参：fproduct_desc：产品描述（已不维护，请不要使用）  |  fbrand_id：品牌id（1.0品牌）
        fbrand_id_v2：品牌id （2.0品牌）  |  fbrand_name：品牌名称
        fclass_id：类目id  |  fclass_name：类目名称  |  fkey_word：关键词
        fos_type_id：系统id，1-iOS，2-Android，3-Mac OS，4-Windows，5-其他
        fos_type_name：系统名称  |  fproduct_id：产品id  |  fproduct_logo：图片名称  |  fproduct_name：产品名称
        frecycle_type_id：回收类型id  |  frecycle_type_name：回收类型  |  fvalid：是否有效，1-有效，2-无效，产品库的上下架，不是估价的上下架
        sum_num：搜索数量  |  fmarket_time：上市时间
        fmax_price：最高价  |  fmin_price：最低价  |  evaFlag：可估价标记，1-可估价，0-不可估价
'''

import hashlib, requests, json, os, pprint
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def product_id_info_get(evaFlag, fproduct_id,fchannel_id,ignoreMaxPrice):
    param = {"_head":{"_interface":"product_id_info_get","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"123","_invokeId":"eva_vpc_k8s_zhangjinfa","_callerServiceId":"112002","_groupNo":"1"},"_param":{"evaFlag":evaFlag,"fproduct_id":fproduct_id,"fchannel_id":fchannel_id, "ignoreMaxPrice":ignoreMaxPrice}}

    secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
    callerserviceid = "112002"
    url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)
    # pprint.pprint(respone.json())

if __name__ == '__main__':
    # product_id_info_get(evaFlag='',fproduct_id='41567#63000#63330#60430',fchannel_id='40000001')
    # product_id_info_get(evaFlag='1',fproduct_id='52238',fchannel_id='10000121')
    # product_id_info_get(evaFlag='',fproduct_id='52238',fchannel_id='')
    # product_id_info_get(evaFlag='',fproduct_id='30831#41567',fchannel_id='')
    # product_id_info_get(evaFlag='0',fproduct_id='30831#41567',fchannel_id='')
    # product_id_info_get(evaFlag='1',fproduct_id='30831#41567',fchannel_id='')
    # product_id_info_get(evaFlag='',fproduct_id='30831#41567',fchannel_id='40000001')
    # product_id_info_get(evaFlag='0',fproduct_id='30831#41567',fchannel_id='40000001')
    # product_id_info_get(evaFlag='2',fproduct_id='30831#41567',fchannel_id='40000001')

    '''1. 不传 ignoreMaxPrice 字段'''
    # product_id_info_get(evaFlag='',fproduct_id='41567',fchannel_id='40000001') #会返回最高价

    '''2. 传 ignoreMaxPrice 字段'''
    # product_id_info_get(evaFlag='', fproduct_id='41567', fchannel_id='40000001',ignoreMaxPrice='') #ignoreMaxPrice传空，会返回最高价
    # product_id_info_get(evaFlag='', fproduct_id='41567', fchannel_id='40000001',ignoreMaxPrice='0') #ignoreMaxPrice传0，会返回最高价
    # product_id_info_get(evaFlag='', fproduct_id='41567', fchannel_id='40000001',ignoreMaxPrice='20210810') #ignoreMaxPrice传其他字符，会返回最高价
    # product_id_info_get(evaFlag='', fproduct_id='41567', fchannel_id='40000001',ignoreMaxPrice='zhangjinfa_20210810') #ignoreMaxPrice传其他字符，会返回最高价
    product_id_info_get(evaFlag='', fproduct_id='41567', fchannel_id='40000001',ignoreMaxPrice='1') #ignoreMaxPrice传正确的1

'''
redis connect info, host=[EVA_REDIS_HOST], port=[6379]
rdscmd=HMGET pdt_basic_info  41567
{"_body":{"_data":{"product_info":[{"fbrand_id":"11","fbrand_id_v2":"2","fbrand_name":"苹果","fclass_id":"1","fclass_name":"手机","fkey_word":"iPhoneX","fmarket_time":"2017-09-13","fmax_price":"211500","fmin_price":"3600","fos_type_id":"1","fos_type_name":"ios系统","fproduct_desc":"","fproduct_id":"41567","fproduct_logo":"41567_20191106154719_960.jpg","fproduct_name":"iPhone X","frecycle_type_id":"3","frecycle_type_name":"正常回收","fvalid":"1"}],"sum_num":"1"},"_ret":"0","_retcode":"0","_retinfo":"成功"},"_head":{"_callerServiceId":"112002","_groupNo":"1","_interface":"product_id_info_get","_invokeId":"eva_vpc_k8s_zhangjinfa","_msgType":"response","_remark":"","_timestamps":"1628566861","_version":"0.01"}}
'''