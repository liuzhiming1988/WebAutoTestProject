#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 估价服务 - 22-等级价格批量估价接口 - http://wiki.huishoubao.com/web/#/138?page_id=12364

    入参：channelId：渠道ID，10000031，否（与 platformId 二选一） | platformId：平台ID，1，否（与 channelId 二选一））
        productId：估价产品ID，41567，是 | userid：登录用户ID，未登录用户，可为空	是
        skuItem：用户选择的sku选项，[“12”,”17”,”36”]，是 | version：配置版本ID（渠道，则为价格运营版本，平台，则为平台版本）
    出参：price：估算价格，单位:分，是 | level：等级，是
'''

import requests, json, time, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_baseprice_ipProxy_test, hsb_eva_ipProxy_test, hsb_response_print

class Eva_Level_Price_Batch():
    def pdt_sku_query(self, productId):
        param = {"_head": {"_interface": "pdt_sku_query", "_msgType": "request", "_remark": "", "_version": "0.01","_timestamps": "123", "_invokeId": "111", "_callerServiceId": "112002", "_groupNo": "1"},"_param": {"subInterface": "sku_option_combination_get","info": {"productId": productId, "combination": "1"}}}
        secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
        callerserviceid = "112002"
        url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
        md5value = json.dumps(param) + "_" + secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID": callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典
        optionsList = respone_dict['_body']['_data']['options']

        str_sku_answer_list = []
        str_Option_answer_desc = ''
        for info in optionsList:
            answerList = info['aInfo']
            index = random.randint(0, len(answerList) - 1)
            str_sku_answer_list.append(answerList[index]['aId'])
            # 以下只为打印输出随机取的估价选项数据
            str_Option_answer_desc += '"' + info['qName'] + ":" + answerList[index]['aName'] + '",'
        str_Option_answer_desc = str_Option_answer_desc[:-1]

        print('==========>1. 机型标准SKU为（随机取）：\n', str_sku_answer_list)
        print()
        print('==========>2. 以上SKU答案项ID对应的选项+答案项名称：\n', '{' + str_Option_answer_desc[:-1] + '}' + '\n')
        return str_sku_answer_list

    def product_lib_sku_to_eva_sku(self, orderId, productId):
        skuList = self.pdt_sku_query(productId=productId)
        param = {"_head": {"_interface": "product_lib_sku_to_eva_sku", "_msgType": "request", "_remark": "hello","_version": "0.01", "_timestamps": "123", "_invokeId": "111", "_callerServiceId": "112006","_groupNo": "1"}, "_param": {"orderId": orderId, "productId": productId, "skuList": skuList}}
        secret_key = "gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU"
        callerserviceid = "112006"
        url = "http://codserver.huishoubao.com/detect/product_lib_sku_to_eva_sku"
        md5value = json.dumps(param) + "_" + secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID": callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典
        sku_list = respone_dict['_data']['_data']['itemList']

        str_sku_list = []
        str_sku_desc_show = ''
        for index in range(0, len(sku_list)):
            str_sku_list.append(sku_list[index]['aId'])
            # 以下只为打印输出随机取的估价选项数据
            str_sku_desc_show += '"' + sku_list[index]['qName'] + ":" + sku_list[index]['aName'] + '",'
        str_sku_desc_show = str_sku_desc_show[:-1]

        print('接口响应『json』格式数据为：\n', json.dumps(respone_dict, ensure_ascii=False) + '\n')
        print('==========>3. 通过商品库sku获取到的估价sku选项为：\n', str_sku_list)
        print()
        print('==========>4. 以上估价SKU选项信息未：\n', '{' + str_sku_desc_show + '}' + '\n')
        return str_sku_list

    ''' 等级价格批量估价接口 '''
    def eva_level_price_batch(self,orderId, channelId, platformId, productId, version):
        skuItem = self.product_lib_sku_to_eva_sku(orderId=orderId, productId=productId)
        param = {"head":{"interface":"eva_level_price_batch","msgtype":"request","remark":"","version":"0.01"},"params":{"channelId":channelId, "platformId":platformId, "cookies":"111111111","ip":"127.0.0.1","productId":productId, "skuItem":skuItem,"version":version, "userId":"1311"}}
        url = "http://evaserver.huishoubao.com/rpc/evaluate"
        headers = {"Content-Type": "application/json;charset=UTF-8"}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        hsb_response_print(respone=respone)

if __name__ == '__main__':
    evaserver22 = Eva_Level_Price_Batch()
    evaserver22.eva_level_price_batch(orderId='7632219', channelId='40000001', platformId='', productId='41567', version='54')
    # evaserver22.eva_level_price_batch(orderId='7632219', channelId='40000001', platformId='', productId='41567', version='111111111')
    # evaserver22.eva_level_price_batch(orderId='7632219', channelId='40000001', platformId='', productId='41567', version='')
    # evaserver22.eva_level_price_batch(orderId='7632219', channelId='', platformId='1', productId='41567', version='920')
    # evaserver22.eva_level_price_batch(orderId='7632219', channelId='', platformId='1', productId='41567', version='111111111')

'''
{"head": {"interface": "eva_level_price_batch", "msgtype": "request", "remark": "", "version": "0.01"}, "params": {"channelId": "40000001", "cookies": "111111111", "ip": "127.0.0.1", "productId": "41567", "skuItem": ["12", "17", "36", "42", "1083"], "userId": "1311", "version": "50"}}
-- StandardPrice:255000 MinPrice:5100
-- 大陆国行 sku:12 value:101 FactorPrice = 255000 * 101% = 257550
-- 保修一个月以上 sku:17 value:100 FactorPrice = 257550 * 100% = 257550
-- 64GB sku:36 value:86 FactorPrice = 257550 * 86% = 221493
-- 银色 sku:42 value:100 FactorPrice = 221493 * 100% = 221493
-- 其他型号 sku:1083 value:85 FactorPrice = 221493 * 85 = 188269
-- level:10 value:3 FactorPrice = 188269 * 3% = 5648.07  Remove Score Quatation:5600
-- level:100 value:118 FactorPrice = 188269 * 118% = 222157 Remove Score Quatation:222100
-- 平台和渠道的价格等级ID如果不一致的话，等级对应的渠道回收价格是：无
-- 渠道中，等级上下限控制值，（强制）默认取的是“下限”值，（强制）默认为“百分比”，即使设置的是“绝对值”，也当做百分比值处理
-- 渠道中，如果有sku的系数配置为 “0”，则按0处理，等级价格计算出来全是0，触发最低价逻辑
'''