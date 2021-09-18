#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 10.可估价产品产品选项获取  - http://wiki.huishoubao.com/index.php?s=/105&page_id=1595
    1. 对应服务：server-base_product（base_product）

    第一步：拿用户估价选项（举例：B端帮卖估价 41567； 可以去2C估价里找41567，找到其选项作为传参【正好可以用此接口）
    B端帮卖，前端，机型估价选项获取（17项）  ①可以传渠道id：10000254（2C）； ②可以传平台 1
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test

def eva_option_get(channel_id, product_id, pid, platform_type):
    param = { "_head":{ "_interface":"eva_option_get", "_msgType":"request", "_remark":"hello", "_version":"0.01", "_timestamps":"123", "_invokeId":"111", "_callerServiceId":"112002", "_groupNo":"1" },"_param":{ "channel_id":channel_id, "product_id":product_id, "pid":pid,"platform_type":platform_type}}
    secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
    callerserviceid = "112002"
    url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    respone.encoding = respone.apparent_encoding  # 编码设置
    respone_dict = json.loads(respone.text)  # 转成字典
    options_list = respone_dict['_body']['_data']['itemList']

    str_options_list = ''
    str_options_desc = ''
    for info in options_list:
        answerList = info['question']
        index = random.randint(0, len(answerList) - 1)
        str_options_list += '"' + answerList[index]['id'] + '",'
        str_options_desc += '"' + info['name'] + ":" + answerList[index]['name'] + '",'
    str_options_list = str_options_list[:-1]

    # print('接口响应『json』格式数据为：\n', json.dumps(respone_dict, ensure_ascii=False) + '\n')
    print('大质检【用户】估价【sku】+【机况】答案项ID（随机取）：\n', '{' + str_options_list + '}' + '\n')
    print('以上【sku】+以上【机况】选项名称+答案项名称：\n', '{' + str_options_desc[:-1] + '}' + '\n')
    print('接口响应时长：{0} 秒'.format(respone.elapsed.total_seconds()))

if __name__ == '__main__':
    ''' channel_id="" 和 platform_type='1' 传一个即可 '''
    # eva_option_get(channel_id='40000001', product_id='41567', pid='', platform_type='')
    # eva_option_get(channel_id='40000001', product_id='30748', pid='', platform_type='')
    eva_option_get(channel_id='40000001', product_id='54791', pid='', platform_type='')
    # eva_option_get(channel_id='10000164', product_id='63330', pid='', platform_type='')