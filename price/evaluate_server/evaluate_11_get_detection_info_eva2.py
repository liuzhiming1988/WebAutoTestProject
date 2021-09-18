#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 估价服务 - 11.检测系统获取估价2.0选项接口  -  http://wiki.huishoubao.net/index.php?s=/138&page_id=2221
	1.对应服务 rpc_evaluate_server（服务器应用名：rpc_evaluate_server）
'''

import requests, json, os, random
from price.hsb_ipProxy_responsePrint import hsb_eva_admin_ipProxy_test, hsb_response_print

def get_detection_info_eva2(oid, productId, isOverInsurance):
    param = {"head":{"interface":"get_detection_info_eva2","msgtype":"request","remark":"","version":"0.01"},"params":{ "oid":oid, "productId":productId, "isOverInsurance":isOverInsurance }}

    headers = {"Content-Type":"application/json;charset=UTF-8"}
    url = "http://admin.huishoubao.com.cn/detection/get_detection_info_eva2"
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_admin_ipProxy_test())
    respone.encoding = respone.apparent_encoding  # 编码设置
    respone_dict = json.loads(respone.text)  # 转成字典
    print(respone_dict)
    options_list = respone_dict['body']['data']['option_info']

    str_options_list = ''
    str_options_desc = ''
    for info in options_list:
        answerList = info['item']
        index = random.randint(0, len(answerList) - 1)
        str_options_list += '"' + answerList[index]['id'] + '",'
        str_options_desc += '"' + info['name'] + ":" + answerList[index]['name'] + '",'
    str_options_list = str_options_list[:-1]

    print('接口响应『json』格式数据为：\n', json.dumps(respone_dict, ensure_ascii=False) + '\n')
    print('检测系统获取估价2.0【sku】+【机况】答案项ID（随机取）：\n', '{' + str_options_list + '}' + '\n')
    print('以上【sku】+以上【机况】选项名称+答案项名称：\n', '{' + str_options_desc[:-1] + '}' + '\n')
    print('接口响应时长：{0} 秒'.format(respone.elapsed.total_seconds()))

if __name__ == '__main__':
    # get_detection_info_eva2(oid="",productId='',isOverInsurance='')
    # get_detection_info_eva2(oid="7576699",productId='',isOverInsurance='')
    # get_detection_info_eva2(oid="20210327",productId='',isOverInsurance='')
    # get_detection_info_eva2(oid="",productId='20210327',isOverInsurance='')
    # get_detection_info_eva2(oid="7576699",productId='',isOverInsurance='')
    # get_detection_info_eva2(oid="7576699",productId='20210327',isOverInsurance='')
    # get_detection_info_eva2(oid="20210327",productId='23007',isOverInsurance='')
    get_detection_info_eva2(oid="7595261",productId='23007',isOverInsurance='')
    # get_detection_info_eva2(oid="7595261",productId='23007',isOverInsurance='0')
    # get_detection_info_eva2(oid="7595261",productId='23007',isOverInsurance='1')
    # get_detection_info_eva2(oid="7595261",productId='41567',isOverInsurance='0')
    # get_detection_info_eva2(oid="7595261",productId='41567',isOverInsurance='1')

'''
admin.huishoubao.com.cn  域名迁移VPC测试环境
测试环境主机名（通过跳板机，远程连接）
vpc-test-admin01
	HOSTS配置
	10.135.42.251         admin.huishoubao.com.cn
	10.0.40.7             prdserver.huishoubao.com
	10.0.40.7             evaserver.huishoubao.com
	10.0.40.7             codserver.huishoubao.com
	123.207.104.59        atm-mapping.huishoubao.com
	10.135.42.251         evaconfg.huishoubao.com
	10.135.42.251         evaadmin.huishoubao.com
	10.135.42.251         evaluation.huishoubao.com.cn
	10.135.109.132        api-amc.huishoubao.com.cn
	10.135.109.132        amc.huishoubao.com.cn
vpc-test-admin02
'''