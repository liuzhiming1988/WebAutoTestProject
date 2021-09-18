#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang

''' 产品服务 - 25.产品标准SKU的获取  - http://wiki.huishoubao.com/index.php?s=/105&page_id=4705
    1. 对应服务：server-base_product（base_product）  |   2. 对应URL：http://prdserver.huishoubao.com

    产品标准SKU（等同于商品库SKU），在机型详情页面，拿到机型标准SKU，再将其映射为 估价SKU
    标准SKU  和  估价SKU  使用的是同一个sku选项池子
    区别在于，举例，如 8GB（17）  64GB（18）  映射成  估价SKU   8+64GB（19） | t_eva_platform_product

    入参：productId：（必填）产品id
        combination：（非必填）获取有效无效sku组合的标记 可不传 默然为0
    出参：productId：产品id | combination：sku组合 | aIdList：组成sk的答案项 | fullSkuId：sku答案组合Id（完整skuId，格式：1_123）
        valid：sku启用标记 | options：sku选项信息 | qName：问题项名称 | qId：问题项id | aInfo：答案项信息 | aId：答案项id | aName：答案项名称
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def pdt_sku_query( productId, combination ):
    param = {"_head":{"_interface":"pdt_sku_query","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"123","_invokeId":"111","_callerServiceId":"112002","_groupNo":"1"},"_param":{"subInterface":"sku_option_combination_get","info":{"productId":productId, "combination":combination}}}
    secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
    callerserviceid = "112002"
    url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    respone.encoding = respone.apparent_encoding  # 编码设置
    respone_dict = json.loads(respone.text)  # 转成字典
    optionsList = respone_dict['_body']['_data']['options']

    str_sku_answer_list = ''
    str_Option_answer_desc = ''
    for info in optionsList:
        answerList = info['aInfo']
        index = random.randint(0, len(answerList) - 1)
        str_sku_answer_list += '"' + answerList[index]['aId'] + '",'
        str_Option_answer_desc += '"' + info['qName'] + ":" + answerList[index]['aName'] + '",'
    str_sku_answer_list = str_sku_answer_list[:-1]

    print('接口响应『json』格式数据为：\n', json.dumps(respone_dict, ensure_ascii=False) + '\n')
    print('【sku】选项-答案项ID（随机取）：\n', '{' + str_sku_answer_list + '}' + '\n')
    print('以上【sku】选项名称+答案项名称：\n', '{' + str_Option_answer_desc[:-1] + '}' + '\n')
    print('接口响应时长：{0} 秒'.format(respone.elapsed.total_seconds()))

if __name__ == '__main__':
    ''' 响应场景："combination":"", "options":"", "productId":"60290", "skuGroup":"" 均非空 '''
    # pdt_sku_query(productId="60290", combination='1')  # 华为 P30
    # pdt_sku_query(productId="23009", combination='1')  # 小米 1s
    # pdt_sku_query(productId="49239", combination='1')  # 小米 8
    # pdt_sku_query(productId="3", combination='1')  # iphone 4
    # pdt_sku_query(productId="1", combination='1')  # iPhone 3GS     "combination": [], "skuGroup": null
    # pdt_sku_query(productId="64001", combination='0')  # iphone X
    # pdt_sku_query(productId="64247", combination='1')

    pdt_sku_query(productId="64247", combination='0')

'''
20200728 更新
20200728-171428-496|INFO|139754866940160||18728|127.0.0.1|base_product|../cgi_frame/cgi_frame.cpp|run|82|
REQUEST_METHOD = POST
CONTENT_LENGTH = 295
SCRIPT_FILENAME = /rpc/new_product_lib
REMOTE_ADDR = 218.18.137.26
HTTP_COOKIE = 
QUERY_STRING = 
POST_DATA = {"_head": {"_interface": "pdt_sku_query", "_msgType": "request", "_remark": "", "_version": "0.01", "_timestamps": "123", "_invokeId": "111", "_callerServiceId": "200001", "_groupNo": "1"}, "_param": {"subInterface": "sku_option_combination_get", "info": {"productId": "1", "combination": "1"}}}

-- 产品SKU映射表
select Fproduct_id, Fvalid_sku_id, Finvalid_sku_id, Fsku_group, Fversion from t_pdt_sku_map  where Fproduct_id = 1;
select Fid, Faid_list from t_pdt_sku  where Fid in (241475,241476,241477,241478,241479,241480,41701,41704);
select Fid, Faid_list from t_pdt_sku  where Fid in (17398,25058);
select t_a.Fid as Faid, t_a.Fname as Faname, t_q.Fid as Fqid, t_q.Fname as Fqname  from t_eva_item_base as t_a, t_eva_item_base as t_q  where t_a.Fpid=t_q.Fid and t_a.Flevel=3 and t_q.Flevel=2 and t_a.Fid in (1192,12,1210,130,1853,2238,2492,38)
select Fid, Fproduct_id, Fsku_id, Fsku_group, Fofficial_guidance_price, Fofficial_guidance_time, Fretail_price, Fretail_price_time, Ftrade_price, Ftrade_price_time, Fpromotion_price, Fpromotion_price_time, F70_new_price, F70_new_time, Foperator, Fofficial_guidance_remark, Fretail_remark, Ftrade_remark, Fpromotion_remark, F70_new_remark from t_eva_risk_price  where (1=1) AND Fproduct_id = 64247 and Fsku_id in (241475,241476,241477,241478,241479,241480,41701,41704);

outPacket=[{"_body":{"_data":{"combination":[],"options":[],"productId":"1","skuGroup":null},"_ret":"0","_retcode":"0","_retinfo":"成功"},"_head":{"_callerServiceId":"200001","_groupNo":"1","_interface":"pdt_sku_query","_invokeId":"111","_msgType":"response","_remark":"","_timestamps":"1595927668","_version":"0.01"}}]
'''