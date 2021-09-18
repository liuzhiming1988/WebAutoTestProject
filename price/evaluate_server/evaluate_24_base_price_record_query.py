#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 估价服务 - 24.获取定价估价记录信息（价格3.0） -  http://wiki.huishoubao.com/web/#/138?page_id=15273
    入参：recodeId：价估价记录id，21051911
    出参：recodeId：价估价记录id  |  productId：产品id  |  channelId：渠道id  |  pid：pid  |  quatation：最终估价价格（单位:分）
        basePrice：基准价（单位:分）  | versionId：系数版本id
        optLevelId：定价等级id  |  optLevelName：定价等级名称
        skuItem：估价sku选项  |  optItem：估价机况选项
        levelTempId：等级模板id （价格2.0）  |  levelStandId：等级标准ID
        saleLevelId：销售等级id  |  salelevelName：销售等级名称
        baseLevelTag：定价等级标签id  |  saleLevelTag：销售等级标签id
        adjPlanId：加成方案id  |  adjPlanVer：加成方案版本  |  adjustPrice：加成后的价格
        adjPlanId2nd：二次加成方案id  |  adjPlanVer2nd：二次加成方案版本  |  adjustPrice2nd：二次加成后的价格
        createTime：创建时间
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test, hsb_response_print

def base_price_record_query(recodeId):
    param = {"_head":{"_interface":"record_query","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"1525332832","_invokeId":"test","_callerServiceId":"116006","_groupNo":"1"},"_param":{"recodeId":recodeId}}

    secret_key = "R2gFCRbILiNhwv3YbtaGceYJlPS5Ku02"
    callerserviceid = "116006"
    url = "http://evaserver.huishoubao.com/base_price/record_query"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    respone.encoding = respone.apparent_encoding  # 编码设置
    respone_dict = json.loads(respone.text)  # 转成字典
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    base_price_record_query(recodeId='')