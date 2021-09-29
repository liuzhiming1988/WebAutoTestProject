#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 | 22.检测标准化选项转换估价选项 | http://wiki.huishoubao.com/index.php?s=/105&page_id=3297  | 对应服务：server-evaluate_detect

    入参：orderid：订单ID（必填） | productId：修改产品后的产品id 优先使用这个 未传递则使用DB中的（非必选） | skuList：sku答案选项（必填）
        checkList：检测答案选项（必填） | isOverInsurance：是否强制过保 0:否 1:强制过保,默认为0（非必填）
    出参：select：转换出来的估价选项 | selectName：转化后的选项的选项描述 | checkPrice：检测价格 | evaluateId：估价Id
        insured：保价标记 1保价 2不保价 | orderId：订单Id | productId：产品Id
        productChangeInsured：由修改产品导致的订单过保，当入参isOverInsurance为1，强制过保时，此参数默认为0，不做判断
        skuChangeInsured：由SKu变动导致的订单过保，入参isOverInsurance为1，强制过保时，此参数默认为0，不做判断
    依赖接口：产品服务 - 21.获取检测标准化产品信息【产品商品库sku信息 + 标准检测机况信息】 - http://wiki.huishoubao.com/index.php?s=/105&page_id=3295
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

class Convert_Check_Item_To_Eva:
    def __init__(self):
        self.secret_key = "gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU"
        self.callerserviceid = "112006"

    def product_check_item(self, productId):
        # 【57项标准检测】 "_interface":"product_check_item"
        # 【闲鱼验机】【53项灰度检】  "_interface":"product_check_item_grayscale"
        # 【闲鱼无忧购验机1.0】  "_interface":"product_check_item_youpin"
        # 【闲鱼无忧购验机2.0】  "_interface":"product_check_item_youpin_v2"
        # 【34项标准检测】  "_interface":"product_check_item_34"
        param = {"_head": { "_interface":"product_check_item_youpin_v2", "_msgType":"request", "_remark":"", "_version":"0.01", "_timestamps":"123456", "_invokeId":"123456", "_callerServiceId":"112006", "_groupNo":"1" },"_param": {"productId":productId}}
        url = "http://codserver.huishoubao.com/detect/product_check_item"
        md5value = json.dumps(param) + "_" + self.secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":self.callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典
        skuList = respone_dict['_data']['_data']['skuList']
        checkList = respone_dict['_data']['_data']['checkList']

        strSkuList = []
        for info in skuList:
            answerList = info['answerList']
            # index = random.randint(0, len(answerList) - 1)
            index = 0
            strSkuList.append(answerList[index]['answerId'])

        strCheckList = []
        for info in checkList:
            answerList = info['answerList']
            # index = random.randint(0, len(answerList) - 1)
            index = 0
            strCheckList.append(answerList[index]['answerId'])

        return strSkuList, strCheckList

    def convert_check_item_to_eva(self, orderId, productId, isOverInsurance):
        (skuList,checkList) = self.product_check_item(productId=productId)
        # skuList = ['6116', '471', '18', '2236', '38', '1091', '1773']
        # checkList = ['7420', '7422', '7426', '7429', '7433', '7438', '7442', '8054', '8055', '7452', '7461', '7462', '7466', '7469', '7471', '7478', '7482', '7489', '7490', '7493', '7500', '7506', '7510', '7518', '7526', '7615', '7534', '7536', '7545', '7547', '7553', '7556', '7560', '7563', '7571', '7574', '7579', '7581', '7587', '7590', '7606', '7614']
        param = {"_head": { "_interface":"convert_check_item_to_eva", "_msgType":"request", "_remark":"", "_version":"0.01", "_timestamps":"123456", "_invokeId":"123456", "_callerServiceId":"112006", "_groupNo":"1" },"_param": {"orderId":orderId,"productId":productId,"skuList":skuList,"checkList":checkList, "isOverInsurance":isOverInsurance }}
        url = "http://codserver.huishoubao.com/detect/convert_check_item_to_eva"
        md5value = json.dumps(param) + "_" + self.secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":self.callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置

        print('==========>1. 产品ID：『{0}』，『检测sku答案项』(随机取)为：\n'.format(productId), skuList)
        print('\n==========>2. 产品ID：『{0}』，『检测机况答案项』(随机取)为：\n'.format(productId), checkList)
        print('\n')
        hsb_response_print(respone=respone)

        # respone_dict = json.loads(respone.text)  # 转成字典
        # selectName = respone_dict['_data']['_data']['selectName']  # 解析出数据
        # strEvaDesc = ''
        # for x in selectName:
        #     strEvaDesc += '"' + x.replace(':', '":"') + '",'
        # print("转换后的估价选项为：\n", '{' + strEvaDesc[:-1] + '}')

if __name__ == '__main__':
    product_22 = Convert_Check_Item_To_Eva()
    # product_22.convert_check_item_to_eva(orderId="7598533", productId="54791", isOverInsurance='')
    # product_22.convert_check_item_to_eva(orderId="7598541", productId="23009", isOverInsurance='1')
    # product_22.convert_check_item_to_eva(orderId="7598541", productId="23009", isOverInsurance='0')
    ''' 2020.03.12 检测估价强制过保需求'''
    # 不带参数 isOverInsurance
    # ①isOverInsurance传空
    # ①isOverInsurance传0
    # ①isOverInsurance传值非0非1
    # ①isOverInsurance传值1，强制过保
    # ①isOverInsurance传非1，检测机型型号与下单型号不一致
    # ①isOverInsurance传1(条件优先），检测机型型号与下单型号不一致
    # ①isOverInsurance传非1，商品库sku选项变化（1091-40），未做映射，"_errStr":"估价SKU项 颜色 在标准检测中未传递对应选项
    # ①isOverInsurance传非1，商品库sku选项变化（1091-40），做了映射，"_errStr":"估价SKU项 颜色 在标准检测中未传递对应选项"

    ''' 2021年5月27日 对接口list进行严格校验'''
    # "_errStr":"估价SKU项 购买渠道 在标准检测中未传递对应选项"
    # product_22.convert_check_item_to_eva(orderId="7633197", productId="41567", isOverInsurance='0') # 2021-05-25日订单 skuList = []  checkList = []

    # "_errStr": "skuList 参数格式错误"
    # product_22.convert_check_item_to_eva(orderId="7633197", productId="41567", isOverInsurance='0') # 2021-05-25日订单 skuList = [""]  checkList = [""]

    # "_errStr":"skuList 参数格式错误"
    # product_22.convert_check_item_to_eva(orderId="7633197", productId="41567", isOverInsurance='0') # 2021-05-25日订单 skuList = ["abc"]  checkList = [""]

    # skuList = ['6116', '471', '18', '2236', '38', '1091', '1773']     checkList = ["abc"]  or  checkList = [""]
    # "_errStr":"checkList 参数格式错误"
    # product_22.convert_check_item_to_eva(orderId="7633197", productId="41567", isOverInsurance='1') # 2021-05-25日订单

    # 迅捷单-获取3.0销售价
    product_22.convert_check_item_to_eva(orderId="7636909", productId="30831", isOverInsurance='0')  # 2021-09-23日订单


'''
{"fclass_name":"手机选项库","fid":"1","flevel":"1","fname":"整机类","fpid":"497","fpid_name":"手机选项库","fvalid":"1"},
{"fclass_name":"手机选项库","fid":"2","flevel":"1","fname":"屏幕类","fpid":"497","fpid_name":"手机选项库","fvalid":"1"},
{"fclass_name":"手机选项库","fid":"3","flevel":"1","fname":"外观类","fpid":"497","fpid_name":"手机选项库","fvalid":"1"},
{"fclass_name":"手机选项库","fid":"4","flevel":"1","fname":"主板类","fpid":"497","fpid_name":"手机选项库","fvalid":"1"}
'''