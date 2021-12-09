#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 定价系统+商品库系统+调价系统+估价系统 - 获取产品估价选项  - http://wiki.huishoubao.com/web/#/347?page_id=15707
    入参：channel_id：渠道id  |  pid：pid  |  product_id：要查询产品选项的产品ID  |  ip：用户公网访问IP，例如：10.0.10.62
    出参：itemid：产品id  |  need_eva：1-需要估价，0-无需估价
        itemList：查询成功的产品配置数组
            conftype：类型id（有大类属性的，显示具体的大类ID； 无大类属性的，显示0  |  confTypeName：类型名称  |  desc：描述，辅助名称进行解释的陈述话语
            alias_id：别名id  |  alias_name：别名名称
            id：问题项id 或 答案项id  |  name：选项名称  |  parent_item：父节点，对于的上一级的节点，一般之答案项对于的问题项的节点id，它是一个问题项节点值
            seq_num：顺序号 （小的在前，大的在后） |  show_level：显示层级，1-问题级，2-答案级
            course：3.0新增字段：选项教程（或者描述）
                course.name：教程名（只有问题项有）  |  course.step：步骤  |  course.step.order：步骤排序号
                course.step.name：步骤名称  |  course.step.desc：步骤说明  |  course.step.pic：步骤图片
            question：答案项列表
                desc：描述，辅助名称进行解释的陈述话语 | id：问题项id 或 答案项id  |  name：选项名称
                parent_item：父节点，对于的上一级的节点，一般之答案项对于的问题项的节点id，它是一个问题项节点值
                picture：图片列表
                    picturename：图片名称
                priority：同问题项下答案的优先级，值越小，优先级越高，由平台产品或渠道的配置系数而来  |  seq_num：顺序号 （小的在前，大的在后）
                show：针对功能性(conftype=3)选项 表示前端页面是否显示该答案项，1-显示，0-或不存在不显示  |  show_level：显示层级，1-问题级，2-答案级
                course：3.0新增字段：选项教程（或者描述）
                    course.name：教程名（只有问题项有）  |  course.step：步骤  |  course.step.order：步骤排序号
                    course.step.name：步骤名称  |  course.step.desc：步骤说明  |  course.step.pic：步骤图片
                weight：同问题项下答案的权重，值越大，优先级越高，由选项库而来
        defualtOptionList：联动关系列表
            defualtOptionList.aId：答案项ID  |  defualtOptionList.aIdDesc：答案项名称
            defaultAid：联动关系数据
                qId：问题项ID  |  qName：问题项名称  |  aId：答案项ID  |  aName：答案项名称
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print,hsb_eva_ipProxy_k8s_test

def v3_eva_option_get(channel_id, product_id, pid):
    param = {"_head":{"_interface":"eva_option_get","_msgType":"request","_remark":"eva_product_v3","_version":"0.01","_timestamps":"123","_invokeId":"eva_product_v3","_callerServiceId":"816006","_groupNo":"1"},"_param":{"channel_id":channel_id, "product_id":product_id, "pid":pid}}
    secret_key = "dk26kmdasnph0voz69fj0jpv7t3ixev8"
    callerserviceid = "212006"
    url = "http://prdserver.huishoubao.com/eva_product_v3/eva_option_get"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    respone.encoding = respone.apparent_encoding  # 编码设置
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    ''' 走了ES 和 Redis，目前2分钟更新一次 '''
    '''1. 渠道 和 PID 为空 | "_retcode":"70020100","_ret":"70020100","_retinfo":"请求参数错误 [ChannelId为必填字段]"'''
    # v3_eva_option_get(channel_id="", pid="3309", product_id="41567")

    '''2. 只传渠道ID 或 只传PID | "_retcode": "70020100", "_ret": "70020100", "_retinfo": "请求参数错误 [Pid为必填字段]'''
    # v3_eva_option_get(channel_id="40000001", pid="", product_id="41567")

    # "_retcode":"70020100","_ret":"70020100","_retinfo":"请求参数错误 [ChannelId为必填字段]"
    # v3_eva_option_get(channel_id="", pid="1001", product_id="41567")

    '''3. 传的渠道ID、PID，有一个不存在、两个都不存在、渠道ID和PID不对应 | 价格不做这个渠道ID/PID的合法性校验，查询不到记录，则使用 全部渠道 对应的数据返回'''
    # v3_eva_option_get(channel_id="2021080312345", pid="1001", product_id="41567") # 渠道ID不存在，PID存在
    # v3_eva_option_get(channel_id="40000001", pid="2021080312345", product_id="41567") # 渠道ID存在，PID不存在
    # v3_eva_option_get(channel_id="2021080312345", pid="2021080312345", product_id="41567") # 渠道ID不存在，PID不存在
    # v3_eva_option_get(channel_id="10000837", pid="1001", product_id="41567") # 渠道ID存在，PID存在，但它们不对应

    '''4. 同时传渠道ID 和 PID（满足“部分渠道/PID”， 正常value）'''
    # v3_eva_option_get(channel_id="40000001", pid="1001", product_id="41567") # 正常iOS机型
    # v3_eva_option_get(channel_id="40000001", pid="1001", product_id="64000") # 正常Android机型
    # v3_eva_option_get(channel_id="40000001", pid="1001", product_id="64000") # 正常Android机型（含聚合类型的 SKU配置（如 一个估价SKU答案项 映射多个 标准SKU答案项）
    # v3_eva_option_get(channel_id="40000001", pid="1001", product_id="64000") # 正常Android机型（含聚合类型的 SKU配置（如 存储容量 = 机身内存 + 存储容量）
    # v3_eva_option_get(channel_id="40000001", pid="1001", product_id="64000") # 正常Android机型（含聚合类型的 SKU配置（如 存储容量 = 机身内存 + 存储容量）

    '''5. 同时传渠道ID 和 PID | 机型“不支持估价” '''
    # "_retcode":"70020301","_ret":"70020301","_retinfo":"获取估价产品产品选项失败 [mongo: no documents in result]"
    # v3_eva_option_get(channel_id="40000001", pid="1001", product_id="65503")
    # "_retcode":"70020301","_ret":"70020301","_retinfo":"获取估价产品产品选项失败 [不支持估价状态机型]"
    # v3_eva_option_get(channel_id="40000001", pid="1001", product_id="4001")

    '''6. 同时传渠道ID 和 PID | 机型 “禁用”状态 | "_data":null,"_retcode":"70020301","_ret":"70020301","_retinfo":"获取估价产品产品选项失败 [产品为下架状态]"'''
    # v3_eva_option_get(channel_id="40000001", pid="1001", product_id="1037")

    '''①前提，入参（机型+PID）要有关联过估价子模板，才会拉取选项； ②入参（机型+PID）有关联过估价子模板，未编辑过SKU，会返回标准SKU'''
    '''7. 同时传渠道ID 和 PID | 机型“不支持估价” | 机型未编辑过SKU，也未操作使用过任何估价模板'''
    # "_retcode":"70020301","_ret":"70020301","_retinfo":"获取估价产品产品选项失败 [mongo: no documents in result]"  |  正常
    # v3_eva_option_get(channel_id="40000001", pid="1001", product_id="65503") # 未关联估价子模板，未编辑过SKU配置
    # v3_eva_option_get(channel_id="40000001", pid="1001", product_id="64559") # 编辑过SKU配置，未关联估价子模板
    # v3_eva_option_get(channel_id="40000001", pid="1001", product_id="64589") # 关联了估价子模板，未编辑过SKU配置
    # v3_eva_option_get(channel_id="40000001", pid="1001", product_id="1013") # 关联了估价子模板，未编辑过SKU配置（无SKU机型）

    '''8. 同时传渠道ID 和 PID | PID有被“部分渠道/PID”的估价模板关联，估价模板中有“使用中、全部渠道”属性的估价模板'''
    # v3_eva_option_get(channel_id="40000001", pid="1001", product_id="41567") # 正常

    '''9. 同时传渠道ID 和 PID | PID没有被“部分渠道/PID”的估价模板关联，估价模板中有“使用中、全部渠道”属性的估价模板'''
    # 正常（使用了 全部渠道 的这个估价模板-估价子模板的机况选项数据返回）
    # v3_eva_option_get(channel_id="10000837", pid="3415", product_id="41567")
    # 正常 | 关联了估价子模板，未编辑过SKU配置 |（使用了 全部渠道 的这个估价模板-估价子模板的机况选项数据返回）
    # v3_eva_option_get(channel_id="10000837", pid="3415", product_id="64589")
    # v3_eva_option_get(channel_id="10000837", pid="0", product_id="64589")


    # v3_eva_option_get(channel_id="10000838", pid="3419", product_id="1069")
    # v3_eva_option_get(channel_id="10000838", pid="3419", product_id="3088")
    # v3_eva_option_get(channel_id="10000838", pid="3419", product_id="41567")


    # v3_eva_option_get(channel_id="10000164", pid="1405", product_id="41567")
    # v3_eva_option_get(channel_id="10000165", pid="1406", product_id="41567")
    # v3_eva_option_get(channel_id="10000166", pid="1407", product_id="41567")
    # v3_eva_option_get(channel_id="10000167", pid="1408", product_id="41567")
    # v3_eva_option_get(channel_id="10000168", pid="1409", product_id="41567")
    v3_eva_option_get(channel_id="10000164", pid="1196", product_id="41567")

'''
【EvaluateProduct】
formParam: {ChannelId:10000768 Pid:3309 PlatformType: ProductId:41567 Ip: BusinessId: NeedDefault:}
rrdisCmd: hget V3EvaPriceProduct 41567: {"ProductId":41567,"ProductName":"iPhone X","BrandIdV1":11,"BrandId":2,"BrandName":"苹果","ClassId":1,"ClassName":"手机","KeyWord":"iPhoneX","OsType":1,"OsName":"ios系统","RecycleType":3,"PicId":"41567_20191106154719_960.jpg","PutawayTime":"2017-09-13","EvaStatus":1,"Status":1,"CreateTime":"2021-01-28T16:56:39Z","UpdateTime":"2021-07-22T19:15:37.558Z","UserName":"张金发_TEST"}
evaProductInfo: &{ProductId:41567 ProductName:iPhone X BrandIdV1:11 BrandId:2 BrandName:苹果 ClassId:1 ClassName:手机 KeyWord:iPhoneX OsType:1 OsName:ios系统 RecycleType:3 PicId:41567_20191106154719_960.jpg PutawayTime:2017-09-13 EvaStatus:1 Status:1 CreateTime:2021-01-28 16:56:39 +0000 UTC UpdateTime:2021-07-22 19:15:37.558 +0000 UTC UserName:张金发_TEST}

rrdisCmd: hget V3EvaChannelTempMap c10000768-p3309: 42
redis templateId: 42
rrdisCmd: hget V3EvaLevelWeight p41567-t42: {"Id":176,"ProductId":41567,"TemplateId":42,"SubTemplateId":65,"LevelWeight":[{"EveLevel":255,"Weight":[{"BaseLevel":350,"Value":660},{"BaseLevel":340,"Value":220},{"BaseLevel":330,"Value":120}]},{"EveLevel":250,"Weight":[{"BaseLevel":360,"Value":1000}]},{"EveLevel":240,"Weight":[{"BaseLevel":329,"Value":1000}]}],"WeightVersion":29,"MaxPrice":165300,"Status":1,"CreateTime":"2021-07-26T18:18:25.77Z","UpdateTime":"2021-07-28T16:08:00.012Z","UserName":"张金发_TEST"}
'''