#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : v3_get_base_item.py
@Author  : liuzhiming
@Time    : 2021/10/22 11:23
"""
import requests
import json
import os
from random import randint
from price.hsb_MD5_Enerypt import get_price_headers, res_print
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test, hsb_response_print
import operator

"""
http://wiki.huishoubao.com/web/#/138?page_id=16189
获取检测选项库信息
http://prdserver.huishoubao.com/base_product_v3/get_base_item
默认返回已启用的问题项和答案项


"""


def v3_get_base_item(class_id, que_name="", index="0", size="10"):
    """获取检测选项库信息"""
    url = "http://prdserver.huishoubao.com/base_product_v3/get_base_item"
    param = {"_head": {"_interface": "get_base_item", "_msgType": "request", "_remark": "","_version": "0.01",
                       "_timestamps": "1632448718","_invokeId": "16324487181227","_callerServiceId": "212011","_groupNo": "1"},
             "_param": {
                 "classId": class_id,
                 "queName": que_name,
                 "pageIndex": index,
                 "pageSize": size
             }
             }
    res = requests.post(url, json=param, headers=get_price_headers(param), proxies=hsb_eva_ipProxy_test())
    res_print(res, "2")  # 打印输出响应结果，非1数字打印json格式
    res_dict = res.json()
    if res_dict["_data"]["_errCode"] == "0":
        print("返回问题项数量：{}个".format(len(res_dict["_data"]["_data"]["itemList"])))


if __name__ == '__main__':

    # v3_get_base_item(class_id="1", que_name="维修")   # 按问题项模糊搜索
    # v3_get_base_item(class_id="100234", que_name="")  # 不存在的类目ID
    # v3_get_base_item(class_id="1", que_name="")  # 查询手机类目所有问题项
    # v3_get_base_item(class_id="1", que_name="", index="0", size="50")  # 每页数量是否正确
    v3_get_base_item(class_id="1", que_name="", index="1", size="20")  # 获取第二页数据是否正确
    # v3_get_base_item(class_id="", que_name="", index="1", size="50")  # 类目ID为空，给出提示【请求参数错误 [ClassId为必填字段]】
