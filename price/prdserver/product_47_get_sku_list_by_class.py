#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 47.产品SKU基础信息分类拉取（新）  -   http://wiki.huishoubao.com/web/#/105?page_id=12269
    1。对应服务：server-base_product（base_product） | 2。对应URL http://prdserver.huishoubao.com

    入参：classId：类目id（必填） | needAns：1-是，0-否，是否需要返回答案项，默认为1（非必填） | valid：1-有效，0-无效，传空或不传表示不限制（非必填）
        pageIndex：分页，下标，从0开始（必填） |  pageSize：分页，大小，最大1000（必填） | keyword：SKU名称搜索  （非必填）
    出参：classId：类目Id | className：类目名称 | itemList：返回的SKU信息数组 | itemList.id：sku问题Id | itemList.name：sku问题名称 | itemList.childs：答案项信息
        itemList.childs.id：sku答案项id | itemList.childs.name：sku答案项名称 | itemList.childs.valid：SKU答案项有效值，1-有效，0-无效
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def get_sku_list_by_class(classId, needAns, keyword, valid):
    param = {"_head":{"_interface":"get_sku_list_by_class","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"","_invokeId":"","_callerServiceId":"112002","_groupNo":"1"},"_param":{"classId":classId, "needAns":needAns, "keyword":keyword, "valid":valid }}
    secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
    callerserviceid = "112002"
    url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # get_sku_list_by_class(classId='', needAns='', keyword='', valid='')
    # get_sku_list_by_class(classId='1', needAns='', keyword='', valid='')
    # get_sku_list_by_class(classId='2', needAns='', keyword='', valid='')
    get_sku_list_by_class(classId='10', needAns='', keyword='', valid='')
    # get_sku_list_by_class(classId='1', needAns='0', keyword='', valid='')
    # get_sku_list_by_class(classId='1', needAns='1', keyword='大陆国行', valid='')
    # get_sku_list_by_class(classId='1', needAns='1', keyword='', valid='0')
    # get_sku_list_by_class(classId='1', needAns='0', keyword='', valid='0')
    # get_sku_list_by_class(classId='1', needAns='1', keyword='', valid='')  # t_pdt_class_sku_map 表数据为空，返回"itemList":[] 为空
    # get_sku_list_by_class(classId='1', needAns='1', keyword='', valid='')  # 正常场景，valid='' 传空  或者  不传valid
    # get_sku_list_by_class(classId='1', needAns='0', keyword='', valid='1')
    # get_sku_list_by_class(classId='1', needAns='1', keyword='', valid='1')  # 正常场景，valid='1'（指问题项的状态）
    # get_sku_list_by_class(classId='1', needAns='1', keyword='', valid='0')  # 正常场景，valid='0' （指问题项的状态）
    # get_sku_list_by_class(classId='1', needAns='', keyword='', valid='1')  # 正常场景，needAns='1' 或者 不传needAns，默认为1
    # get_sku_list_by_class(classId='1', needAns='0', keyword='', valid='0')  # 正常场景，needAns='0' （不展示答案项）
    # get_sku_list_by_class(classId='1', needAns='1', keyword='大陆国行', valid='1')  # 正常场景，keyword='大陆国行' （搜索的是目标答案项）
    # get_sku_list_by_class(classId='1', needAns='1', keyword='大陆国行', valid='1')  # 正常场景，keyword='大陆国行' （搜索的是目标答案项）
    # get_sku_list_by_class(classId='1', needAns='1', keyword='', valid='0')  # t_pdt_class_sku_map 表只有classID为1的数据，入参 classId='2'
    # get_sku_list_by_class(classId='1', needAns='1', keyword='', valid='0')  # classId='1' 手机，但是录入的sku问题项id是笔记本类目的（正常返回，此场景暂不考虑）

'''
注意：现在入参中的 valid='1'     只控制问题项的状态，需要返回答案项时，答案项的状态在程序中过滤，只返回’有效‘状态的答案项
场景1：问题项-启用，答案项-禁用；   needAns='1',  valid='1'   返回问题项
场景2：问题项-启用，无答案项；      needAns='1',  valid='1'   返回问题项

 {"_body":{"_data":{"classId":"1","className":"手机","itemList":[{"childs":[{"id":"12","name":"大陆国行","valid":"1"},{"id":"13","name":"香港行货","valid":"1"},{"id":"14","name":"其他国家地区-无锁版","valid":"1"},{"id":"15","name":"其他国家地区-有锁版","valid":"1"}],"id":"11","name":"购买渠道"},{"childs":[{"id":"17","name":"保修一个月以上","valid":"1"},{"id":"18","name":"保修一个月以内或过保","valid":"1"}],"id":"16","name":"保修期"},{"childs":[{"id":"27","name":"非官换机","valid":"2"},{"id":"28","name":"官换机","valid":"2"}],"id":"26","name":"官换机"},{"childs":[{"id":"33","name":"8GB","valid":"1"},{"id":"34","name":"16GB","valid":"1"}],"id":"32","name":"存储容量"}],"pageInfo":{"pageIndex":"0","pageSize":"10","total":"1785"}},"_ret":"0","_retcode":"0","_retinfo":"成功"},"_head":{"_callerServiceId":"112002","_groupNo":"1","_interface":"get_sku_list_by_class","_invokeId":"9b1adc8f-4ee2-4afa-91b2-adc74eca4dc2","_msgType":"response","_remark":"","_timestamps":"1599708225","_version":"0.01"}}
'''