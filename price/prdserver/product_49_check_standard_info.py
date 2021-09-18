#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 49.获取质检标准信息列表   -    http://wiki.huishoubao.com/web/#/105?page_id=12296
    1. 对应服务：server-evaluate_detect（服务器应用名：server-evaluate_detect）
    2. 对应URL http://codserver.huishoubao.com

    入参：classId：类目ID | valid：有效标识，1-有效，0-无效 | itemKey：质检标准选项关键字（id、名称）
    出参：checkList：检测列表 | id：质检标准id | name：质检标准名称 | classId：类目id | className：类目名称 | optName：操作者 | os：系统描述
        remarks：备注信息 | upTiem：更新时间 | valid：有效标识，1：有效，0：无效 | setList：质检集合列表 | setList.osId：操作系统ID
        setList.osName：操作系统名称 | setList.type：质检类型 | setList.typeName：质检类型名称
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def check_standard_info(classId, valid, checkKey):
    param = {"_head":{"_interface":"check_standard_info","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"123456","_invokeId":"123456","_callerServiceId":"112006","_groupNo":"1"},"_param":{"classId":classId, "valid":valid, "checkKey":checkKey }}

    secret_key = "gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU"
    callerserviceid = "112006"
    url = "http://codserver.huishoubao.com/detect/check_standard_info"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # check_standard_info(classId='',valid='',checkKey='')
    # check_standard_info(classId='1',valid='',checkKey='')
    # check_standard_info(classId='2',valid='',checkKey='')
    # check_standard_info(classId='3',valid='',checkKey='')
    # check_standard_info(classId='1',valid='1',checkKey='')
    # check_standard_info(classId='1',valid='',checkKey='7.23新手机质检模板')
    check_standard_info(classId='1',valid='',checkKey='9')
    # check_standard_info(classId='1',valid='1',checkKey='') # 正常流程
    # check_standard_info(classId='1',valid='1',checkKey='') # 正常流程


# SELECT a.Fid, a.Fname, a.Fvalid, a.Fremarks, a.Fclass_id, a.Fopt_name, a.Fupdate_time, b.Fos_type, c.Fos_name, b.Ftemplate_type, d.Fname AS Fclass_name FROM t_check_standard_info a LEFT JOIN t_check_standard_item_set b ON a.Fid = b.Fcheck_standard_id LEFT JOIN t_eva_os_type c ON b.Fos_type = c.Fos_id LEFT JOIN t_pdt_class d ON a.Fclass_id = d.Fid WHERE (1=1) AND a.Fclass_id = 1 AND a.Fvalid = 1;

'''
outPacket=[{"_data":{"_data":{"checkList":[{"classId":"1","className":"手机","id":"1","name":"闲鱼验机与竞拍选项模板","optName":"init","os":"ios系统+Android","remarks":"","setList":[{"osId":"1","osName":"ios系统","type":"1","typeName":"标准检测"},{"osId":"2","osName":"Android","type":"1","typeName":"标准检测"}],"upTiem":"2020-09-10 17:25:43","valid":"1"},{"classId":"1","className":"手机","id":"3","name":"7.23新手机质检标准","optName":"init","os":"ios系统+Android","remarks":"","setList":[{"osId":"1","osName":"ios系统","type":"1","typeName":"标准检测"},{"osId":"2","osName":"Android","type":"1","typeName":"标准检测"}],"upTiem":"2020-09-10 16:31:16","valid":"1"}]},"_errCode":"0","_errStr":"success","_ret":"0"},"_head":{"_callerServiceId":"112006","_groupNo":"1","_interface":"check_standard_info","_invokeId":"123456","_msgType":"response","_remark":"","_timestamps":"1599735651","_version":"0.01"}}]
'''
