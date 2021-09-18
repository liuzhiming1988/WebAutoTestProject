#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 45.检测获取产品商品库sku信息和大质检机况信息  - http://wiki.huishoubao.com/index.php?s=/105&page_id=7967
    1. 对应服务：server-evaluate_detect（服务器应用名：server-evaluate_detect）
    2. 对应URL http://codserver.huishoubao.com

    入参：productId：产品id（必填） | orderId：订单id（必填） | isOverInsurance：是否强制过保，0-否，1-强制过保，默认为0（非必填）
    出参：orderId：是，订单id | productId：是，产品id | optionList：是，大质检机况 问题项集合 | skuList：是，商品库sku 问题项集合；
        questionId：是，大质检机况/商品库sku，问题项id | questionName：是，大质检机况/商品库sku，问题项名称
        answerList：是，大质检机况/商品库sku，答案项集合；
          answerId：是，大质检机况/商品库sku，答案项id；| answerName：是，大质检机况/商品库sku，答案项名称；| answerWeight：是，大质检机况/商品库sku 答案项权重,值越大机况越好
        dIdList：是，细化项集合 | dId：否，细化项ID | dName：否，细化项名称
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def get_product_lib_sku_option_item(productId, orderId, isOverInsurance):
    param = {"_head": { "_interface":"get_product_lib_sku_option_item", "_msgType":"request", "_remark":"", "_version":"0.01", "_timestamps":"123456", "_invokeId":"123456", "_callerServiceId":"112006", "_groupNo":"1"},"_param": {"productId":productId, "orderId":orderId, "isOverInsurance":isOverInsurance}}

    secret_key = "gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU"
    callerserviceid = "112006"
    url = "http://codserver.huishoubao.com/detect/get_product_lib_sku_option_item"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    respone.encoding = respone.apparent_encoding  # 编码设置
    print(respone.text)
    respone_dict = json.loads(respone.text)  # 转成字典
    optionList = respone_dict['_data']['_data']['optionList']
    skuList = respone_dict['_data']['_data']['skuList']

    strOptionList = ''
    strOptionDesc = ''
    for info in optionList:
        answerList = info['answerList']
        index = random.randint(0, len(answerList) - 1)
        strOptionList += '"' + answerList[index]['answerId'] + '",'
        strOptionDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'
    strOptionList = strOptionList[:-1]

    strSkuList = ''
    strSkuDesc = ''
    for info in skuList:
        answerList = info['answerList']
        index = random.randint(0, len(answerList) - 1)
        strSkuList += '"' + answerList[index]['answerId'] + '",'
        strSkuDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'
    strSkuList = strSkuList[:-1]

    print('接口响应『json』格式数据为：\n', json.dumps(respone_dict, ensure_ascii=False), '\n')
    print('商品库sku选项-答案项ID（随机取）：\n', '{' + strSkuList + '}' + '\n')
    print('大质检机况选项-答案项ID（随机取）：\n', '{' + strOptionList + '}' + '\n')
    print('以上【sku】+【机况】选项对应的问题项名称+答案项名称：\n', '{' + strSkuDesc + strOptionDesc[:-1] + '}' + '\n')
    print('接口响应时长：{0} 秒'.format(respone.elapsed.total_seconds()))

if __name__ == '__main__':
    # get_product_lib_sku_option_item(productId='', orderId='',isOverInsurance='')
    # get_product_lib_sku_option_item(productId='', orderId='7632330',isOverInsurance='')
    # get_product_lib_sku_option_item(productId='41567', orderId='7632330',isOverInsurance='')
    # get_product_lib_sku_option_item(productId='41567', orderId='7632330',isOverInsurance='2')
    # get_product_lib_sku_option_item(productId='41567', orderId='7632330',isOverInsurance='0')
    get_product_lib_sku_option_item(productId='41567', orderId='7632330',isOverInsurance='1')
    # get_product_lib_sku_option_item(productId='54791', orderId='7598466',isOverInsurance='0')
    # get_product_lib_sku_option_item(productId='23009', orderId='7598541',isOverInsurance='1')

    # get_product_lib_sku_option_item(productId='59249', orderId='7605674',isOverInsurance='0')

    # 错误的（传的productId，并不是这个orderId下的，会返回新的 productId 的sku和机况信息）
    # param = '{"_head": { "_interface":"get_product_lib_sku_option_item", "_msgType":"request", "_remark":"", "_version":"0.01", "_timestamps":"123456", "_invokeId":"123456", "_callerServiceId":"112006", "_groupNo":"1" }, "_param": { "productId":"30831", "orderId":"7559186"}}'

    # 过保订单
    # param = '{"_head": { "_interface":"get_product_lib_sku_option_item", "_msgType":"request", "_remark":"", "_version":"0.01", "_timestamps":"123456", "_invokeId":"123456", "_callerServiceId":"112006", "_groupNo":"1" },"_param": { "productId":"54791", "orderId":"7554950"}}'

'''
curl -H 'HSB-OPENAPI-SIGNATURE:bcc22ec180295451ea19d49ee416d7bf' -H 'HSB-OPENAPI-CALLERSERVICEID:216008' -d '{"_head":{"_callerServiceId":"216008","_groupNo":"1","_interface":"pdt_sku_query","_invokeId":"d3084ed04a1ca1d534e31edc4fd09f48","_msgType":"request","_remark":"","_timestamps":"1603177363","_version":"0.01"},"_param":{"info":{"combination":"0","productId":"54791"},"subInterface":"sku_option_combination_get"}}' http://prdserver.huishoubao.com/rpc/new_product_lib

response: {"_body":{"_data":{"options":[{"aInfo":[{"aId":"12","aName":"大陆国行"},{"aId":"13","aName":"香港行货"},{"aId":"14","aName":"其他国家地区-无锁版"},{"aId":"15","aName":"其他国家地区-有锁版"},{"aId":"1124","aName":"国行官换机/官翻机"},{"aId":"6047","aName":"国行展示机"},{"aId":"6116","aName":"国行BS机"},{"aId":"7630","aName":"监管机"}],"qId":"11","qName":"购买渠道"},{"aInfo":[{"aId":"124","aName":"移动版"},{"aId":"130","aName":"全网通"},{"aId":"471","aName":"移动联通"}],"qId":"122","qName":"制式"},{"aInfo":[{"aId":"17","aName":"保修一个月以上"},{"aId":"18","aName":"保修一个月以内或过保"}],"qId":"16","qName":"保修期"},{"aInfo":[{"aId":"2236","aName":"3GB"}],"qId":"2232","qName":"机身内存"},{"aInfo":[{"aId":"36","aName":"64GB"},{"aId":"37","aName":"128GB"},{"aId":"38","aName":"256GB"}],"qId":"32","qName":"存储容量"},{"aInfo":[{"aId":"40","aName":"白色"},{"aId":"41","aName":"黑色"},{"aId":"47","aName":"红色"},{"aId":"133","aName":"蓝色"},{"aId":"395","aName":"黄色"},{"aId":"2202","aName":"珊瑚色"}],"qId":"39","qName":"颜色"},{"aInfo":[{"aId":"1083","aName":"其他型号"},{"aId":"2269","aName":"A2108"},{"aId":"5377","aName":"A2107"}],"qId":"918","qName":"型号"}],"productId":"54791","skuGroup":null},"_ret":"0","_retcode":"0","_retinfo":"成功"},"_head":{"_callerServiceId":"216008","_groupNo":"1","_interface":"pdt_sku_query","_invokeId":"d3084ed04a1ca1d534e31edc4fd09f48","_msgType":"response","_remark":"","_timestamps":"1603177363","_version":"0.01"}}

select Fid, Fname, Flevel, Fpid, Fplatform_type_property, Fvalid, Fweight from t_eva_item_base  where Fid in(12,13,14,15,1124,6047,6116,7630,124,130,471,17,18,2236,36,37,38,40,41,47,133,395,2202,1083,2269,5377);

curl -d '{"head":{"interface":"insured_options","msgtype":"request","remark":"","version":"0.01"},"params":{"order_id":"7598466","productId":"54791","user_name":"server-evaluate_detect"}}' http://evaserver.huishoubao.com/rpc/insured

线上调用
curl -H 'HSB-OPENAPI-SIGNATURE:ea815ffb8be4600e693a910df496334c' -H 'HSB-OPENAPI-CALLERSERVICEID:112006' -d '{"_head": {"_interface": "get_product_lib_sku_option_item", "_msgType": "request", "_remark": "","_version": "0.01", "_timestamps": "123456", "_invokeId": "123456","_callerServiceId": "112006", "_groupNo": "1"},"_param": {"productId": "23007", "orderId": "10192534", "isOverInsurance":"0"}}' http://codserver.huishoubao.com/detect/get_product_lib_sku_option_item
'''