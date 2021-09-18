#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 48.获取质检标准选项集合信息 - http://wiki.huishoubao.com/web/#/105?page_id=12268
    1. 对应服务：server-evaluate_detect（服务器应用名：server-evaluate_detect）
    2. 对应URL http://codserver.huishoubao.com

    入参：checkStandardId：质检标准id ，非空  （必填） | osType：操作系统类型，1-iOS，2-Android，3-mac os，4-windows，5-其他，非空（必填）
        checkType：检测类型，1-标准检测，2-标准大质检，非空（必填）
    出参：checkList：问题项集合 | questionId：问题项id | questionName：问题项名称 | confType：大类类型 | answerList：答案项集合
        answerId：答案项id | answerName：答案项名称 | answerWeight：答案项权重
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def check_standard_item_set(checkStandardId, osType, checkType):
    param = {"_head":{"_interface":"check_standard_item_set","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"123456","_invokeId":"123456","_callerServiceId":"112006","_groupNo":"1"},"_param":{"checkStandardId":checkStandardId, "osType":osType,"checkType":checkType }}

    secret_key = "gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU"
    callerserviceid = "112006"
    url = "http://codserver.huishoubao.com/detect/check_standard_item_set"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # check_standard_item_set(checkStandardId='9', osType='1', checkType='1') # 正常流程
    # check_standard_item_set(checkStandardId='9', osType='2', checkType='1') # 正常流程
    check_standard_item_set(checkStandardId='9', osType='2', checkType='2') # 正常流程
    # check_standard_item_set(checkStandardId='9', osType='1', checkType='2') # 正常流程
    # check_standard_item_set(checkStandardId='1', osType='1', checkType='1') # t_check_standard_info.Fvalid=0，不影响，正常查询(由另一个接口规避）
    # check_standard_item_set(checkStandardId='1', osType='1', checkType='1') # t_check_standard_item_set.Fvalid=0，不影响(应由另一个接口判断t_check_standard_info.Fvalid=0状态）
    # check_standard_item_set(checkStandardId='', osType='', checkType='')  # 必传字段，传参为空； 返回：checkStandardId为空或非数值
    # check_standard_item_set(checkStandardId='1', osType='', checkType='') # 必传字段，传参为空； 返回：osType为空或非纯数值
    # check_standard_item_set(checkStandardId='1', osType='1', checkType='') # 必传字段，传参为空； 返回：checkType为空或非纯数值
    # check_standard_item_set(checkStandardId='5', osType='1', checkType='1') # checkStandardId='5' 不存在； 返回：空
    # check_standard_item_set(checkStandardId='1', osType='3', checkType='1') # osType='3' 不存在； 返回：空



'''
[{"answerIDs":["4210","4211","4212","4246","5572"],"questionID":"5004","confType":"1"},{"answerIDs":["4194","4195","4196","4247"],"questionID":"5005","confType":"1"},{"answerIDs":["4249","4250","4251","4252"],"questionID":"5064","confType":"1"},{"answerIDs":["5101","5102","5103","5104"],"questionID":"5100","confType":"1"},{"answerIDs":["5106","5107","5108","5109"],"questionID":"5105","confType":"1"},{"answerIDs":["4298","4299","4300","4301"],"questionID":"5076","confType":"1"},{"answerIDs":["4302","4303","4304","4305"],"questionID":"5077","confType":"1"},{"answerIDs":["4306","4307","4308","4309"],"questionID":"5078","confType":"1"},{"answerIDs":["4310","4311","4312","4313"],"questionID":"5079","confType":"1"},{"answerIDs":["4359","4360","4361","4362","5138"],"questionID":"5093","confType":"1"},{"answerIDs":["4270","4271","4272","4273"],"questionID":"5069","confType":"1"},{"answerIDs":["4274","4275","4276","4277"],"questionID":"5070","confType":"1"},{"answerIDs":["4282","4283","4284","4285"],"questionID":"5072","confType":"1"},{"answerIDs":["4286","4287","4288","4289"],"questionID":"5073","confType":"1"},{"answerIDs":["5111","5112","5113","5114"],"questionID":"5110","confType":"1"},{"answerIDs":["4290","4291","4292","4293"],"questionID":"5074","confType":"1"},{"answerIDs":["4032","4245","5115","5116","5117"],"questionID":"5042","confType":"1"},{"answerIDs":["4011","4253","5118","5119","5120"],"questionID":"5043","confType":"1"},{"answerIDs":["4004","4320","5121","5122","5123"],"questionID":"5046","confType":"1"},{"answerIDs":["4321","4322","5124","5125"],"questionID":"5081","confType":"1"},{"answerIDs":["4323","4324","5126"],"questionID":"5082","confType":"1"},{"answerIDs":["4118","4330","5143"],"questionID":"5036","confType":"1"},{"answerIDs":["4142","4329","5142"],"questionID":"5037","confType":"1"},{"answerIDs":["4027","4331","5144","5244"],"questionID":"5060","confType":"1"},{"answerIDs":["4074","4332","5145","5245"],"questionID":"5048","confType":"1"},{"answerIDs":["4101","4333","5146"],"questionID":"5040","confType":"1"},{"answerIDs":["4197","4198","4200","5149","5150"],"questionID":"5023","confType":"1"},{"answerIDs":["4077","4334","5147","5148"],"questionID":"5024","confType":"1"},{"answerIDs":["5231","5232","5233","5234","5235"],"questionID":"5230","confType":"1"},{"answerIDs":["5156","5157","5158","5159","5160","5161","5162"],"questionID":"5154","confType":"1"},{"answerIDs":["5163","5164","5165","5166","5167","5168","5169"],"questionID":"5155","confType":"1"},{"answerIDs":["4327","4328","5176","5177","5178"],"questionID":"5083","confType":"1"},{"answerIDs":["5180","5181","5182","5183","5184"],"questionID":"5179","confType":"1"},{"answerIDs":["4148","4149"],"questionID":"5053","confType":"1"},{"answerIDs":["5201","5202","5203"],"questionID":"5200","confType":"1"},{"answerIDs":["5186","5187","5188","5189","5190","5191","5192"],"questionID":"5185","confType":"1"},{"answerIDs":["5194","5195","5196","5197","5198","5199"],"questionID":"5193","confType":"1"},{"answerIDs":["4357","4358","5246"],"questionID":"5092","confType":"1"},{"answerIDs":["4368","4369","4370","4371","4372","4381","5204","6950"],"questionID":"5094","confType":"1"},{"answerIDs":["4025","4026","4363","4364","4365","4366","4367"],"questionID":"5003","confType":"1"},{"answerIDs":["4314","4315","4316","4317"],"questionID":"5080","confType":"1"},{"answerIDs":["4051","4325","4375","4377","4378","4382","5139","5248"],"questionID":"5050","confType":"1"},{"answerIDs":["4218","4326","4376","4379","4380","4383","5140","5141","5249"],"questionID":"5051","confType":"1"},{"answerIDs":["4093","4095","4096","4097","4099","4100","4318","4319","4373","4374"],"questionID":"5022","confType":"1"}]
'''