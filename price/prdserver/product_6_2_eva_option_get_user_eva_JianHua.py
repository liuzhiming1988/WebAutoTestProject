#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 6_1.可估价产品产品选项获取 - http://wiki.huishoubao.com/index.php?s=/105&page_id=1595

    1-对应服务：server-base_product（base_product）  | 2-对应URL http://prdserver.huishoubao.com

    business_id：业务id（1-自有； 和need_default必须同时存在）
    need_default：【控制接口是否走估价简化新加流程】是否需要选项默认值（1：需要，其他不需要； 和business_id必须同时存在）
    {"answerItem":"21,8,82,236,3244,3243,61,3245,52,1077,224,66,58,56,2170", "skuItemDefault":"1"}  skuItemDefault 控制是否返回基本信息默认项
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test

def eva_option_get(channel_id, product_id, pid, business_id, need_default):
    param = { "_head":{ "_interface":"eva_option_get", "_msgType":"request", "_remark":"hello", "_version":"0.01", "_timestamps":"123", "_invokeId":"111", "_callerServiceId":"112002", "_groupNo":"1" },"_param":{ "channel_id":channel_id, "product_id":product_id, "pid":pid, "business_id":business_id, "need_default":need_default }}

    secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
    callerserviceid = "112002"
    url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    # response.encoding：从HTTP header中猜测的响应内容编码方式；
    # response.apparent_encoding：从内容分析出的响应内容的编码方式（备选编码方式）
    respone.encoding = respone.apparent_encoding  # 编码设置
    respone_dict = json.loads(respone.text)  # 转成字典
    print(respone_dict)
    options_list = respone_dict['_body']['_data']['itemList']

    str_options_list = ''
    str_options_desc = ''
    for info in options_list:
        answerList = info['question']
        index = random.randint(0, len(answerList) - 1)
        str_options_list += '"' + answerList[index]['id'] + '",'
        str_options_desc += '"' + info['name'] + ":" + answerList[index]['name'] + '",'
    str_options_list = str_options_list[:-1]

    print('接口响应『json』格式数据为：\n', json.dumps(respone_dict, ensure_ascii=False) + '\n')
    print('大质检【用户】估价【sku】+【机况】答案项ID（随机取）：\n', '{' + str_options_list + '}' + '\n')
    print('以上【sku】+以上【机况】选项名称+答案项名称：\n', '{' + str_options_desc[:-1] + '}' + '\n')
    print('接口响应时长：{0} 秒'.format(respone.elapsed.total_seconds()))

if __name__ == '__main__':
    # "business_id": "1", "need_default": "1"   正常返回(iPhone)
    # 核对：defualtOptionList返回aid，在itemList里，defualtOptionList返回所有的aid，包含在数据库的配置里
    # eva_option_get( channel_id="", product_id="41567", pid="1001", business_id="1", need_default="1" )

    # "business_id":"1", "need_default":"2"    接口不走估价简化新加流程，不返回 defualtOptionList
    # eva_option_get(channel_id="", product_id="63398", pid="1001", business_id="1", need_default="1" )

    # android
    # eva_option_get(channel_id="", product_id="41567", pid="1001", business_id="1", need_default="2" )

    # "business_id":"2" 不存在，defualtOptionList返回空数组
    # eva_option_get(channel_id="", product_id="41567", pid="1001", business_id="20210325", need_default="1" )

    # "business_id":"1", "need_default":""    验证："_retinfo":"business_id和need_default必须同时存在"
    # eva_option_get(channel_id="", product_id="41567", pid="1001", business_id="1", need_default="" )

    # "business_id":"", "need_default":""   均传空
    eva_option_get(channel_id="", product_id="41567", pid="1001", business_id="", need_default="" )

    pass