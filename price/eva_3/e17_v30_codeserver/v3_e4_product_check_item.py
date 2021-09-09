#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 估价服务 - 估价3.0 - 4 获取产品检测模板选项信息  - http://wiki.huishoubao.com/web/#/138?page_id=15854
    入参：productId：产品机型id  |  checkType：检测类型、检测场景，例如顺丰上门场景，或是闲鱼验机场景，1,2，是
        userId：检测人  |  ip：用户IP，127.0.0.1
        freqLimitType：频率限制类型，0-不限制，1-IP，2-UserId	0 1 2 （外部对到用户端系统，建议增加限频；内部系统可以不限频）
    出参：productId：产品id  |  productName：产品名称  |  brandId：品牌id  |  brandName：品牌名称
        classId：品类id  |  className：品类名称
        skuList：sku选项列表
            skuList.questionId：sku问题项id  |  skuList.questionName：sku问题项名称
            skuList.singleFlag：sku多选项 1-单选项、2-多选项  |  skuList.questWeight：sku检测答案项权重（越小越好）
            skuList.answerList：sku问题项下的答案选项列表  |  skuList.answerList.answerId：sku答案选项id
            skuList.answerList.answerName：sku答案选项名称  |  skuList.answerList.answerWeight：sku答案选项权重（越小越好）
            skuList.answerList.singleFlag：sku答案多选项 1-单选项、2-多选项
        checkList：检测机况选项列表
            checkList.itemType：问题项分类id  |  checkList.itemTypeName：问题项分类名称
            checkList.order：问题项排序（越小越好）  |  checkList.questionList：问题项列表
            checkList.question.questionId：问题项id  |  checkList.question.questionName：问题项名称
            checkList.question.singleFlag：多选项 1-单选项、2-多选项  |  checkList.question.questWeight：检测答案项权重（越小越好）
            checkList.question.answerList：问题项下的答案选项列表  |  checkList.question.answerList.answerId：答案选项id
            checkList.question.answerList.answerName：答案选项名称  |  checkList.question.answerList.answerWeight：答案选项权重（越小越好）
            skuLcheckList.questionist.answerList.singleFlag：答案多选项 1-单选项、2-多选项
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def v3_product_check_item(productId, checkType, freqLimitType, ip):
    param = {"_head":{"_interface":"product_check_item","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"1525332832","_invokeId":"152533283241636","_callerServiceId":"216002","_groupNo":"1"},"_param":{"productId":productId, "checkType":checkType, "userId":"1895", "freqLimitType":freqLimitType, "ip":ip}}
    secret_key = "rAfnRwyWfh2N9vXVgWwdpJxaXgOCd8af"
    callerserviceid = "216002"
    url = "http://codserver.huishoubao.com/detect_v3/product_check_item"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    respone.encoding = respone.apparent_encoding  # 编码设置
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    ''' 响应内容中："questWeight":"1" 是指检测问题项，在检测子模板中的排序； "answerWeight":"1" 是指检测答案项，在检测子模板中的排序 '''

    # 1. 只命中 “配置方式：按机型配置” 的检测子模板
    # v3_product_check_item(productId='41567', checkType='10', freqLimitType='1', ip='127.0.0.1')

    # 2. 同时命中 “配置方式：按机型配置” 和 “配置方式：按操作系统配置” 的检测子模板； 优先取  “配置方式：按机型配置”  的配置
    # v3_product_check_item(productId='41567', checkType='10', freqLimitType='1', ip='127.0.0.1')

    # 3. 只命中 “配置方式：按操作系统配置” 的检测子模板
    # v3_product_check_item(productId='41567', checkType='10', freqLimitType='1', ip='127.0.0.1')

    # 4. 未命中任何 检测子模板  |  "_errStr":"获取产品检测选项失败 [机型[41567]没有查询到检测子模板信息]"  |  正常
    # v3_product_check_item(productId='41567', checkType='10', freqLimitType='1', ip='127.0.0.1')
    # v3_product_check_item(productId='41567', checkType='16', freqLimitType='1', ip='127.0.0.1')

    # 5. 检测方式被禁用  | "_errStr":"获取产品检测选项失败 [检测类型为禁用状态]"  |  正常
    # v3_product_check_item(productId='41567', checkType='10', freqLimitType='1', ip='127.0.0.1')

    # 6. 检测方式未关联 检测模板 | "_errStr":"获取产品检测选项失败 [没有查询检测类型信息]"  ？？？
    # v3_product_check_item(productId='41567', checkType='10', freqLimitType='1', ip='127.0.0.1')

    # 7. 传的检测方式ID  不存在 | "_errStr":"获取产品检测选项失败 [数据库没有查询到检测类型[20210831]信息]" |  正常
    # v3_product_check_item(productId='41567', checkType='20210831', freqLimitType='1', ip='127.0.0.1')

    # 8. 检测方式传空 | "_errStr":"请求参数错误 [CheckType为必填字段]" | 正常
    # v3_product_check_item(productId='41567', checkType='', freqLimitType='1', ip='127.0.0.1')

    # 9. 手机类目机型，所传检测方式为笔记本类目下方式ID  | "_errStr":"获取产品检测选项失败 [没有查询检测类型信息]","_errCode":"70023301" ？？？
    # v3_product_check_item(productId='41567', checkType='15', freqLimitType='1', ip='127.0.0.1')


    # v3_product_check_item(productId='1008', checkType='2', freqLimitType='1', ip='127.0.0.1') #34项苹果安卓定价模板v1（iPhone3G-3GS或低端安卓）(ID:13)
    # v3_product_check_item(productId='1132', checkType='2', freqLimitType='1', ip='127.0.0.1') #34项安卓定价模板v1（安卓简易无指纹）(ID:12)
    # v3_product_check_item(productId='6027', checkType='2', freqLimitType='1', ip='127.0.0.1') #34项安卓定价模板v1（安卓简易有指纹）(ID:11)
    # v3_product_check_item(productId='30780', checkType='2', freqLimitType='1', ip='127.0.0.1') #34项安卓定价模板v1（安卓无面容无指纹）(ID:10)
    # v3_product_check_item(productId='58960', checkType='2', freqLimitType='1', ip='127.0.0.1') #34项安卓定价模板v1（安卓-面容）(ID:9)
    # v3_product_check_item(productId='2063', checkType='2', freqLimitType='1', ip='127.0.0.1') #34项安卓定价模板v1（安卓指纹）(ID:8)
    # v3_product_check_item(productId='59998', checkType='2', freqLimitType='1', ip='127.0.0.1') #34项安卓定价模板v1（安卓面容+指纹）(ID:7)
    # v3_product_check_item(productId='30750', checkType='2', freqLimitType='1', ip='127.0.0.1') #34项苹果定价模板v1（iPhone4-5c）(ID:6)
    # v3_product_check_item(productId='38201', checkType='2', freqLimitType='1', ip='127.0.0.1') #34项苹果定价模板v1（iPhone5s-8P及以上）(ID:5)
    v3_product_check_item(productId='41567', checkType='2', freqLimitType='1', ip='127.0.0.1') #34项苹果定价模板v1（iPhoneX及以上）(ID:4)

'''
【EvaluateCheckV3】 【前提：定价等级模板 要切换到 定价等级标准】
【价格3.0一期，B端寄卖切换会使用】

清除价格3.0 所有的redis
http://111.230.107.156:15672/#/queues
Queue EvaToolsCmdProQueue in virtual host eva_vhost

http://wiki.huishoubao.com/web/#/347?page_id=15636

{
"cmd": "DelEvaRedis",
"params": ["AdjustPlan"]
}
params数组空时，删除所有价格3.0的key
可以在 EvaluateToolsGo 查看push记录

'''