#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : p002_insured_role202109.py
@Author  : liuzhiming
@Time    : 2021/9/24 17:11
"""

import requests
import json
import os
import random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test, hsb_response_print,hsb_eva_ipProxy_k8s_test

"""
获取产品检测模板选项信息：http://wiki.huishoubao.com/web/#/138?page_id=15854
检测模板获取回收价：http://wiki.huishoubao.net/web/#/138?page_id=15977
需求点：
1.定价标准发生变化，从检测方式的历史记录中取定价标准一致的检测模板选项
2.不保价三种场景：强制过保、超过保价期、检测与估价机型不一致
3.比价逻辑
4.检测选项->定价选项->估价选项，选项转换测试
5.特殊逻辑映射测试：维修问题项-100061特殊映射
"""


# 对应服务：
# 命令
class V3_Evaluate:
    def __init__(self):
        self.callerserviceid = "112002"
        self.secret_key_v3_eva_option_get = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"

        self.serviceid_eva = "216002"
        self.secret_key_v3_evaluate = "bw32mCzrqvBykEDetbyqZoOWU9GZ8Pqb"

    def v3_eva_option_get(self, channel_id, pid, product_id):
        "http://wiki.huishoubao.com/web/#/347?page_id=15707"
        param = {"_head": {"_interface": "eva_option_get", "_msgType": "request", "_remark": "eva_product_v3",
                           "_version": "0.01", "_timestamps": "123", "_invokeId": "eva_product_v3",
                           "_callerServiceId": self.callerserviceid, "_groupNo": "1"},
                 "_param": {"channel_id": channel_id, "product_id": product_id, "pid": pid}}
        url = "http://prdserver.huishoubao.com/eva_product_v3/eva_option_get"
        md5value = json.dumps(param) + "_" + self.secret_key_v3_eva_option_get
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),
                   "HSB-OPENAPI-CALLERSERVICEID": self.callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典
        print(json.dumps(respone_dict, indent=4, ensure_ascii=False))
        options_list = respone_dict['_body']['_data']['itemList']

        str_options_list = []
        str_options_desc = ''
        for info in options_list:
            answerList = info['question']
            index = random.randint(0, len(answerList) - 1)
            str_options_list.append(answerList[index]['id'])
            str_options_desc += '"' + info['name'] + '":"' + answerList[index]['name'] + '",'

        return str_options_list, str_options_desc

    def v3_evaluate(self, channel_id, pid, product_id, options_list=None):
        "http://wiki.huishoubao.com/web/#/347?page_id=15687"
        if options_list:
            str_options_list, str_options_desc = options_list, "非自动获取"
        else:
            (str_options_list, str_options_desc) = self.v3_eva_option_get(channel_id=channel_id, pid=pid,
                                                                          product_id=product_id)
        param = {"_head": {"_interface": "evaluate", "_msgType": "request", "_remark": "liuzhiming_autoTest",
                           "_version": "0.01", "_timestamps": "123", "_invokeId": "111",
                           "_callerServiceId": self.serviceid_eva, "_groupNo": "1"},
                 "_param": {"productid": product_id, "ip": "127.0.0.1", "cookies": "zhangjinfa_autoTest",
                            "userid": "1895", "select": str_options_list, "pid": pid, "channel_id": channel_id}}
        url = "http://evaserver.huishoubao.com/evaluate_price_v3/evaluate"
        md5value = json.dumps(param) + "_" + self.secret_key_v3_evaluate
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),
                   "HSB-OPENAPI-CALLERSERVICEID": self.serviceid_eva}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典

        print('========>1.『{0}』 产品的『估价选项-答案项ID』(随机取)为：\n'.format(product_id), str_options_list)
        print('\n========>2. 以上『估价选项-问题项名称：答案项名称』为：\n', '{' + str_options_desc[:-1] + '}')
        hsb_response_print(respone=respone)


class V3_Recycle_Evaluate:
    def v3_product_check_item(self, orderId, productId, checkType):
        "http://wiki.huishoubao.com/web/#/138?page_id=15854"
        param = {"_head": {"_interface": "product_check_item", "_msgType": "request", "_remark": "", "_version": "0.01",
                           "_timestamps": "1525332832",
                           "_invokeId": "152533283241636", "_callerServiceId": "216002", "_groupNo": "1"},
                 "_param": {"productId": productId, "orderId": orderId, "checkType": checkType, "userId": "1895",
                            "freqLimitType": "1", "ip": "127.0.0.1"}}
        secret_key = "rAfnRwyWfh2N9vXVgWwdpJxaXgOCd8af"
        callerserviceid = "216002"
        url = "http://codserver.huishoubao.com/detect_v3/product_check_item"
        md5value = json.dumps(param) + "_" + secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),
                   "HSB-OPENAPI-CALLERSERVICEID": callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典
        print("获取检测模板选项结果：\n{}".format(json.dumps(respone.json(), indent=4, ensure_ascii=False)))
        checkList = respone_dict['_data']['_data']['checkList']
        skuList = respone_dict['_data']['_data']['skuList']

        strCheckList = []
        strCheckDesc = ''
        for info_question in checkList:
            questionList = info_question['questionList']
            for info_answer in questionList:
                answerList = info_answer['answerList']
                '''第一种方式：在answerList下随机取1个'''
                index = random.randint(0, len(answerList) - 1)
                strCheckList.append(answerList[index]['answerId'])
                strCheckDesc += '"' + info_answer['questionName'] + ":" + answerList[index]['answerName'] + '",'

                '''第二种方式：在answerList下取answerWeight最大的那个'''
                # index = sorted(answerList, key=lambda x: int(x['answerWeight']), reverse=True)[0]
                # strCheckList.append(index['answerId'])
                # strCheckDesc += '"' + info_answer['questionName'] + '":"' + index['answerName'] + '",'

        strSkuList = []
        strSkuDesc = ''
        for info in skuList:
            answerList = info['answerList']
            # index = random.randint(0, len(answerList) - 1)
            index = 0
            strSkuList.append(answerList[index]['answerId'])
            strSkuDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'

        print(strSkuList, strCheckList)
        return strSkuList, strSkuDesc, strCheckList, strCheckDesc

    def v3_recycle_evaluate(self, orderId, productId, checkType, isOverInsurance, sku_list=None, item_list=None):
        "http://wiki.huishoubao.com/web/#/138?page_id=15977"
        if sku_list:
            strSkuList, strSkuDesc, strCheckList, strCheckDesc = sku_list, "SKU非自动获取", item_list, "机况检测选项非自动获取"
        else:
            (strSkuList, strSkuDesc, strCheckList, strCheckDesc) = self.v3_product_check_item(
                orderId=orderId, productId=productId, checkType=checkType)

        param = {
            "_head": {
                "_interface": "recycle_evaluate",
                "_msgType": "request",
                "_remark": "",
                "_version": "0.01",
                "_timestamps": "1525332832",
                "_invokeId": "152533283241636",
                "_callerServiceId": "816006",
                "_groupNo": "1"
            },
            "_param": {
                "productId": productId,
                "orderId": orderId,
                "checkType": checkType,
                "optItem": strCheckList,
                "skuItem": strSkuList,
                "userId": "1895",
                "isOverInsurance": isOverInsurance,
                "ip": "127.0.0.1"
            }
        }
        # print(param)
        secret_key = "rAfnRwyWfh2N9vXVgWwdpJxaXgOCd8af"
        callerserviceid = "216002"
        url = "http://codserver.huishoubao.com/detect_v3/recycle_evaluate"
        md5value = json.dumps(param) + "_" + secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),
                   "HSB-OPENAPI-CALLERSERVICEID": callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        res = respone.json()
        print("获取检测回收价 | {}".format(url))
        print("响应信息为：")
        print(json.dumps(res, indent=4, ensure_ascii=False))
        options_list = []  # 估价明细选项
        for item in res["_data"]["_data"]["evaItemList"]:
            aId = item["ansId"]
            options_list.append(aId)

        base_list = []  # 定价选项
        for item in res["_data"]["_data"]["baseItemList"]:
            aId = item["ansId"]
            base_list.append(aId)

        print('========>1.『{0}』 产品的『标准sku』(随机取)为：\n'.format(productId), strSkuList)
        print('\n========>2. 以上『标准sku』为：\n', '{' + strSkuDesc[:-1] + '}')
        print('\n========>3.『{0}』 产品的『检测模板选项-机况-价格3.0』(随机取)为：\n'.format(productId), strCheckList)
        print('\n========>4. 以上『检测模板选项-机况-价格3.0』为：\n', '{' + strCheckDesc[:-1] + '}')
        # hsb_response_print(respone=respone)

        print("转换后的估价明细选项为：{}".format(options_list))
        print("======转换后的定价明细选项为：\n{}".format(base_list))
        if "100061" in options_list:
            print("成功命中 【屏幕和主板均有维修/故障（ID：100061）】")


if __name__ == '__main__':
    ''' 估价系统 与 定价系统 区分开理解，此处，不考虑机型的 定价状态'''

    v3_eva = V3_Evaluate()  # 用户估价
    rec_eva = V3_Recycle_Evaluate()  # 检测回收价   服务EvaluateCheckV3

    # 1. 调试获取估价选项
    # v3_eva.v3_eva_option_get(channel_id="10000060", pid="1260",product_id="41567")

    # check_list = ['15', '18', '36', '42', '1634', '100044', '100048', '100055', '100017', '100005', '100058', '100066']
    # check_list = ['100062', '100044', '100048', '100052', '100017',
    #               '100005', '100058', '12', '17', '36', '42', '1083']    # 固定估价选项iPhone X
    # check_list = ['100061', '100062', '100049', '100056', '12', '17',
    #               '36', '40', '130', '1083', '2235']   # 固定估价选项iPhone12   4737
    check_list = ['8012', '17', '38', '42', '1634', '100065', '100056', '100044',
                  '100048', '100026', '100008', '100074']  # 测试估价模板（非线上同步模板）

    # 回收宝自有-APP渠道ID10000060进行估价--使用固定选项
    # v3_eva.v3_evaluate(channel_id='10000060', pid='1260', product_id='41567', options_list=check_list)   # iphone x
    # v3_eva.v3_evaluate(channel_id='10000060', pid='1260', product_id='41567')  # iphone x  自动选择估价选项
    # v3_eva.v3_evaluate(channel_id='10000060', pid='1260', product_id='64494', options_list=check_list)  # iphone 12  预估价=历史价

    # 获取检测回收价测试
    sku_list = ['12', '17', '36', '42', '130', '1083', '2236']  # iphone X
    # sku_list = ['12', '17', '36', '40', '130', '1083', '2235']  # iphone 12
    item_list = ['9032', '9037', '9045', '9055', '9770', '9086', '9100', '9104', '9110',
                 '9113', '9016', '9024', '9565', '9056', '9058', '9060', '9065', '9070', '9073', '9075', '9076',
                 '9078', '9080', '9081', '7575', '9083', '9088', '9119', '9191', '9092', '9096']

    """
    检测环节特殊逻辑：
      定价答案项命中屏幕维修（ID：9093）、更换非原装屏（ID：9092）、更换屏幕玻璃盖板（ID：9091）其一，
      且同时命中序列号异常（ID：9097）、内存扩容（ID：9096）、主板维修/故障（ID：9095）其一
      ①估价子模板包含答案项 屏幕和主板均有维修/故障（ID：100061），默认映射到此答案项，不再匹配映射关系
      ②估价子模板未包含答案项 屏幕和主板均有维修/故障（ID：100061），使用映射规则
    """
    # spec_list = ['9093', '9097']
    # spec_list = ['9093', '9096']
    # spec_list = ['9093', '9095']
    # spec_list = ['9092', '9097']
    # spec_list = ['9092', '9096']
    # spec_list = ['9092', '9095']
    # spec_list = ['9091', '9097']
    # spec_list = ['9091', '9096']
    # spec_list = ['9091', '9095']
    # spec_list = ['9090', '9095']  # 未同时命中指定定价选项，则根据映射关系进行命中（100060）
    # item_list.extend(spec_list)  # 合并入特殊逻辑命中选项

    # rec_eva.v3_recycle_evaluate(orderId="7637141", productId="41567", checkType="3", isOverInsurance="0")   # 已过保（超过保价期）
    # rec_eva.v3_recycle_evaluate(orderId="7639875", productId="41567", checkType="2", isOverInsurance="0",
    #                             sku_list=sku_list, item_list=item_list)  # 未过保

    # 二期切换
#     rec_eva.v3_recycle_evaluate(orderId="7639883", productId="30831", checkType="1", isOverInsurance="0",
#                                 sku_list=["12","18","37","45","130","2257","2234"], item_list=["9015","9037","9045","9054","9056","9060","9065"
# ,"9070","7559","9080","7570","9083","9087","7589","9090","9108","9109","9112","9564","9649","9651","8158","8164","8168","9660","9658","8241","8240","9028","9094","9019","9625"])  # 未过保

    rec_eva.v3_recycle_evaluate(orderId="7639980", productId="38200", checkType="5", isOverInsurance="0",
                                                            sku_list=sku_list, item_list=item_list)  # 未过保
    # rec_eva.v3_recycle_evaluate(orderId="7637142", productId="41567", checkType="4", isOverInsurance="0",sku_list=sku_list,item_list=item_list)   # 找不到对应定价标准的检测模板
    # rec_eva.v3_recycle_evaluate(orderId="7637142", productId="41567", checkType="3", isOverInsurance="1")   # 已过保（强制过保）
    # rec_eva.v3_recycle_evaluate(orderId="7637142", productId="30831", checkType="3", isOverInsurance="0")   # 已过保（机型不一致）

    # 估价答案项无100061（特殊映射逻辑）,返回的估价明细中应无100061
    # rec_eva.v3_recycle_evaluate(orderId="7637142", productId="64494", checkType="3", isOverInsurance="1",
    #                             sku_list=sku_list, item_list=item_list)  #

    # 人工指定检测选项
    # rec_eva.v3_recycle_evaluate(orderId="7637142", productId="41567", checkType="3", isOverInsurance="0",sku_list=sku_list,item_list=item_list)  # 未过保

    skus12 = ['12', '17', '36', '40', '130', '1083', '2235']
    items12 = ['9032', '9037', '9045', '9055', '9770', '9086', '9093', '9097', '9100', '9104', '9110', '9113', '9016',
               '9024', '9565', '9056', '9058', '9060', '9065', '9070', '9073', '9075', '9076', '9078', '9080', '9081',
               '7575', '9083', '9088', '9119', '9191']
    # rec_eva.v3_recycle_evaluate(orderId="7637189", productId="64494", checkType="3", isOverInsurance="1",
    #                             sku_list=skus12, item_list=items12)      # iPhone 12   预估价=历史价

    # 获取检测选项测试
    # rec_eva.v3_product_check_item(productId="41567", orderId="7637142", checkType="4")      # 获取不到有效的检测模板
    # rec_eva.v3_product_check_item(productId="41567", orderId="", checkType="3")    # 获取历史中的检测模板

    """
    1.现网检测模板的定价标准与历史定价标准不一致，取历史价
    2.sku无版本时，取标准SKU出价格，不会再估价失败。
    """
    """
    下单成功，iPhone X 订单ID：【7637141】   过保
    下单成功，iPhone X 订单ID：【7637142】   未过保
    下单成功，iPhone12 订单ID：【7637189】    用户估价4737
    """
