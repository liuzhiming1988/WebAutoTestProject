#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 32.2.帮买获取用户精准估价、最高价、下跌价 - http://wiki.huishoubao.net/index.php?s=/105&page_id=8355  -  server-bangmai_pro_eva

    入参：pid：pid，不为空  |  channelId：渠道id，不为空  |  productId：要查询产品选项的产品ID
        select：用户选择的估价选项ID，当为空数组时，获取的是机型的最高价  |  ip：用户真实IP（限频用）  |  userId：用户id

    出参：hsbPrice：回收价价格，单位:分  |  highestPrice：帮买最高价，单位:分  |  dropInPrice：预计降价幅度，单位:分

    eva_option_get接口：http://wiki.huishoubao.com/web/#/105?page_id=1595  platform_type：使用在不需要 pid 和 channle_id 的场景下，优先使用channel_id 或 pid，可不传
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test, hsb_response_print

class BM_Evaluate:
    def eva_option_get(self, channel_id, product_id, pid):
        param = {"_head": {"_interface": "eva_option_get", "_msgType": "request", "_remark": "hello", "_version": "0.01","_timestamps": "123", "_invokeId": "111", "_callerServiceId": "112002", "_groupNo": "1"},"_param": {"channel_id": channel_id, "product_id": product_id, "pid": pid, "platform_type":"1"}}
        secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
        callerserviceid = "112002"
        url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
        md5value = json.dumps(param) + "_" + secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典
        options_list = respone_dict['_body']['_data']['itemList']

        str_options_list = []
        str_options_desc_show = ''
        for info in options_list:
            answerList = info['question']
            index = random.randint(0, len(answerList) - 1)
            str_options_list.append(answerList[index]['id'])
            # 以下只为打印输出随机取的估价选项数据
            str_options_desc_show += '"' + info['name'] + ":" + answerList[index]['name'] + '",'
        str_options_desc_show = str_options_desc_show[:-1]

        return str_options_list,str_options_desc_show

    def bm_evaluate(self, channelId, pid, productId):
        (select,str_options_desc_show) = self.eva_option_get(channel_id=channelId,product_id=productId,pid=pid)
        param = {"_head":{"_interface":"bm_evaluate","_msgType":"request","_remark":"hello","_version":"0.01","_timestamps":"123","_invokeId":"111","_callerServiceId":"110001","_groupNo":"1"},"_param":{"channelId":channelId, "pid":pid, "productId":productId, "select":select, "ip":"127.0.0.1"}}
        url = "http://bmserver.huishoubao.com/bangmai/bm_evaluate"
        secret_key = "c36691ced620bf82ad3fc4642f8a6427"
        callerserviceid = "110001"
        md5value = json.dumps(param) + "_" + secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())

        print('==========>1. 估价答案项ID传参数据为（随机取）：\n', select)
        print('\n')
        print('==========>2. 以上估价答案项ID对应的选项+答案项名称：\n', '{' + str_options_desc_show[:-1] + '}' + '\n')
        hsb_response_print(respone=respone)

if __name__ == '__main__':
    product_32_2 = BM_Evaluate()
    # product_32_2.bm_evaluate(channelId='10000164', pid='1405', productId='')
    # product_32_2.bm_evaluate(channelId='10000164', pid='1405', productId='41567')
    product_32_2.bm_evaluate(channelId='10000164', pid='1405', productId='63330')