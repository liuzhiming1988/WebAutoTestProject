#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 估价服务 - 24.获取定价估价记录信息（价格3.0） -  http://wiki.huishoubao.com/web/#/138?page_id=15273
    入参：recodeId：价估价记录id，价格2.0：年月+估价ID，21051911；   估价3.0：9 + 年月 + 估价ID
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
    url = "http://bpeserver.huishoubao.com/adjustment_price/record_query"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    respone.encoding = respone.apparent_encoding  # 编码设置
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    ''' recodeId：价估价记录id，价格2.0：年月+估价ID，21051911；   估价3.0：9 + 年月 + 估价ID '''
    base_price_record_query(recodeId='9210679129')  # 价格3.0
    # base_price_record_query(recodeId='210656301')  # 价格2.0

'''
价格3.0 【BasePriceEvaluate】
formParam: {RecodeId:9210585715}
Prefix: 2105 RecordId: 85715
{EvaluateId:85715 ProductId:41567 BasePrice:161600 SbuType:2 EvaType:3 VersionId:196 OptLevelId:600 Select:[12 471 18 2236 38 1091 2242 9016 9019 9027 9029 9037 9039 9052 9056 9057 9059 9062 9070 9072 9074 7559 9078 9079 9081 7575 9082 9086 9088 9090 9095 9099 9104 9106 9113 9117 7532] SkuItem:[12 18 38 471 1091 2236 2242] OptItem:[7532 7559 7575 9016 9019 9027 9029 9037 9039 9052 9056 9057 9059 9062 9070 9072 9074 9078 9079 9081 9082 9086 9088 9090 9095 9099 9104 9106 9113 9117] LevelTempId:15 Quatation:292500 ErrorCode:0 ErrorInfo:success SpendTime:3 CreateTime:2021-05-22 16:15:05.773 +0000 UTC Interface: IP: UserId: ChannelId:0 Pid:0 LevelStandId:0 SaleLevelId:0 BaseLevelTag:[] SaleLevelTag:[] AdjPlanId:0 AdjPlanVer:0 AdjustPrice:0 AdjPlanId2nd:0 AdjPlanVer2nd:0 AdjustPrice2nd:0 OptLevelName: SaleLevelName:}
'''