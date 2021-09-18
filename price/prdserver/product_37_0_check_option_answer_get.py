#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 37.1.标准检测选项答案项搜索接口 - http://wiki.huishoubao.com/web/#/105?page_id=6759
    检测映射服务（wiki项目：产品服务）：eva_detect
    入参：classId：类目，不同类目有不同的选项库，1-手机，2-笔记本，3-平板，5-智能手表，可为空
        questionId：标准检测问题项ID，可传递多个，以#号分割，例如：91#675#31，可为空
        keyword：关键词 会匹配答案项名称和答案项描述，可为空
        answerId：标准检测答案项id，可传递多个，以#号分割 例如 1#19#98#90 ,可为空
        valid：是否可用, 0-不可用，1-可用,可为空
        pageIndex：分页的页码，从0开始  |  pageSize：每页的数据量，最大500个
    出参：pageIndex：分页的页码  |  pageSize：每页的数据量
        list：产品列表  |  classId：类目ID  |  className：类目名称  |  qId：检测问题项ID
        qName：检测问题项名称  |  aId：检测答案项ID  |  aName：检测答案项名称
        singleFlag：选项类型标识, 1-单选项，2-多选项
        valid：是否可用, 0-不可用，1-可用  |  total：总数
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def check_option_answer_get(classId, questionId, keyword, answerId, valid):
    param = {"_head":{"_interface":"check_option_answer_get","_msgType":"request","_remark":"hello","_version":"0.01","_timestamps":"123","_invokeId":"111","_callerServiceId":"112006","_groupNo":"1"},"_param":{"pageIndex":"0","pageSize":"50","classId":classId,"questionId":questionId,"keyword":keyword,"answerId":answerId,"valid":valid}}

    secret_key = "gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU"
    callerserviceid = "112006"
    url = "http://codserver.huishoubao.com/detect/check_option_answer_get"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # check_option_answer_get(classId='',questionId='',keyword='',answerId='',valid='')
    # check_option_answer_get(classId='1',questionId='',keyword='',answerId='',valid='')
    # check_option_answer_get(classId='1',questionId='',keyword='',answerId='',valid='2')
    # check_option_answer_get(classId='1',questionId='',keyword='',answerId='',valid='0')
    # check_option_answer_get(classId='1',questionId='',keyword='',answerId='',valid='1')
    # check_option_answer_get(classId='1',questionId='',keyword='购买渠道',answerId='',valid='1')
    # check_option_answer_get(classId='1',questionId='11',keyword='',answerId='',valid='1')
    check_option_answer_get(classId='1',questionId='',keyword='',answerId='13',valid='1')