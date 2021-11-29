#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 估价服务 - 12-获取估价记录信息接口  -  http://wiki.huishoubao.com/web/#/138?page_id=2273
    1.估价查询服务（wiki项目：产品服务）：eva_query
	2.对应服务 server-evaluate_query（服务器应用名：server-evaluate_query）
    3.对应URL： http://codserver.huishoubao.com

    出参：pid	是，pid | tagId：是，平台标识tagid | channelId：是，渠道ID | userId：是，用户ID | productId：是，产品ID | platform：是，估价平台标识
        evaVersion：是，估价版本 | userItem：是，用户估价选项 | evaPrice：是，估价价格 | operEvaVersion：是，运营估价版本 | operEvaPrice：是，运营估价价格
        spAllowance：是，运营商补贴 | selfAllowance：是，利润补贴 | allowanceType：是，补贴类型 | spProfit：是，运营商补贴金额 | selfProfit：是，利润补贴金额
        lastQuote：是，最后报价金额 | propertyFlag：是，属性,位操作进行设置,估价、运营、补贴等 | createTime：是，创建时间 | unifiedPrice：是，公司标准估价价格
        unifiedVersion：是，公司标准估价版本 | additionPrice：是，渠道加成价格 | additionVersion：是，渠道加成版本 | itemGroupLevel：是，选项分组等级
        itemTemplateId：是，选项模板id

    备注：evaluateId 估价id： SELECT * FROM recycle.t_eva_record_2001 b;   表中   2001+Fid 即为估价id '''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_k8s_test,hsb_response_print

def get_eva_record(evaluateId):
    param = {"_head":{"_interface":"get_eva_record","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"1525332832","_invokeId":"eva_vpc_k8s_zhangjinfa","_callerServiceId":"212011","_groupNo":"1"},"_param":{"evaluateId":evaluateId}}

    secret_key = "cfd7fabf8b7ca4602b3768ccd7440da4"
    callerserviceid = "212011"
    # eva_query 估价查询服务
    url = "http://evaserver.huishoubao.com/eva_query/get_eva_record"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_k8s_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # get_eva_record(evaluateId="191132222") #价格2.0
    # get_eva_record(evaluateId="20104607") #价格2.0
    # get_eva_record(evaluateId="2011236885") #价格2.0
    # get_eva_record(evaluateId="") #价格2.0
    # get_eva_record(evaluateId="211060937") #价格2.0
    # get_eva_record(evaluateId="2106118278") #价格2.0
    # get_eva_record(evaluateId="82111279") #价格3.0
    get_eva_record(evaluateId="921112164369")
