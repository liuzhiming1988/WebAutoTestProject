#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 13.选项库答案项搜索接口 - http://wiki.huishoubao.com/index.php?s=/105&page_id=1873  -  base_product
    入参：classId：类目，不同类目有不同的选项库，1-手机，2-笔记本，3-平板，5-智能手表
        platformType：平台，某些平台对某些选项不可见，1.2C 2.2B 3.微回收 4.转转 5.vivo 6.闲鱼验机
        questionId：问题项ID，可传递多个，以#号分割，例如 91#675#31  |  keyword，关键词，会匹配答案项名称和答案项描述
        answerId：答案项id，可传递多个，以#号分割，例如 1#19#98#90  |  valid：答案项有效无效标记，1-有效，2-无效，3-不限制，不传默认为筛选有效
        parentId：父级ID  |  pageIndex：分页的页码，获取分页数据时，值不能为空，代表当前的页码，从1开始
        pageSize：每页的数据量，获取分页数据时，值不能为空，代表每页数据量，最大500个
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def options_answer_get(classId, platformType, answerId, questionId, keyword):
    param = { "_head":{ "_interface":"options_answer_get", "_msgType":"request", "_remark":"hello", "_version":"0.01",
                        "_timestamps":"123", "_invokeId":"111", "_callerServiceId":"112002", "_groupNo":"1" },
              "_param":{ "pageIndex":"0", "pageSize":"100", "classId":classId, "platformType":platformType, "answerId": answerId,"questionId":questionId, "keyword":keyword } }

    secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
    callerserviceid = "112002"
    url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)
    respone_dict = json.loads(respone.text)  # 转成字典
    item_list = respone_dict["_body"]["_data"]["list"]   # 返回的选项列表
    select_list = []     # 选中列表
    if item_list:
        for item in item_list:
            aId, qId = item["aId"],item["qId"]
            item_dict = {"aId": aId, "qId": qId}
            select_list.append(item_dict)
    print("选中选项为：\n{}".format(select_list))


if __name__ == '__main__':
    # options_answer_get(classId='1', platformType='', questionId='11', keyword='')
    # options_answer_get(classId='', platformType='', questionId='', keyword='')
    # options_answer_get(classId='1', platformType='', questionId='', keyword='')
    # options_answer_get(classId='1', platformType='1', questionId='', keyword='')
    # options_answer_get(classId='1', platformType='1', questionId='1', keyword='')
    # options_answer_get(classId='1', platformType='1', questionId='', keyword='屏幕')
    # options_answer_get(classId='1', platformType='', questionId='2169', keyword='')
    # options_answer_get(classId='1', platformType='', questionId='2169', keyword='未更换')
    # options_answer_get(classId='1', platformType='', questionId='20210326', keyword='')

    a_id = "21#23#55#59#65#223#1078#3246#2171#5535#6931#7641"
    options_answer_get(classId='1', platformType='', answerId=a_id, questionId='', keyword='')
