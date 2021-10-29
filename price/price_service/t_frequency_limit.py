#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : t_frequency_limit.py
@Author  : liuzhiming
@Time    : 2021/10/27 15:29
"""

import json
import random
import time
import requests

from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_MD5_Enerypt import res_print
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test, hsb_eva_ipProxy_k8s_test

"""
【频率限制测试】对应服务：k8s   basepriceevaluate
接口：http://codserver.huishoubao.com/detect/product_check_item
wiki：http://wiki.huishoubao.com/web/#/105?page_id=3295

接口：http://bpeserver.huishoubao.com/adjustment_price/sale_apply_price
wiki：http://wiki.huishoubao.com/web/#/138?page_id=15625

confluence测试总结: http://confluence.huishoubao.com/pages/viewpage.action?pageId=4622207
"""


class Sale_Apply_Price:
    def product_check_item_34(self, productId):
        param = {
            "_head": {"_interface": "product_check_item_34", "_msgType": "request", "_remark": "", "_version": "0.01",
                      "_timestamps": "123456", "_invokeId": "test_zhangjinfa", "_callerServiceId": "112006",
                      "_groupNo": "1"}, "_param": {"productId": productId}}
        secret_key = "gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU"
        callerserviceid = "112006"
        url = "http://codserver.huishoubao.com/detect/product_check_item"
        md5value = json.dumps(param) + "_" + secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),
                   "HSB-OPENAPI-CALLERSERVICEID": callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典
        checkList = respone_dict['_data']['_data']['checkList']
        skuList = respone_dict['_data']['_data']['skuList']

        strCheckList = []
        strCheckDesc = ''
        for info in checkList:
            answerList = info['answerList']
            '''第一种方式：在answerList下随机取1个'''
            index = random.randint(0, len(answerList) - 1)
            strCheckList.append(answerList[index]['answerId'])
            strCheckDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'

            '''第二种方式：在answerList下取answerWeight最大的那个'''
            # index = sorted(answerList, key=lambda x: int(x['answerWeight']), reverse=True)[0]
            # strCheckList.append(index['answerId'])
            # strCheckDesc += '"' + info['questionName'] + ":" + index['answerName'] + '",'

        strSkuList = []
        strSkuDesc = ''
        for info in skuList:
            answerList = info['answerList']
            index = random.randint(0, len(answerList) - 1)
            strSkuList.append(answerList[index]['answerId'])
            strSkuDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'
        return strSkuList, strSkuDesc, strCheckList, strCheckDesc

    def sale_apply_price(self, planId, productId, evaType, ip="10.0.11.88", user_id="1895", freqLimitType="1"):
        # (strSkuList, strSkuDesc, strCheckList, strCheckDesc) = self.product_check_item_34(productId=productId)

        '''1. iPhone X'''
        strSkuList = ['8012', '130', '17', '2236', '36', '42', '2242']
        strCheckList = ['9015', '9019', '9027', '9028', '9035', '9039', '9047', '7481', '9057', '9059', '9062', '9067',
                        '9071', '9074', '7559', '9077', '9079', '7570', '7574', '9082', '9084', '7589', '9090', '9094',
                        '9098', '9102', '9106', '9111', '9117', '9120']

        param = {"_head": {"_interface": "sale_apply_price", "_msgType": "request", "_remark": "", "_version": "0.01",
                           "_timestamps": "1525332832", "_invokeId": "lzm_adjustPrice",
                           "_callerServiceId": "116006", "_groupNo": "1"},
                 "_param": {"planId": planId, "productId": productId, "evaType": evaType, "skuItem": strSkuList,
                            "optItem": strCheckList, "ip": ip, "userId": user_id, "freqLimitType": freqLimitType}}
        # print("==========>请求参数为：\n{}".format(json.dumps(param)))
        secret_key = "R2gFCRbILiNhwv3YbtaGceYJlPS5Ku02"
        callerserviceid = "116006"
        url = "http://bpeserver.huishoubao.com/adjustment_price/sale_apply_price"
        md5value = json.dumps(param) + "_" + secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),
                   "HSB-OPENAPI-CALLERSERVICEID": callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_k8s_test())

        # print('========>1.『{0}』 产品的『检测标准化选项-sku』(随机取)为：\n'.format(productId), strSkuList)
        # print('\n========>2. 以上『检测标准化选项-sku』为：\n', '{' + strSkuDesc[:-1] + '}')
        # print('\n========>3.『{0}』 产品的『检测标准化选项-机况-34』(随机取)为：\n'.format(productId), strCheckList)
        # print('\n========>4. 以上『检测标准化选项-机况-34』为：\n', '{' + strCheckDesc[:-1] + '}')
        # res_print(respone)
        print(respone.json()["_data"]["_errStr"])


if __name__ == '__main__':
    # 频率限制类型，0不限制；1-IP，2-UserId

    sale = Sale_Apply_Price()

    for x in range(1, 4+1):
        print("=======第{}次\n".format(x))
        time.sleep(1)
        sale.sale_apply_price(planId="3", productId="41567", evaType="3",
                              ip="10.0.11.2", user_id="1891",
                              freqLimitType="2")

    # 天限制  ip和UserId都已限制
    # sale.sale_apply_price(planId="3", productId="41567", evaType="3",
    #                       ip="10.0.11.2", user_id="1891",
    #                       freqLimitType="1")

    # 已加黑名单 ip="10.0.11.99", user_id="1999"
    # sale.sale_apply_price(planId="3", productId="41567", evaType="3",
    #                       ip="10.0.11.99", user_id="1999",
    #                       freqLimitType="1")

    # 同时在黑名单和白名单
    # sale.sale_apply_price(planId="3", productId="41567", evaType="3",
    #                       ip="10.0.11.100", user_id="1888",
    #                       freqLimitType="1")
