#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : v3_e8_auto_check.py
@Author  : liuzhiming
@Time    : 2021/9/7 10:48
"""

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test, hsb_response_print


class V3AutoCheck:

    def __init__(self):
        self.sku_checked = []
        self.opt_checked = []
        self.proxies = hsb_eva_ipProxy_test()

    def v3_product_check_item(self, productId, checkType, freqLimitType, ip):
        print("\n=============获取sku和opt选中列表=================")
        param = {"_head": {"_interface": "product_check_item", "_msgType": "request", "_remark": "", "_version": "0.01",
                           "_timestamps": "1525332832", "_invokeId": "152533283241636", "_callerServiceId": "216002",
                           "_groupNo": "1"},
                 "_param": {"productId": productId, "checkType": checkType, "userId": "1895",
                            "freqLimitType": freqLimitType, "ip": ip}}
        secret_key = "rAfnRwyWfh2N9vXVgWwdpJxaXgOCd8af"
        callerserviceid = "216002"
        url = "http://codserver.huishoubao.com/detect_v3/product_check_item"
        md5value = json.dumps(param) + "_" + secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),
                   "HSB-OPENAPI-CALLERSERVICEID": callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=self.proxies)
        respone.encoding = respone.apparent_encoding  # 编码设置
        # hsb_response_print(respone=respone)

        raw_json = json.loads(respone.text)
        if raw_json["_data"]["_errCode"] == "0":
            pass
        else:
            print(raw_json["_data"]["_errStr"])
            return False

        check_list = raw_json["_data"]["_data"]["checkList"]
        check_desc = "=============已选机况信息（描述）：===================\n"
        sku_list = raw_json["_data"]["_data"]["skuList"]
        sku_desc = "=============已选sku（描述）：===================\n"

        j = 1
        for sku in sku_list:
            answer_list = sku["answerList"]
            self.sku_checked.append(answer_list[0]["answerId"])
            sku_desc += "{}-【{}】：{}({})\n".format(j,
                sku["questionName"], answer_list[0]["answerName"], answer_list[0]["answerId"])
            j += 1
        print("【SKU选中列表】{}".format(self.sku_checked))
        print(sku_desc)

        i = 1
        for opt in check_list:
            for question in opt["questionList"]:
                answer_list = question["answerList"]
                self.opt_checked.append(answer_list[0]["answerId"])
                check_desc += "{}-【{}】：{}({})\n".format(i,
                    question["questionName"], answer_list[0]["answerName"], answer_list[0]["answerId"])
                i+=1
        print("【机况选中项】{}".format(self.opt_checked))
        print(check_desc)

    def v3_sale_evaluate(self, planId, productId, checkType, freqLimitType, ip):
        print("\n=============获取估价信息===========")
        url = "http://codserver.huishoubao.com/detect_v3/sale_evaluate"
        param = {"_head": {"_interface": "sale_evaluate", "_msgType": "request", "_remark": "", "_version": "0.01",
                           "_timestamps": "1525332832", "_invokeId": "152533283241636",
                           "_callerServiceId": "216002", "_groupNo": "1"},
                 "_param": {"planId": planId, "productId": productId, "checkType": checkType, "optItem": self.opt_checked,
                            "skuItem": self.sku_checked, "userId": "1895", "freqLimitType": freqLimitType, "ip": ip}}
        secret_key = "rAfnRwyWfh2N9vXVgWwdpJxaXgOCd8af"
        callerserviceid = "216002"

        md5value = json.dumps(param) + "_" + secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),
                   "HSB-OPENAPI-CALLERSERVICEID": callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=self.proxies)
        respone.encoding = respone.apparent_encoding  # 编码设置
        # hsb_response_print(respone=respone)

        raw_json = json.loads(respone.text)
        if raw_json["_data"]["_errCode"] == "0":
            print(raw_json["_data"]["_data"])
        else:
            print(raw_json["_data"]["_errStr"])
            return False

    def v3_sale_evaluate_generation(self, productId, evaType):
        checkType = ""
        if evaType == "0":
            checkType = "2"

        print("\n=============获取等级信息============")
        url = "http://codserver.huishoubao.com/detect_v3/sales_level_generation"
        param = {"_head": {"_interface": "sales_level_generation", "_msgType": "request", "_remark": "",
                           "_version": "0.01", "_timestamps": "1525332832", "_invokeId": "152533283241636",
                           "_callerServiceId": "216002", "_groupNo": "1"},
                 "_param": {"productId": productId, "evaType": evaType,
                            "optItem": self.opt_checked, "checkType": checkType}}
        secret_key = "rAfnRwyWfh2N9vXVgWwdpJxaXgOCd8af"
        callerserviceid = "216002"

        md5value = json.dumps(param) + "_" + secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),
                   "HSB-OPENAPI-CALLERSERVICEID": callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=self.proxies)
        respone.encoding = respone.apparent_encoding  # 编码设置
        # hsb_response_print(respone=respone)

        raw_json = json.loads(respone.text)
        if raw_json["_data"]["_errCode"] == "0":
            level_info = raw_json["_data"]["_data"]
            print(level_info)
        else:
            print(raw_json["_data"]["_errStr"])
            return False


if __name__ == '__main__':

    # evaType：质检类型，1-57标准质检，2-大质检，3-34标准质检，0-价格3.0
    # checkType：检测类型、检测场景，例如顺丰上门场景，或是闲鱼验机场景	1,2	是
    # 出参：
    #         evaBasePrice：销售定价价格 单位:分
    #         sellerPrice：卖家参考价 单位:分
    #         sellerMaxPrice：卖家最高价考价 单位:分
    #         buyerPrice：买家参考价 单位:分
    #         recordId：估价唯一id（id 会超过int(11)，请不要用int保存）（可通过：24 获取定价估价记录接口，获取信息）
    #         levelId：价格3.0-定价等级id  |  levelName：价格3.0-定价等级名称
    #         saleLevelId：价格3.0-销售等级id （价格2.0为空）  |  saleLevelName：价格3.0-销售等级名称 （价格2.0为空）
    #         baseLevelTag：价格3.0-定价等级标签
    #         baseLevelTag.tagId：定价等级标签id  |  baseLevelTag.tagName：定价等级标签名称
    #         saleLevelTag：价格3.0-销售等级标签
    #         saleLevelTag.tagId：销售等级标签id  |  saleLevelTag.tagName：销售等级标签名称
    productId = '23011'
    checkType = '2'
    freqLimitType = '1'
    ip = '127.0.0.1'

    planId = "9"
    evaType = "0"

    auto_check = V3AutoCheck()
    auto_check.v3_product_check_item(productId, checkType, freqLimitType, ip)

    auto_check.v3_sale_evaluate(planId, productId, checkType, freqLimitType, ip)

    auto_check.v3_sale_evaluate_generation(productId, evaType)




