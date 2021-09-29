#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : p001_xyplus_20210911.py
@Author  : liuzhiming
@Time    : 2021/9/11 11:04
"""

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test, hsb_response_print


class XYPlusAuto:

    def __init__(self):
        self.secret_key = "gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU"
        self.callerserviceid = "112006"

        self.strCheckList = []
        self.strCheckDesc = ''
        self.strSkuList = []
        self.strSkuDesc = ''
        self.aIdList = []

    def product_check_item(self, productId):
        url = "http://codserver.huishoubao.com/detect/product_check_item"
        param = {"_head": {"_interface": "product_check_item_xyplus", "_msgType":"request", "_remark":"", "_version":"0.01", "_timestamps":"123456", "_invokeId":"123456", "_callerServiceId":"112006", "_groupNo":"1" },"_param": {"productId": productId}}

        md5value = json.dumps(param) + "_" + self.secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":self.callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典
        # print("======获取检测选项返回参数=========\n{}".format(json.dumps(respone_dict, indent=4, ensure_ascii=False)))
        checkList = respone_dict['_data']['_data']['checkList']
        skuList = respone_dict['_data']['_data']['skuList']

        for info in checkList:
            answerList = info['answerList']
            # index = random.randint(0, len(answerList) - 1)
            index = 0
            self.strCheckList.append(answerList[index]['answerId'])
            self.strCheckDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'
        self.strCheckList = self.strCheckList[:-1]

        for info in skuList:
            answerList = info['answerList']
            # index = random.randint(0, len(answerList) - 1)
            index = 0
            self.strSkuList.append(answerList[index]['answerId'])
            self.strSkuDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'

        # print('接口响应『json』格式数据为：\n', json.dumps(respone_dict, ensure_ascii=False),'\n')
        print('检测sku选项-答案项ID（随机取）：{}\n'.format(self.strSkuList))
        print('检测机况选项-答案项ID（随机取）：{}\n'.format(self.strCheckList))
        print('检测以上【sku】+以上【机况】选项名称+答案项名称：{}{}\n'.format(self.strSkuDesc, self.strCheckDesc[:-1]))
        print('接口响应时长：{0} 秒'.format(respone.elapsed.total_seconds()))

    # 产品服务 | 22.检测标准化选项转换估价选项 | http://wiki.huishoubao.com/index.php?s=/105&page_id=3297
    def convert_check_item_to_eva(self, productId, orderId="", isOverInsurance="1"):
        self.product_check_item(productId)
        param = {"_head": {"_interface": "convert_check_item_to_eva", "_msgType": "request", "_remark": "",
                           "_version": "0.01", "_timestamps": "123456", "_invokeId": "123456",
                           "_callerServiceId": self.callerserviceid, "_groupNo": "1"},
                 "_param": {"orderId": orderId, "productId": productId, "skuList": self.strSkuList, "checkList": self.strCheckList,
                            "isOverInsurance": isOverInsurance}}
        print("======转换估价选项参数=========\n{}".format(param))
        url = "http://codserver.huishoubao.com/detect/convert_check_item_to_eva"
        md5value = json.dumps(param) + "_" + self.secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),
                   "HSB-OPENAPI-CALLERSERVICEID": self.callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典

        print(respone_dict)

        self.aIdList = respone_dict['_data']['_data']['select']
        print("======aIdList==============={}".format(self.aIdList))

        print('==========1. 产品sku选项-答案项ID（随机取）：\n', self.strSkuList)
        print()
        print('==========2. 检测机况选项-答案项ID（随机取）：\n', self.strCheckList)
        print()
        print('==========3. 以上【sku】+【机况】选项对应的问题项名称+答案项名称：\n', '{' + self.strSkuDesc + self.strCheckDesc[:-1] + '}' + '\n')

    # 销售等级生产：http://wiki.huishoubao.com/web/#/105?page_id=6051
    def sales_level_generation_xyplus(self, productId, channelId, aIdList = "", checkAIdList="", orderId = "", isRecord = 1):

        if not aIdList or not checkAIdList:
            self.convert_check_item_to_eva(productId, orderId)
            aIdList = self.aIdList
            checkAIdList = self.strCheckList

        param = {"_head": {"_interface": "sales_level_generation_xyplus", "_msgType": "request", "_remark": "",
                           "_version": "0.01", "_timestamps": "", "_invokeId": "", "_callerServiceId": self.callerserviceid,
                           "_groupNo": "1"},
                 "_param": {"productId": productId, "orderId": orderId, "channelId": channelId, "aIdList": aIdList,"checkAIdList": checkAIdList,
                            "isRecord": isRecord}}
        print(param)
        url = "http://prdserver.huishoubao.com/product/sales_level_generation"
        md5value = json.dumps(param) + "_" + self.secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),
                   "HSB-OPENAPI-CALLERSERVICEID": self.callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())

        print('==========4. 产品ID：『{0}』，『请求获取‘销售等级’的估价答案项』为：\n'.format(productId), checkAIdList)
        # print('==========5. 转换后的SKU+机况选项的描述：\n', aIdListOption)
        hsb_response_print(respone=respone)


if __name__ == '__main__':
    plus = XYPlusAuto()
    # plus.product_check_item("38200")     #
    # plus.sales_level_generation_xyplus(productId="38200", channelId="10000260", orderId="7636695")
    # plus.sales_level_generation_xyplus(productId="38200", channelId="10000260", orderId="7636695")
    plus.convert_check_item_to_eva("41567","7636932",isOverInsurance="1")





