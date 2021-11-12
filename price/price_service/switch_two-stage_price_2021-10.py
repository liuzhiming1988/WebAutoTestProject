#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : switch_two-stage_price_2021-10.py
@Author  : liuzhiming
@Time    : 2021/10/15 10:59
"""

import requests
import json
import os
from random import randint
from price.hsb_MD5_Enerypt import get_price_headers, res_print
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test, hsb_response_print
import operator

"""
获取估价选项
http://prdserver.huishoubao.com/eva_product_v3/eva_option_get
http://wiki.huishoubao.com/web/#/347?page_id=15707
获取估价
http://evaserver.huishoubao.com/evaluate_price_v3/evaluate
http://wiki.huishoubao.com/web/#/347?page_id=15687
获取检测模板选项
http://codserver.huishoubao.com/detect_v3/product_check_item
http://wiki.huishoubao.com/web/#/138?page_id=15854
检测模板获取回收价
http://codserver.huishoubao.com/detect_v3/recycle_evaluate
http://wiki.huishoubao.com/web/#/138?page_id=15977
定价选项获取销售价格
http://bpeserver.huishoubao.com/adjustment_price/sale_apply_price
http://wiki.huishoubao.com/web/#/138?page_id=15625
检测模板获取销售价格
http://codserver.huishoubao.com/detect_v3/sale_evaluate
http://wiki.huishoubao.com/web/#/138?page_id=15853
"""


# 【价格3.0】用户估价
class V3EvaPrice:

    def v3_eva_option_get(self, product_id, channel_id, pid, get_way="1", is_best="1"):
        """获取产品估价选项"""
        url = "http://prdserver.huishoubao.com/eva_product_v3/eva_option_get"
        param = {"_head": {"_interface": "eva_option_get", "_msgType": "request", "_remark": "eva_product_v3",
                           "_version": "0.01", "_timestamps": "123", "_invokeId": "eva_product_v3",
                           "_callerServiceId": "112002", "_groupNo": "1"},
                 "_param": {"channel_id": channel_id, "product_id": product_id, "pid": pid}}
        print("url：{}，请求参数\n{}".format(url, json.dumps(param)))
        res = requests.post(url, json=param, headers=get_price_headers(param), proxies=hsb_eva_ipProxy_test())
        res_print(res, "1")  # 打印输出响应结果，非1数字打印json格式
        questions = res.json()["_body"]["_data"]["itemList"]
        answer_ids = []  # 定义答案项ID列表
        answer_names = ""  # 定义答案项名称列表，便于对照
        for question in questions:
            answers = question["question"]
            question_single = question["single"]
            if get_way == "1":  # 随机获取答案项
                if question_single == "1":
                    """随机选中单选"""
                    i = randint(0, len(answers) - 1)
                    answer_id = answers[i]["id"]
                    answer_ids.append(answer_id)

                    answer_name = answers[i]["name"]
                    answer_names += "【{}】{}\n".format(answer_id, answer_name)

                elif question_single == "2":
                    """多选, 
                    1.随机多选N项，
                    2.随机选中，如果多选标识，添加到临时列表，
                    3.如果是单选，则清空已选中项，只保留单选项，
                    4.最后添加到answer_ids
                    """
                    j = randint(1, len(answers))  # 随机多选的个数
                    temp_ids = []
                    temp_names = ""
                    for x in range(j):
                        i = randint(0, len(answers) - 1)
                        answer_single = answers[i]["single"]

                        if answer_single == "1":
                            """答案项是单选，则对临时变量（存储id和name）重新赋值，并退出循环"""
                            answer_id = answers[i]["id"]
                            temp_ids = [answer_id]
                            answer_name = answers[i]["name"]
                            temp_names = "【{}】{}\n".format(answer_id, answer_name)
                            break
                        elif answer_single == "2":
                            """答案项是多选，则将id和name追加到临时变量中"""
                            answer_id = answers[i]["id"]
                            if answer_id in temp_ids:  # 防止随机到重复的答案项
                                pass
                            else:
                                temp_ids.append(answer_id)
                                answer_name = answers[i]["name"]
                                temp_names += "【{}】{}\n".format(answer_id, answer_name)
                    # 将多选问题项的最后结果添加到最终结果中
                    temp_ids = list(dict.fromkeys(temp_ids))  # 对列表去重
                    answer_names += temp_names
                    answer_ids.extend(temp_ids)

            elif get_way == "2":  # 按优先级返回固定答案项
                answers = sorted(answers, key=operator.itemgetter("priority"), reverse=True)  # 按优先级字段进行倒序

                if is_best == "0":  # 取优先级最高的
                    answer_id = answers[0]["id"]
                    answer_ids.append(answer_id)
                    answer_name = answers[0]["name"]
                    answer_names += "【{}】{}\n".format(answer_id, answer_name)
                elif is_best == "1":  # 取优先级最低的
                    answer_id = answers[-1]["id"]
                    answer_ids.append(answer_id)
                    answer_name = answers[-1]["name"]
                    answer_names += "【{}】{}\n".format(answer_id, answer_name)

        print("========>1.产品的『估价选项-答案项ID』为：\n{}".format(answer_ids))
        print("\n========>2. 以上『估价选项-问题项名称：答案项名称』为：\n{}".format(answer_names))

        return answer_ids

    def v3_eva(self, product_id, channel_id, pid, options=None):
        if not options:
            options = self.v3_eva_option_get(product_id, channel_id, pid)
        url = "http://evaserver.huishoubao.com/evaluate_price_v3/evaluate"
        param = {"_head": {"_interface": "evaluate", "_msgType": "request", "_remark": "liuzhiming_autoTest",
                           "_version": "0.01", "_timestamps": "895467888516", "_invokeId": "79464631336456",
                           "_callerServiceId": "216053", "_groupNo": "1"},
                 "_param": {"productid": product_id, "ip": "127.0.0.1", "cookies": "liuzhiming_autoTest",
                            "userid": "1895", "select": options, "pid": pid, "channel_id": channel_id}}
        print("获取估价结果的请求参数为：\n{}".format(param))
        print(get_price_headers(param))
        res = requests.post(url, json=param, headers=get_price_headers(param), proxies=hsb_eva_ipProxy_test())
        res_print(res, "1")  # 打印输出响应结果，非1数字打印json格式


# 【价格3.0】检测模板获取回收价
class V3DetectGetRecyclePrice:

    def v3_product_check_item(self, product_id, order_id, check_type, is_over="0"):
        "http://wiki.huishoubao.com/web/#/138?page_id=15854"
        param = {"_head": {"_interface": "product_check_item", "_msgType": "request", "_remark": "", "_version": "0.01",
                           "_timestamps": "1525332832",
                           "_invokeId": "152533283241636", "_callerServiceId": "216002", "_groupNo": "1"},
                 "_param": {"productId": product_id, "orderId": order_id, "checkType": check_type, "userId": "1895",
                            "freqLimitType": "1", "isOverInsurance": is_over, "ip": "127.0.0.1"}}
        url = "http://codserver.huishoubao.com/detect_v3/product_check_item"
        print("url：{}  请求参数\n{}".format(url, json.dumps(param)))
        respone = requests.post(url, json=param, headers=get_price_headers(param), proxies=hsb_eva_ipProxy_test())
        res_print(respone)
        respone_dict = respone.json()
        checkList = respone_dict['_data']['_data']['checkList']
        skuList = respone_dict['_data']['_data']['skuList']

        strCheckList = []
        strCheckDesc = ''
        for info_question in checkList:
            questionList = info_question['questionList']
            for info_answer in questionList:
                answerList = info_answer['answerList']
                '''第一种方式：在answerList下随机取1个'''
                index = randint(0, len(answerList) - 1)
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
            index = randint(0, len(answerList) - 1)
            # index = 0
            strSkuList.append(answerList[index]['answerId'])
            strSkuDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'

        print(strSkuList, strCheckList)
        return strSkuList, strSkuDesc, strCheckList, strCheckDesc

    def v3_recycle_eva(self):
        pass


# 【价格3.0】定价选项获取销售价
class V3BaseGetSalePrice:

    def v3_sale_apply_price(self):
        pass


# 【价格3.0】检测模板获取销售价
class V3DetectGetSalePrice:

    def v3_sale_eva(self):
        pass


if __name__ == '__main__':
    eva = V3EvaPrice()
    recycle = V3DetectGetRecyclePrice()
    base_sale = V3BaseGetSalePrice()
    detect_sale = V3DetectGetSalePrice()

    # eva.v3_eva_option_get(product_id="41567", channel_id="10000060", pid="1260", get_way="1", is_best="1")
    # eva.v3_eva(product_id="41567", channel_id="10000060", pid="1260")

    recycle.v3_product_check_item(product_id="41567", order_id="7637141", check_type="3", is_over="1")

    # for x in range(500):
    #     eva.v3_eva_option_get(product_id="41567", channel_id="10000060", pid="1260", get_way="2")
