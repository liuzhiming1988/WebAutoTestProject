#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 估价服务 - 13-获取产品历史配置选项  -  insured_his_options - http://wiki.huishoubao.net/index.php?s=/138&page_id=2422
    入参：productId：产品Id  |  evaPlatform：估价平台  |  propertyFlag：属性标记  |  evaVersion：平台估价版本
        operEvaVersion：运营估价版本  | uniVersion：标准估价版本  | evaluateId：估价Id，优先使用估价Id，未传递估价ID或估价ID查不到信息再使用以上6个参数查询
    出参：itemList：选项列表  |  conftype：选项类型  |  desc：选项描述  |  id：选项ID  |  name：选项名称  |  parent_item：选项父Id
        question：问题项列表  |  show：表示前端页面是否显示该答案项，1-显示。0-或不存在不显示
        show_level：显示层级，1-级为问题级，2-级位答案级  |  seq_num：顺序号
'''

import requests, json, os
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print, hsb_eva_ipProxy_k8s_test


def insured_his_options(evaluateId, productId="",evaPlatform="",evaVersion="",operEvaVersion="",uniVersion=""):
    param = {"head":{"interface":"insured_his_options","msgtype":"request","remark":"","version":"0.01"},"params":{"productId":productId,"evaPlatform":evaPlatform,"propertyFlag":"0","evaVersion":evaVersion,"operEvaVersion":operEvaVersion,"uniVersion":uniVersion,"evaluateId":evaluateId}}

    headers = {"Content-Type":"application/json"}
    url = "http://evaserver.huishoubao.com/rpc/insured"
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_k8s_test())
    # print(respone.text)
    hsb_response_print(respone=respone)


if __name__ == '__main__':
    # insured_his_options(productId='',evaPlatform='',evaVersion='',operEvaVersion='',uniVersion='',evaluateId='')
    # insured_his_options(productId='41567',evaPlatform='1',evaVersion='0',operEvaVersion='0',uniVersion='0',evaluateId='0')
    # insured_his_options(productId='41567',evaPlatform='1',evaVersion='1',operEvaVersion='0',uniVersion='0',evaluateId='0')
    # insured_his_options(productId='41567',evaPlatform='2',evaVersion='1',operEvaVersion='0',uniVersion='0',evaluateId='0')
    # insured_his_options(productId='41567',evaPlatform='10',evaVersion='50',operEvaVersion='0',uniVersion='0',evaluateId='0')
    # insured_his_options(productId='41567',evaPlatform='',evaVersion='',operEvaVersion='',uniVersion='',evaluateId='21041740195')
    # insured_his_options(productId='41567',evaPlatform='',evaVersion='',operEvaVersion='',uniVersion='',evaluateId='202104281412')
    # insured_his_options(productId='41567',evaPlatform='1',evaVersion='297',operEvaVersion='0',uniVersion='0',evaluateId='0')
    insured_his_options(evaluateId="21121150")

'''
rpc_insured_server
select Fevaluate_item, Fstandard_price, Fmin_price, Fproduct_id, Fproduct_item, Fshow_item, Fsku_map from t_eva_pditems_history  where Fplatform_type = 1 and Fproduct_id = 41567 and Fversion = 297 limit 1
'''