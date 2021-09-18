#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 34.销售等级的生成 - sales_level_generation - http://wiki.huishoubao.net/index.php?s=/105&page_id=6051
    服务：base_product
    1. 标准检机况：不需要传channelId  |  2. 大质检机况：需要传channelId（销售价格查询需求中，产品需要的是2C平台，默认使用 回收宝主站 渠道id

    入参：productId：产品Id （必填） | channelId：渠道Id （必填）；
        aIdList：估价答案项列表（可直接通过 产品服务 - 6.可估价产品产品选项获取（eva_option_get）  取到估价答案项） （必填）；
        cIdList：估价检测细化项列表（必填，可传空） | orderId：订单号（非必填）
        checkAIdList：检测答案项列表,检测,估价答案项只要包含其一就可，即(channelId&&aIdList&&cIdList) or checkAIdList  （非必填）；
        isRecord：是否做记录,1-做记录，0-不做记录，只给估价后台使用，默认记录（非必填）
    出参：productId：产品id | templateId：使用的销售等级模版Id | level：成色等级
        levelName：成色名称 | levelDesc：成色描述 | levelLabel：销售标签
        _retcode：3001：配置问题 根据产品ID获取不到销售等级模版; | 3002：配置问题 该产品已被禁用,无法生成销售等级;
            3003：配置问题 该产品配置的销售等级模版被禁用; | 3004：配置问题 该产品配置的销售等级模版和选项模版的映射被禁用;
            3005：配置问题 产品使用的检测模版未和销售等级模版建立映射; | 3006：配置问题 产品未使用检测模版;
            3008：配置问题 无法生成等级; 1-系统错误和参数错误，0-成功
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

class Sales_Level_Generation_Notebook:
    def __init__(self):
        self.secret_key = "gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU"
        self.callerserviceid = "112006"

    # 产品服务 - 45.检测获取产品商品库sku信息和大质检机况信息  - http://wiki.huishoubao.com/index.php?s=/105&page_id=7967
    def get_product_lib_sku_option_item(self, productId, orderId):
        param = {"_head": {"_interface": "get_product_lib_sku_option_item", "_msgType": "request", "_remark": "","_version": "0.01", "_timestamps": "123456", "_invokeId": "123456","_callerServiceId": "112006", "_groupNo": "1"},"_param": {"productId": productId, "orderId": orderId}}
        url = "http://codserver.huishoubao.com/detect/get_product_lib_sku_option_item"
        md5value = json.dumps(param) + "_" + self.secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID": self.callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典
        skuList = respone_dict['_data']['_data']['skuList']
        optionList = respone_dict['_data']['_data']['optionList']

        strSkuList = []
        strSkuDesc = ''
        for info_sku in skuList:
            answerList_sku = info_sku['answerList']
            index_sku = random.randint(0, len(answerList_sku) - 1)
            strSkuList.append(answerList_sku[index_sku]['answerId'])
            strSkuDesc += '"' + info_sku['questionName'] + ":" + answerList_sku[index_sku]['answerName'] + '",'

        strOptionList = []
        strOptionDesc = ''
        for info_option in optionList:
            answerList_option = info_option['answerList']
            index_option = random.randint(0, len(answerList_option) - 1)
            strOptionList.append(answerList_option[index_option]['answerId'])
            strOptionDesc += '"' + info_option['questionName'] + ":" + answerList_option[index_option]['answerName'] + '",'
        return strSkuList, strOptionList, strSkuDesc, strOptionDesc

    # 产品服务 - 46.检测商品库sku信息加大质检机况估价接口 - http://wiki.huishoubao.com/index.php?s=/105&page_id=8007
    def product_lib_and_option_to_evaluate(self, orderId, productId):
        (skuList, optionList, skuDesc, sptionDesc) = self.get_product_lib_sku_option_item(productId=productId, orderId=orderId)
        param = {"_head": {"_interface": "product_lib_and_option_to_evaluate", "_msgType": "request", "_remark": "","_version": "0.01", "_timestamps": "123456", "_invokeId": "123456", "_callerServiceId": "112006", "_groupNo": "1"},"_param": {"orderId": orderId, "productId": productId, "skuList": skuList, "optionList": optionList, "userId": "1311"}}
        url = "http://codserver.huishoubao.com/detect/product_lib_and_option_to_evaluate"
        md5value = json.dumps(param) + "_" + self.secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID": self.callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典

        print('==========1. 商品库sku选项-答案项ID（随机取）：\n', skuList)
        print('==========2. 大质检机况选项-答案项ID（随机取）：\n', optionList)
        print('==========3. 以上【sku】+【机况】选项对应的问题项名称+答案项名称：\n', '{' + skuDesc + sptionDesc[:-1] + '}' + '\n')

        return respone_dict['_data']['_data']['select'], respone_dict['_data']['_data']['selectName']

    def sales_level_generation_notebook(self, productId, orderId, channelId):
        (aIdList, aIdListOption)= self.product_lib_and_option_to_evaluate(orderId=orderId, productId=productId)
        param = {"_head":{"_interface":"sales_level_generation","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"","_invokeId":"","_callerServiceId":"112002","_groupNo":"1"},"_param":{"productId":productId,"channelId":channelId,"aIdList":aIdList,"cIdList":[]}}
        secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
        callerserviceid = "112002"
        url = "http://prdserver.huishoubao.com/product/sales_level_generation"
        md5value = json.dumps(param) + "_" + secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())

        print('==========4. 产品ID：『{0}』，『请求获取‘销售等级’的估价答案项』为：\n'.format(productId), aIdList)
        print('==========5. 转换后的SKU+机况选项的描述：\n', aIdListOption)
        hsb_response_print(respone=respone)

if __name__ == '__main__':
    product_34_3 = Sales_Level_Generation_Notebook()
    '''【20210120原则上】平板和笔记本，只有大质检，没有保价概念
    但是，获取销售等级，不管走标准检还是大质检，最终都可以通过传 aIdList（估价答案项list）来获取销售等级
    即使是走标准件，价格接口会将其检测选项转换成估价选项，检测只需要传 aIdList，就可以通过销售等级模板映射的估价选项模板来获取到等级 '''
    # 平板  | 64011 | ZY0101210120000136 | iPad Pro 12.9寸 4代 2020款
    # product_34_3.sales_level_generation_notebook(productId='64011', orderId='7605607', channelId='40000001') # iPad Pro 12.9寸 4代 2020款
    # product_34_3.sales_level_generation_notebook(productId="30765", orderId='7605614', channelId='40000001') # iPad Pro 9.7寸 2016款
    # product_34_3.sales_level_generation_notebook(productId="31201", orderId='7605617', channelId='40000001') # iPad 4代 (Retina屏)
    # product_34_3.sales_level_generation_notebook(productId="31231", orderId='7605618', channelId='40000001') # iPad mini4
    # product_34_3.sales_level_generation_notebook(productId="59114", orderId='7605619', channelId='40000001') # iPad Pro 12.9寸 3代 2018款
    # product_34_3.sales_level_generation_notebook(productId="64011", orderId='7605620', channelId='40000001') # iPad Pro 12.9寸 4代 2020款
    # product_34_3.sales_level_generation_notebook(productId="64429", orderId='7605624', channelId='40000001') # iPad 8代

    product_34_3.sales_level_generation_notebook(productId="64467", orderId='7605659', channelId='40000001') # 华为 MatePad 10.8英寸
    # product_34_3.sales_level_generation_notebook(productId="64327", orderId='7605660', channelId='40000001') # 华为MediaPad T5 10.1英寸
    # product_34_3.sales_level_generation_notebook(productId="63815", orderId='7605670', channelId='40000001') # 华为 MatePad Pro 10.8英寸
