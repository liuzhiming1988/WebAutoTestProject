#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 估价服务 - 估价3.0 - 5.检测模板获取销售价  - http://wiki.huishoubao.com/web/#/138?page_id=15853
    入参：planId：方案id，111 …  |  productId：产品机型id	41567 …	是
        checkType：检测类型、检测场景，例如顺丰上门场景，或是闲鱼验机场景	1,2	是
        optItem：机况答案选项id  |  skuItem：标准sku答案选项id  |  userId：检测人
        ip：用户IP  |  freqLimitType：频率限制类型，0-不限制、1-IP、2-UserId	0 1 2 （外部对到用户端系统，建议增加限频；内部系统可以不限频）
    出参：evaBasePrice：销售定价价格 单位:分
        sellerPrice：卖家参考价 单位:分
        sellerMaxPrice：卖家最高价考价 单位:分
        buyerPrice：买家参考价 单位:分
        recordId：估价唯一id（id 会超过int(11)，请不要用int保存）（可通过：24 获取定价估价记录接口，获取信息）
        levelId：价格3.0-定价等级id  |  levelName：价格3.0-定价等级名称
        saleLevelId：价格3.0-销售等级id （价格2.0为空）  |  saleLevelName：价格3.0-销售等级名称 （价格2.0为空）
        baseLevelTag：价格3.0-定价等级标签
            baseLevelTag.tagId：定价等级标签id  |  baseLevelTag.tagName：定价等级标签名称
        saleLevelTag：价格3.0-销售等级标签
            saleLevelTag.tagId：销售等级标签id  |  saleLevelTag.tagName：销售等级标签名称
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def v3_sale_evaluate(planId, productId, checkType, skuItem, optItem, freqLimitType, ip):
    param = {"_head":{"_interface":"sale_evaluate","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"1525332832","_invokeId":"152533283241636","_callerServiceId":"216002","_groupNo":"1"},"_param":{"planId":planId, "productId":productId, "checkType":checkType,"optItem":optItem, "skuItem":skuItem, "userId":"1895", "freqLimitType":freqLimitType, "ip":ip}}
    secret_key = "rAfnRwyWfh2N9vXVgWwdpJxaXgOCd8af"
    callerserviceid = "216002"
    url = "http://codserver.huishoubao.com/detect_v3/sale_evaluate"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    respone.encoding = respone.apparent_encoding  # 编码设置
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # 1. 正常场景
    # v3_sale_evaluate(planId='10', productId='41567', checkType='16', skuItem=['12', '18', '38', '1091', '130', '2241', '2236'], optItem=['8162','8351','8359','8148','8173','8323','8315','8090','8290','8101'], freqLimitType='1', ip='127.0.0.1')

    # 2. 检测方式传空  |  "_errStr":"请求参数错误 [CheckType为必填字段]","_errCode":"70023100"
    # v3_sale_evaluate(planId='10', productId='41567', checkType='', skuItem=['12', '18', '38', '1091', '130', '2241', '2236'], optItem=['8162','8351','8359','8148','8173','8323','8315','8090','8290','8101'], freqLimitType='1', ip='127.0.0.1')

    # 3. 传的检测方式ID  不存在 | "_errStr":"销售估价失败 [数据库没有查询到检测类型[20210831]信息]", "_errCode":"70023303"
    # v3_sale_evaluate(planId='10', productId='41567', checkType='20210831', skuItem=['12', '18', '38', '1091', '130', '2241', '2236'], optItem=['8162','8351','8359','8148','8173','8323','8315','8090','8290','8101'], freqLimitType='1', ip='127.0.0.1')

    # 4. 检测方式未关联 检测模板 | "_errStr":"销售估价失败 [检测方式[10]未关联检测模板]","_errCode":"70023303"
    # v3_sale_evaluate(planId='10', productId='41567', checkType='10', skuItem=['12', '18', '38', '1091', '130', '2241', '2236'], optItem=['8162','8351','8359','8148','8173','8323','8315','8090','8290','8101'], freqLimitType='1', ip='127.0.0.1')

    # 5. 检测方式被禁用 | "_errStr":"销售估价失败 [检测类型为禁用状态]" | "_errCode":"70023303"
    # v3_sale_evaluate(planId='10', productId='41567', checkType='11', skuItem=['12', '18', '38', '1091', '130', '2241', '2236'], optItem=['8162','8351','8359','8148','8173','8323','8315','8090','8290','8101'], freqLimitType='1', ip='127.0.0.1')

    # 6. 机型 未命中任何 检测子模板 | "_errStr":"销售估价失败 [机型[41567]没有查询到检测子模板信息]","_errCode":"70023303"
    # v3_sale_evaluate(planId='10', productId='41567', checkType='16', skuItem=['12', '18', '38', '1091', '130', '2241', '2236'], optItem=['8162','8351','8359','8148','8173','8323','8315','8090','8290','8101'], freqLimitType='1', ip='127.0.0.1')

    # 7. 只命中 “配置方式：按操作系统配置” 的检测子模板
    # v3_sale_evaluate(planId='10', productId='41567', checkType='16', skuItem=['12', '18', '38', '1091', '130', '2241', '2236'], optItem=['8162','8351','8359','8148','8173','8323','8315','8090','8290','8101'], freqLimitType='1', ip='127.0.0.1')

    # 8. 同时命中 “配置方式：按机型配置” 和 “配置方式：按操作系统配置” 的检测子模板； 优先取  “配置方式：按机型配置”  的配置
    # v3_sale_evaluate(planId='10', productId='41567', checkType='16', skuItem=['12', '18', '38', '1091', '130', '2241', '2236'], optItem=['8162','8351','8359','8148','8173','8323','8315','8090','8290','8101'], freqLimitType='1', ip='127.0.0.1')

    # 9. 只命中 “配置方式：按机型配置” 的检测子模板
    # v3_sale_evaluate(planId='10', productId='41567', checkType='16', skuItem=['12', '18', '38', '1091', '130', '2241', '2236'], optItem=['8162','8351','8359','8148','8173','8323','8315','8090','8290','8101'], freqLimitType='1', ip='127.0.0.1')

    # 10. 销售价应用方案ID传空 | "_errStr":"请求参数错误 [PlanId为必填字段]","_errCode":"70023100"
    # v3_sale_evaluate(planId='', productId='41567', checkType='16', skuItem=['12', '18', '38', '1091', '130', '2241', '2236'], optItem=['8162','8351','8359','8148','8173','8323','8315','8090','8290','8101'], freqLimitType='1', ip='127.0.0.1')

    # 11. 销售价应用方案ID 不存在 | "_errStr":"销售估价失败 [未查询到调价方案数据]","_errCode":"70023303"
    # v3_sale_evaluate(planId='20210831', productId='41567', checkType='16', skuItem=['12', '18', '38', '1091', '130', '2241', '2236'], optItem=['8162','8351','8359','8148','8173','8323','8315','8090','8290','8101'], freqLimitType='1', ip='127.0.0.1')

    # 12. 销售价应用方案 禁用状态 | "_errStr":"销售估价失败 [禁用状态的销售价应用方案]","_errCode":"70023303"
    # v3_sale_evaluate(planId='19', productId='41567', checkType='16', skuItem=['12', '18', '38', '1091', '130', '2241', '2236'], optItem=['8162','8351','8359','8148','8173','8323','8315','8090','8290','8101'], freqLimitType='1', ip='127.0.0.1')

    # 13. 销售价应用方案为空 | "evaBasePrice":"345800","sellerPrice":"0","sellerMaxPrice":"0","buyerPrice":"0"
    # v3_sale_evaluate(planId='18', productId='41567', checkType='16', skuItem=['12', '18', '38', '1091', '130', '2241', '2236'], optItem=['8162','8351','8359','8148','8173','8323','8315','8090','8290','8101'], freqLimitType='1', ip='127.0.0.1')

    # 14. 销售价应用方案不为空，机型未命中销售价应用方案 规则 | "evaBasePrice":"345800","sellerPrice":"0","sellerMaxPrice":"0","buyerPrice":"0"
    # v3_sale_evaluate(planId='17', productId='41567', checkType='16', skuItem=['12', '18', '38', '1091', '130', '2241', '2236'], optItem=['8162','8351','8359','8148','8173','8323','8315','8090','8290','8101'], freqLimitType='1', ip='127.0.0.1')

    # 15. sku传空 | "_errStr":"销售估价失败 [SKU个数错误: U[0] P[7]]","_errCode":"70023303"
    # v3_sale_evaluate(planId='10', productId='41567', checkType='16', skuItem=[], optItem=['8162','8351','8359','8148','8173','8323','8315','8090','8290','8101'], freqLimitType='1', ip='127.0.0.1')

    # 16. sku少传，单个问题项多传 | "_errStr":"销售估价失败 [SKU个数错误: U[6] P[7]]" | "_errStr":"销售估价失败 [SKU个数错误: U[8] P[7]]"
    # v3_sale_evaluate(planId='10', productId='41567', checkType='16', skuItem=['12', '18', '38', '1091', '130', '2241'], optItem=['8162','8351','8359','8148','8173','8323','8315','8090','8290','8101'], freqLimitType='1', ip='127.0.0.1')
    # v3_sale_evaluate(planId='10', productId='41567', checkType='16', skuItem=['12', '13', '18', '38', '1091', '130', '2241', '2236'], optItem=['8162','8351','8359','8148','8173','8323','8315','8090','8290','8101'], freqLimitType='1', ip='127.0.0.1')

    # 17. 机况不传 |  拿 定价标准里，各选项的默认项  |  "_errStr":"请求参数错误 [OptItem必须至少包含1项]","_errCode":"70023100"
    # v3_sale_evaluate(planId='10', productId='41567', checkType='16', skuItem=['12', '18', '38', '1091', '130', '2241', '2236'], optItem=[], freqLimitType='1', ip='127.0.0.1')

    # 18. 机况少传 | 入参选项转成定价标准选项，未传的 拿 定价标准里，各选项的默认项
    # v3_sale_evaluate(planId='10', productId='41567', checkType='16', skuItem=['12', '18', '38', '1091', '130', '2241', '2236'], optItem=['8351'], freqLimitType='1', ip='127.0.0.1')

    # 19. 来源-定价标准选项，单选项传了多个 | 拿 定价标准里 这两个选项 优先级更低的那个
    # v3_sale_evaluate(planId='10', productId='41567', checkType='16', skuItem=['12', '18', '38', '1091', '130', '2241', '2236'], optItem=['8162',  '8351','8353',  '8359','8148','8173','8323','8315','8090','8290','8101'], freqLimitType='1', ip='127.0.0.1')

    # 20. 来源-质检标准选项，单选项传了多个 | 将入参选项转换成定价标准选项，如果对应的定价标准选项有多个，拿 定价标准里 这多个选项 优先级更低的那个
    # v3_sale_evaluate(planId='10', productId='41567', checkType='16', skuItem=['12', '18', '38', '1091', '130', '2241', '2236'], optItem=['8162','8163',  '8351', '8359','8148','8173','8323','8315','8090','8290','8101'], freqLimitType='1', ip='127.0.0.1')

    # 21. 来源-定价标准选项，多选项传了多个  |  都带（去匹配价格等级标准）
    # v3_sale_evaluate(planId='10', productId='41567', checkType='16', skuItem=['12', '18', '38', '1091', '130', '2241', '2236'], optItem=['8162', '8351', '8359','8148',  '8379','8380',  '8323','8315','8090','8290','8101'], freqLimitType='1', ip='127.0.0.1')

    ''' 22. 来源-质检标准选项，多选项传了多个 |  将入参选项转换成定价标准选项，如果对应的定价标准选项有多个，拿 定价标准里 这多个选项 优先级更低的那个'''
    '''22.1. 同时命中了多选项的答案项，单选项的答案项 | 单选的优先级，同时低于多选的优先级，最终命中单选'''
    # checkOpt:   [8162（质检） 8351（定价） 8359（定价） 8148（质检） 8378（定价） 8323（定价） 8315（定价）  8090（质检） 8291 8292 8293 8101]
    # baseStanOpt:[8371（定价） 8351（定价） 8359（定价） 8361（定价） 8378（定价） 8323（定价） 8315（定价）  8308（定价） ]
    # v3_sale_evaluate(planId='10', productId='41567', checkType='16', skuItem=['12', '18', '38', '1091', '130', '2241', '2236'], optItem=['8162','8351','8359','8148','8378','8323','8315',  '8090','8291','8292','8293','8101'], freqLimitType='1', ip='127.0.0.1')

    '''22.2. 同时命中了多选项的答案项，单选项的答案项 | 单选的优先级，同时高于多选的优先级，最终命中多选'''
    # checkOpt:   [8162（质检） 8351（定价） 8359（定价） 8148（质检） 8378（定价） 8323（定价） 8315（定价）  8090（质检） 8291 8292 8293 8101]
    # baseStanOpt:[8371（定价） 8351（定价） 8359（定价） 8361（定价） 8378（定价） 8323（定价） 8315（定价）  8313（定价） 8310 8309 ]
    # v3_sale_evaluate(planId='10', productId='41567', checkType='16', skuItem=['12', '18', '38', '1091', '130', '2241', '2236'], optItem=['8162','8351','8359','8148','8378','8323','8315',  '8090','8291','8292','8293','8101'], freqLimitType='1', ip='127.0.0.1')

    '''22.3. 同时命中了多选项的答案项，单选项的答案项 | 单选的优先级，比有的多选项高，也比有的多选项低，最终命中多选'''
    # checkOpt:   [8162（质检） 8351（定价） 8359（定价） 8148（质检） 8378（定价） 8323（定价） 8315（定价）  8090（质检） 8291 8292 8293 8101]
    # baseStanOpt:[8371（定价） 8351（定价） 8359（定价） 8361（定价） 8378（定价） 8323（定价） 8315（定价）  8313（定价） 8310 8309 ]
    # v3_sale_evaluate(planId='10', productId='41567', checkType='16', skuItem=['12', '18', '38', '1091', '130', '2241', '2236'], optItem=['8162', '8351', '8359', '8148', '8378', '8323', '8315',   '8090', '8291', '8292', '8293', '8101'], freqLimitType='1', ip='127.0.0.1')

    '''22.3. 同时命中了多选项的答案项，（有2个）单选属性的答案项 | 单选的优先级，同时低于多选的优先级，最终命中（优先级小的）单选'''
    # checkOpt:   [8162（质检） 8351（定价） 8359（定价） 8148（质检） 8378（定价） 8323（定价） 8315（定价） 8090（质检） 8291 8292 8293 8101]
    # baseStanOpt:[8371（定价） 8351（定价） 8359（定价） 8361（定价） 8378（定价） 8323（定价） 8313（定价） 8309（定价） ]
    # v3_sale_evaluate(planId='10', productId='41567', checkType='16', skuItem=['12', '18', '38', '1091', '130', '2241', '2236'], optItem=['8162', '8351', '8359', '8148', '8378', '8323', '8315',   '8090', '8291', '8292', '8293', '8101'], freqLimitType='1', ip='127.0.0.1')

    '''22.4. 同时命中了多选项的答案项，（有2个）单选属性的答案项 | 单选的优先级，同时高于多选的优先级，最终命中多选'''
    # checkOpt:   [8162（质检） 8351（定价） 8359（定价） 8148（质检） 8378（定价） 8323（定价） 8315（定价） 8090（质检） 8291 8292 8293 8101]
    # baseStanOpt:[8371（定价） 8351（定价） 8359（定价） 8361（定价） 8378（定价） 8323（定价） 8313（定价） 8313（定价） 8310 ]
    # v3_sale_evaluate(planId='10', productId='41567', checkType='16', skuItem=['12', '18', '38', '1091', '130', '2241', '2236'], optItem=['8162', '8351', '8359', '8148', '8378', '8323', '8315',   '8090', '8291', '8292', '8293', '8101'], freqLimitType='1', ip='127.0.0.1')

    '''22.5. 同时命中了多选项的答案项，（有2个）单选属性的答案项 | 单选的优先级，一个比部分多选的优先级高，一个比多选的优先级都低，最终命中（低的那个）单选'''
    # checkOpt:   [8162（质检） 8351（定价） 8359（定价） 8148（质检） 8378（定价） 8323（定价） 8315（定价） 8090（质检） 8291 8292 8293 8101]
    # baseStanOpt:[8371（定价） 8351（定价） 8359（定价） 8361（定价） 8378（定价） 8323（定价） 8313（定价） 8309（定价） ]
    # v3_sale_evaluate(planId='10', productId='41567', checkType='16', skuItem=['12', '18', '38', '1091', '130', '2241', '2236'], optItem=['8162', '8351', '8359', '8148', '8378', '8323', '8315',   '8090', '8291', '8292', '8293', '8101'], freqLimitType='1', ip='127.0.0.1')

    '''22.6. 同时命中了多选项的答案项，（有2个）单选属性的答案项 | （2个）单选的优先级，两个同时高于部分多选的优先级，且低于部分多选的优先级，最终命中多选'''
    # checkOpt:   [8162（质检） 8351（定价） 8359（定价） 8148（质检） 8378（定价） 8323（定价） 8315（定价） 8090（质检） 8291 8292 8293 8101]
    # baseStanOpt:[8371（定价） 8351（定价） 8359（定价） 8361（定价） 8378（定价） 8323（定价） 8313（定价） 8313（定价） 8310 ]
    v3_sale_evaluate(planId='10', productId='41567', checkType='16', skuItem=['12', '18', '38', '1091', '130', '2241', '2236'], optItem=['8162', '8351', '8359', '8148', '8378', '8323', '8315',   '8090', '8291', '8292', '8293', '8101'], freqLimitType='1', ip='127.0.0.1')

    # 23. 无sku机型 | 4157 华为 OPhone | 正常
    # v3_sale_evaluate(planId='10', productId='4157', checkType='16', skuItem=[], optItem=['8162','8351','8359','8148','8378','8323','8315','8090',   '8291','8292','8293',   '8101'], freqLimitType='1', ip='127.0.0.1')

    # 24. 销售定价-未定价状态机型 | "_errStr":"销售估价失败 [未定价状态机型]","_errCode":"70023303"
    # v3_sale_evaluate(planId='10', productId='4004', checkType='16', skuItem=[], optItem=['8162','8351','8359','8148','8378','8323','8315','8090',   '8291','8292','8293',   '8101'], freqLimitType='1', ip='127.0.0.1')

    # 25. 下架状态机型 | "_errStr":"销售估价失败 [产品为下架状态]"
    # v3_sale_evaluate(planId='10', productId='4007', checkType='16', skuItem=[], optItem=['8162','8351','8359','8148','8378','8323','8315','8090',   '8291','8292','8293',   '8101'], freqLimitType='1', ip='127.0.0.1')

    # 26. 切换version为2之后，有不少销售已定价状态的机型，实际上没有销售定价版本数据 | 4301 华为 C8818 | "_errStr":"销售估价失败 [获取产品选项系数配置失败]","_errCode":"70023303" | 正常
    # v3_sale_evaluate(planId='10', productId='4301', checkType='16', skuItem=[], optItem=['8162','8351','8359','8148','8378','8323','8315','8090',   '8291','8292','8293',   '8101'], freqLimitType='1', ip='127.0.0.1')


'''
【EvaluateCheckV3】 【前提：定价等级模板 要切换到 定价等级标准】
【价格3.0一期，B端寄卖切换会使用】

【入参】
{"_head": {"_interface": "sale_evaluate", "_msgType": "request", "_remark": "", "_version": "0.01", "_timestamps": "1525332832", "_invokeId": "152533283241636", "_callerServiceId": "216002", "_groupNo": "1"}, "_param": {"planId": "10", "productId": "41567", "checkType": "16", "optItem": ["8162", "8351", "8359", "8148", "8173", "8323", "8315", "8090", "8290", "8101"], "skuItem": ["12", "18", "38", "1091", "130", "2241", "2236"], "userId": "1895", "freqLimitType": "1", "ip": "127.0.0.1"}}
formParam: {PlanId:10 ProductId:41567 SkuItem:[12 18 38 1091 130 2241 2236] OptItem:[8162 8351 8359 8148 8173 8323 8315 8090 8290 8101] CheckType:16 UserId:1895 Ip:127.0.0.1 FreqLimitType:1}
rrdisCmd: hget V3EvaPrdCheckSubTemp t16-p41567: 48
redis checkSubTempId: 48

【根据 checkType='16'，得出关联的检测模板信息，同时得出配置了该机型的检测子模板信息】
rrdisCmd: hget V3EvaCheckSubTemplate 48: {"TemplateId":29,"SubTemplateId":48,"SubTemplateName":"29第一个子模板-按机型配置","Remarks":"29第一个子模板-按机型配置","SubTemplateVersion":2,"TemplateItem":[{"ItemType":8036,"Order":1,"ItemList":[{"Qid":8161,"Order":1,"Single":1,"Source":2,"Answer":[{"Aid":8164,"Order":1,"Single":1},{"Aid":8163,"Order":2,"Single":1},{"Aid":8162,"Order":3,"Single":1}]},{"Qid":8350,"Order":2,"Single":1,"Source":1,"Answer":[{"Aid":8355,"Order":1,"Single":1},{"Aid":8354,"Order":2,"Single":1},{"Aid":8353,"Order":3,"Single":1},{"Aid":8352,"Order":4,"Single":1},{"Aid":8351,"Order":5,"Single":1}]},{"Qid":8356,"Order":3,"Single":1,"Source":1,"Answer":[{"Aid":8359,"Order":1,"Single":1},{"Aid":8358,"Order":2,"Single":1},{"Aid":8357,"Order":3,"Single":1}]}]},{"ItemType":9581,"Order":2,"ItemList":[{"Qid":8147,"Order":1,"Single":1,"Source":2,"Answer":[{"Aid":8149,"Order":1,"Single":1},{"Aid":8148,"Order":2,"Single":1}]},{"Qid":8172,"Order":2,"Single":1,"Source":2,"Answer":[{"Aid":8177,"Order":1,"Single":1},{"Aid":8174,"Order":2,"Single":1},{"Aid":8175,"Order":3,"Single":1},{"Aid":8176,"Order":4,"Single":1},{"Aid":8173,"Order":5,"Single":1}]},{"Qid":8322,"Order":3,"Single":1,"Source":1,"Answer":[{"Aid":8324,"Order":1,"Single":1},{"Aid":8323,"Order":2,"Single":1}]}]},{"ItemType":9580,"Order":3,"ItemList":[{"Qid":8314,"Order":1,"Single":1,"Source":1,"Answer":[{"Aid":8317,"Order":1,"Single":1},{"Aid":8316,"Order":2,"Single":1},{"Aid":8315,"Order":3,"Single":1}]},{"Qid":8089,"Order":2,"Single":2,"Source":2,"Answer":[{"Aid":8095,"Order":1,"Single":2},{"Aid":8094,"Order":2,"Single":2},{"Aid":8093,"Order":3,"Single":2},{"Aid":8092,"Order":4,"Single":2},{"Aid":8091,"Order":5,"Single":2},{"Aid":8090,"Order":6,"Single":1}]},{"Qid":8289,"Order":3,"Single":2,"Source":2,"Answer":[{"Aid":8293,"Order":1,"Single":2},{"Aid":8294,"Order":2,"Single":2},{"Aid":8292,"Order":3,"Single":2},{"Aid":8291,"Order":4,"Single":2},{"Aid":8290,"Order":5,"Single":1}]},{"Qid":8100,"Order":4,"Single":1,"Source":2,"Answer":[{"Aid":8103,"Order":1,"Single":1},{"Aid":8102,"Order":2,"Single":1},{"Aid":8101,"Order":3,"Single":1}]}]}],"PriceStadId":16,"Status":1,"SpuType":2,"CreateTime":"2021-08-31T11:40:01.219Z","UpdateTime":"2021-08-31T11:40:14.066Z","UserName":"张金发_TEST"}

rrdisCmd: hget V3BasePriceStad 16: redis: nil
filter: map[Fid:map[$in:[16]] Fstatus:1]

SkuItem:[12 18 38 1091 130 2241 2236]
入参："optItem": ["8162", "8351", "8359", "8148", "8173", "8323", "8315", "8090", "8290", "8101"]
checkOpt（入参检测选项）:   [8162（质检） 8351（定价） 8359（定价） 8148（质检) 8173（质检） 8323（定价） 8315（定价） 8090（质检） 8290（质检） 8101（质检）]
baseStanOpt（定价标准选项）:[8371        8351       8359        8361       8378        8323       8315        8308]
rrdisCmd: get E_FL_TD_BPE_3: redis: nil

【根据 planId='10'，拿取销售价应用方案信息】
rrdisCmd: hget V3BasePriceProduct 41567: {"ProductId":41567,"ClassId":1,"BrandId":2,"OsType":1,"Status":1,"PriceState":1,"PauState":1,"RecycState":1,"SyncPriceState":1,"UserName":"陈亮","CreateTime":"2021-01-28T16:56:39Z","UpdateTime":"2021-01-28T16:56:39Z"}
baseProductInfo: {ProductId:41567 ClassId:1 BrandId:2 OsType:1 Status:1 PriceState:1 PauState:1 RecycState:1 SyncPriceState:1 UserName:陈亮 CreateTime:2021-01-28 16:56:39 +0000 UTC UpdateTime:2021-01-28 16:56:39 +0000 UTC}
rrdisCmd: hget V3SaleApplyPlan 10: redis: nil
Mgo query: map[Fid:map[$in:[10]]]
Mgo selector: map[]
Mgo result: [{PlanId:10 PlanName:071202测试方案008 Remarks: State:1 DelFlag:0 CreateTime:2021-07-12 17:13:50.872 +0000 UTC UpdateTime:2021-08-27 19:40:10.003 +0000 UTC UserName:张金发_TEST PlanVersion:3 PlanInfo:{SellerPrice:{ClassBranchPriceRule:[{ClassList:[1] BrandList:[1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28] PricePlusList:[{Begin:100 End:30000 Percent:-50 Absolute:0 Type:1 PriceType:2} {Begin:30100 End:100000 Percent:-20 Absolute:0 Type:1 PriceType:2} {Begin:100100 End:200000 Percent:-20 Absolute:0 Type:1 PriceType:2} {Begin:200100 End:9999900 Percent:-10 Absolute:0 Type:1 PriceType:2}]} {ClassList:[2] BrandList:[2] PricePlusList:[{Begin:100 End:999999900 Percent:110 Absolute:0 Type:1 PriceType:1}]} {ClassList:[3] BrandList:[2] PricePlusList:[{Begin:100 End:99999900 Percent:0 Absolute:900 Type:2 PriceType:2}]}] ProductRule:[{PrdId:41567 PrdAdjust:{Percent:110 Absolute:0 Type:1} SkuRule:[] CombRule:[]}]} SellerMaxPrice:{ClassBranchPriceRule:[{ClassList:[1] BrandList:[1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26] PricePlusList:[{Begin:100 End:30000 Percent:150 Absolute:0 Type:1 PriceType:2} {Begin:30100 End:100000 Percent:80 Absolute:0 Type:1 PriceType:2} {Begin:100100 End:200000 Percent:60 Absolute:0 Type:1 PriceType:2} {Begin:200100 End:9999900 Percent:40 Absolute:0 Type:1 PriceType:2}]}] ProductRule:[]} BuyerPrice:{ClassBranchPriceRule:[{ClassList:[1] BrandList:[1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28] PricePlusList:[{Begin:100 End:30000 Percent:110 Absolute:0 Type:1 PriceType:2} {Begin:30100 End:100000 Percent:90 Absolute:0 Type:1 PriceType:2} {Begin:100100 End:200000 Percent:70 Absolute:0 Type:1 PriceType:2} {Begin:200100 End:9999900 Percent:50 Absolute:0 Type:1 PriceType:2}]}] ProductRule:[]}}}]

【获取定价价格】
定价价格计算开始 ...
校验SKU选项 ...
机况-匹配价格等级标准开始 ...
    optItem: [8371 8351 8359 8361 8378 8323 8315 8308]
    rrdisCmd: hget V3BasePriceLevelStad 2: redis: nil
    filter: map[Fid:2]
    levelOrderMap: map[0:600 1:590 2:580 3:570 4:530 5:520 6:510 7:460 8:450 9:440 10:430 11:429 12:428 13:427 14:426 15:425 16:424 17:423 18:422 19:370 20:360 21:350 22:340 23:330 24:329 25:328 26:327 27:270 28:260 29:250 30:240 31:230 32:220 33:210 34:200 35:190 36:189 37:188 38:180 39:170 40:160 41:150 42:149 43:148 44:147 45:140 46:130 47:120 48:110 49:100 50:90 51:80 52:70 53:60 54:50 55:40 56:39 57:38]
    levelSaleMap: map[38:50 39:50 40:60 50:60 60:60 70:90 80:90 90:100 100:100 110:130 120:130 130:140 140:140 147:170 148:170 149:170 150:170 160:180 170:180 180:180 188:210 189:210 190:210 200:220 210:220 220:220 230:260 240:260 250:270 260:270 270:270 327:350 328:350 329:350 330:350 340:360 350:360 360:360 370:370 422:450 423:450 424:450 425:450 426:450 427:460 428:460 429:480 430:480 440:490 450:490 460:500 510:510 520:520 530:530 570:570 580:580 590:590 600:600]
    matching!!!
    match order: 0, itemComb: [8359]
    match level: 600, saleLevel: 600
    rrdisCmd: hget V3BaseLevel 600: {"Id":600,"Name":"S","Status":1,"ClassId":1}
    rrdisCmd: hget V3SaleLevel 600: redis: nil
    filter: map[Fid:map[$in:[600]]]
    rrdisCmd: hset V3SaleLevel 600 {"Id":600,"Name":"S","Desc":"","Status":1,"ClassId":1}: 1
    
    rrdisCmd: hmset V3LevelLabel 8 {"Id":8,"Name":"手机定价等级标签2","Status":1,"ClassId":1,"TypeId":1} 9 {"Id":9,"Name":"手机定价等级标签3","Status":1,"ClassId":1,"TypeId":1} 10 {"Id":10,"Name":"手机销售等级标签1","Status":1,"ClassId":1,"TypeId":2} 11 {"Id":11,"Name":"手机销售等级标签2","Status":1,"ClassId":1,"TypeId":2} 12 {"Id":12,"Name":"手机销售等级标签3","Status":1,"ClassId":1,"TypeId":2} 1 {"Id":1,"Name":"定价-测试标签","Status":0,"ClassId":3,"TypeId":1} 2 {"Id":2,"Name":"销售-测试标签","Status":0,"ClassId":3,"TypeId":2} 7 {"Id":7,"Name":"手机定价等级标签1","Status":1,"ClassId":1,"TypeId":1}: true
机况-匹配价格等级标准结束 ...

匹配穷举价格 ...
【定价定价】按系数计算定价价格 ...
    basePrice: 177900.000000
    sku: 12 value: 0.000000 price: 177900.000000        大陆国行
    sku: 18 value: 0.000000 price: 177900.000000        剩余保修期不足一个月或过保
    sku: 38 value: 38509.000000 price: 216409.000000    256GB
    sku: 130 value: 0.000000 price: 216409.000000       全网通
    sku: 1091 value: 0.000000 price: 216409.000000      深空灰色
    sku: 2236 value: 0.000000 price: 216409.000000      3GB
    sku: 2241 value: 0.000000 price: 216409.000000      A1865
    level: 600 value: 1598 price: 345821.593750
    Format Evaluate Price: 345821.593750
    base price: 345821.593750 -> 345800
定价价格计算结束 ...

【卖家参考价】【Price: 345800.000000 基于定价价格计算】加成价格计算开始 ...
    AdjustPlanInfo: &{Price:345800 Level:600 ProductId:41567 ClassId:1 BrandId:2 BasePrice:177900 Skuitem:[12 18 38 130 1091 2236 2241] PriceAdjPlan:0xc0002b7680 PriceAdjPlan2nd:<nil>}
    Matching Product Rule
    matching!!!
    product: 41567 value: {Percent:110 Absolute:0 Type:1}
    calculate product adjust
    345800.000000 * ((110 / 1000) + 1)
    Price: 383838.000000
    Format Evaluate Price: 383838.000000
    不进行2次加成计算
加成价格计算结束 ...

【卖家最高价】【Price: 383800.000000 基于卖家参考价计算】加成价格计算开始 ...
    AdjustPlanInfo: &{Price:383800 Level:600 ProductId:41567 ClassId:1 BrandId:2 BasePrice:177900 Skuitem:[12 18 38 130 1091 2236 2241] PriceAdjPlan:0xc0002b77a0 PriceAdjPlan2nd:<nil>}
    Matching Product Rule
    Matching Class Brand Price Rule
    ResultPriceType matching!!! Price: 383800.000000
    rule value: {Begin:200100 End:9999900 Percent:40 Absolute:0 Type:1 PriceType:2}
    383800.000000 * ((40 / 1000) + 1) = 399152.000000
    Price: 399152.000000
    Format Evaluate Price: 399152.000000
    不进行2次加成计算
加成价格计算结束 ...

【买家参考价】【Price: 383800.000000 基于卖家参考价计算】加成价格计算开始 ...
    AdjustPlanInfo: &{Price:383800 Level:600 ProductId:41567 ClassId:1 BrandId:2 BasePrice:177900 Skuitem:[12 18 38 130 1091 2236 2241] PriceAdjPlan:0xc0002b78c0 PriceAdjPlan2nd:<nil>}
    Matching Product Rule
    Matching Class Brand Price Rule
    ResultPriceType matching!!! Price: 383800.000000
    rule value: {Begin:200100 End:9999900 Percent:50 Absolute:0 Type:1 PriceType:2}
    383800.000000 * ((50 / 1000) + 1) = 402989.968750
    Price: 402989.968750
    Format Evaluate Price: 402989.968750
    不进行2次加成计算
加成价格计算结束 ...

【生成定价估价记录】
    Mgo Query: map[_id:eva_record_2108]
    Mgo Change: {Update:map[$inc:map[sequence_value:1]] Replace:false Remove:false Upsert:true ReturnNew:true}
    Mgo Result: {Sequence:1260553}

【最终返回】
    {"_head":{"_callerServiceId":"216002","_groupNo":"1","_interface":"sale_evaluate","_invokeId":"152533283241636","_msgType":"response","_remark":"","_timestamps":"1630392637","_version":"0.01"},"_data":{"_errStr":"SUCCESS","_data":{"evaBasePrice":"345800","sellerPrice":"383800","sellerMaxPrice":"399100","buyerPrice":"402900","recordId":"921081262041","levelId":"600","levelName":"S","saleLevelId":"600","saleLevelName":"S","saleLevelDesc":"","baseLevelTag":[{"tagId":"8","tagName":"手机定价等级标签2"},{"tagId":"7","tagName":"手机定价等级标签1"}],"saleLevelTag":[{"tagId":"11","tagName":"手机销售等级标签2"},{"tagId":"10","tagName":"手机销售等级标签1"}]},"_errCode":"0","_ret":"0"}}
'''