#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : v2_solution_detect.py
@Author  : liuzhiming
@Time    : 2021/10/22 9:39
"""
import requests
import json
import os
from random import randint
from price.hsb_MD5_Enerypt import get_price_headers, res_print
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test, hsb_ordserver_ipProxy_test
import operator

"""
【适用价格2.0】
解决问题：检测时返回提示“获取产品保价估价选项失败,建议排查订单id是否存在”
解决步骤：
1. 使用本脚本，传入orderId
2. 返回两个sql，使用第一个sql查询出此机型的估价历史版本信息
3. 复制最近的一个版本为 Insert语句
4. 修改Insert语句中，版本号为第二个sql查询条件中的版本号，然后执行
5. 第二个sql执行后能返回记录，说明问题已解决，可以成功进行检测
（sql需要在价格VPC环境的recycle数据库中执行）
问题原因：
同步线上数据后，订单ID中的估价版本信息与测试环境中不一致导致
"""


class DetectIssue:
    @staticmethod
    def get_order_info(order_id):  # 从订单信息中拿到productId、evaluateId
        """"""
        url = "http://ordserver.huishoubao.com/order_center/getOrderInfo"
        param = {"_head": {"_callerServiceId": "216009", "_groupNo": "1", "_interface": "getOrderInfo",
                           "_invokeId": "92847505a83371e99119f52157e8b0bf", "_msgType": "request", "_remark": "",
                           "_timestamps": "1634866297", "_version": "0.01"},
                 "_param": {"containInfo": ["good", "basic", "evaluation"], "orderId": order_id}}
        res = requests.post(url, json=param, headers=get_price_headers(param), proxies=hsb_ordserver_ipProxy_test())
        res_print(res, 1)
        # print(param)
        res_dict = res.json()
        if res_dict["_data"]["_retinfo"] == "success":
            property = res_dict["_data"]["_data"]["basic"]["orderProperty"]
            evaluation = res_dict["_data"]["_data"]["evaluation"]
            print("订单属性：{}\n".format(property))
            print("获取的价格信息为：{}".format(evaluation))
            return evaluation
        else:
            return False

    def get_eva_info(self, eva_id):  # 根据evaluateId 获取估价信息，返回platform_type和version信息
        pass

    @staticmethod
    def format_sql_out(product_id, platform_type, version):  # 根据 productId  platform_type和version  格式化输出sql，拿到sql去数据库添加对应的历史版本信息
        # print("\nselect * from t_eva_pditems_history  where Fplatform_type = {} and Fproduct_id = {} ORDER BY Fupdate_time DESC LIMIT 5;\n".format(platform_type, product_id))
        # print("select Fevaluate_item, Fstandard_price, Fmin_price, Fproduct_id, Fproduct_item, Fshow_item, Fsku_map from t_eva_pditems_history  where Fplatform_type = {} and Fproduct_id = {} and Fversion = {} limit 1;".format(platform_type, product_id, version))

        insert_sql = """INSERT INTO `recycle`.`t_eva_pditems_history`(
                `Fplatform_type`, `Fproduct_id`, `Fstandard_price`, `Fmax_price`, `Fmin_price`, `Falgorithm_id`, 
                `Fevaluate_item`, `Fdelete_flag`, `Fproduct_item`, `Fshow_item`, `Foperator_name`, `Fsku_map`, 
                `Fitem_group`, `Fitem_add_sub`, `Falgorithm_order`, `Fall_combination_price`, `Fcreate_time`, 
                `Fupdate_time`,`Fversion`)  (select Fplatform_type, Fproduct_id, Fstandard_price, Fmax_price, 
                Fmin_price, Falgorithm_id, Fevaluate_item, Fdelete_flag, Fproduct_item, Fshow_item, Foperator_name, 
                Fsku_map, Fitem_group, Fitem_add_sub, Falgorithm_order, Fall_combination_price, Now(), Now(), {} from 
                t_eva_pditems_history  where Fplatform_type = {} and Fproduct_id = {} ORDER BY Fupdate_time DESC LIMIT 1)
            """.format(version, platform_type, product_id)
        print("======>Format | Insert语句为：\n{}".format(insert_sql))
        return insert_sql


if __name__ == '__main__':
    from utils.mysql_client import MysqlClient
    di = DetectIssue()
    evaluation = di.get_order_info(order_id="7638650")
    sql = di.format_sql_out(evaluation["productId"], evaluation["evaPlatform"], evaluation["evaluateVersion"])
    vpc_price_mysql_client = MysqlClient(
        host="193.112.170.216",
        port=3306,
        username="eva",
        password="evao123456",
        database="recycle"
    )
    vpc_price_mysql_client.insert(sql)

