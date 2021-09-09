#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 估价服务 - （弃用）23.定价估价接口（价格3.0） -  http://wiki.huishoubao.com/web/#/138?page_id=2211
    入参：channelId：渠道id，10000139  |  pid：pid，1001  |  roductId：产品机型id，41567
        evaType：价格2.0 质检类型，1-57标准质检，2-大质检，3-34标准质检，价格3.0-填0
        skuItem：sku答案选项id，“12”等  |  optItem：机况答案选项id，“7422”等  |  ip：用户IP，127.0.0.1
        userId：用户ID	123456  |  priceType：价格类型：1-销售定价，2-回收定价
        freqLimitType：频率限制类型，0-不限制，1-IP，2-UserId
    出参：quotation：估算价格 单位:分  |  standPrice：定价价格 单位:分  |  adjustPrice：加成价格 单位:分
        adjustPrice2nd：二次加成价格 单位:分  |  recordId：估价唯一id（id 会超过int(11)，请不要用int保存）（可通过：24 获取定价估价记录接口，获取信息）
        levelId：价格3.0-定价等级id  |  levelName：价格3.0-定价等级名称
        saleLevelId：价格3.0-销售等级id （价格2.0为空）
        saleLevelName：价格3.0-销售等级名称 （价格2.0为空）
        baseLevelTag：定价等级标签id  |  saleLevelTag：销售等级标签id
    错误码：900 未知错误  |  901 参数错误  |  902 获取数据失败  |  903 下架状态  |  904 产品配置数据错误
        905 等级匹配失败  |  906 生成估价记录失败  |  999 频率限制
    场景逻辑：
        1、按比例加成  定价价格 * (( 按比例加成值 / 1000 ) + 1)
        2、按金额加成  定价价格 + 按金额加成值
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test, hsb_response_print

def base_price_evaluatee(channelId, pid, productId, ip, freqLimitType):
    # "priceType":"2" 回收定价 | "evaType":"0" 价格3.0
    param = {"_head":{"_interface":"evaluate","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"1525332832","_invokeId":"mikingzhang_adjustPrice","_callerServiceId":"116006","_groupNo":"1"},"_param":{"channelId":channelId, "pid":pid, "productId":productId, "evaType":"0","skuItem":['12', '471', '18', '2236', '38', '1091', '2242'], "optItem":['8297', '8301', '8305', '8309', '8312', '8316', '8320', '8323', '8326', '8333', '8336', '8339', '8343', '8349', '8351', '8359',   '8361', '8364', '8367', '8371', '8375', '8378', '8382', '8385', '8389', '8393', '8397', '8403', '8408', '8412', '8416', '8419', '8422', '8425', '8429', '8432', '8436', '8441', '8444', '8449'], "ip":ip, "userId":"1002","priceType":"2", "freqLimitType":freqLimitType}}

    secret_key = "R2gFCRbILiNhwv3YbtaGceYJlPS5Ku02"
    callerserviceid = "116006"
    url = "http://bpeserver.huishoubao.com/base_price/evaluate"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    respone.encoding = respone.apparent_encoding  # 编码设置
    respone_dict = json.loads(respone.text)  # 转成字典
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    ''' 一、回收调价方案 - 自住调价 - 不自动使用最新的回收定价版本
    SKU：标准sku
    机况：机型【iPhone X】 - 商品等级标准：手机定价等级标准-20210310（ID: 2） - 定价标准：定价标准-20200301（ID: 4） - 质检标准：质检标准-20210301（ID: 4）
    可选机况：去 定价标准：定价标准-20200301（ID: 4） 问题项下面随机找 
    "optItem" : ['8297', '8301',    '8305', '8309', '8312',    '8316', '8320', '8323', '8326', '8333', '8336', '8339', '8343', '8349', '8351', '8359', '8361', '8364', '8367', '8371', '8375', '8378', '8382', '8385', '8389', '8393', '8397', '8403', '8408', '8412', '8416', '8419', '8422', '8425', '8429', '8432', '8436', '8441', '8444', '8449'] '''

    '''一、【自主调价 - 不自动使用 - 命中】渠道 - 当前使用的定价版本时间：2021-05-25 23:05:43 | 回收定价有更新 | 历史版本 基准价 命中调价方案规则'''
    # iPhone X， 历史版本：1395  基准价：1958  |  线上版本：1396  基准价：2002
    # 回收定价价格是用 历史版本 系数 计算 |  匹配调价规则是用 历史版本的基准价 匹配  |  正常
    # base_price_evaluatee(channelId='10000060', pid='0', productId='41567', ip='127.0.0.1', freqLimitType='0') # 按类目+品牌+初始化价格范围调价 | 按比例
    # base_price_evaluatee(channelId='10000060', pid='0', productId='41567', ip='127.0.0.1', freqLimitType='0') # 按类目+品牌+初始化价格范围调价 | 按比例 -101%
    # base_price_evaluatee(channelId='10000060', pid='0', productId='41567', ip='127.0.0.1', freqLimitType='0') # 按类目+品牌+初始化价格范围调价 | 按金额
    # base_price_evaluatee(channelId='10000060', pid='0', productId='41567', ip='127.0.0.1', freqLimitType='0') # 按机型调价 | 按比例
    # base_price_evaluatee(channelId='10000060', pid='0', productId='41567', ip='127.0.0.1', freqLimitType='0') # 按机型调价 | 按金额

    # 2021.05.28 确认 先计算机型加成，再计算sku+等级加成（先计算绝对值金额，再计算比例）
    # base_price_evaluatee(channelId='10000060', pid='0', productId='41567', ip='127.0.0.1', freqLimitType='0') # 按机型调价（有sku+等级）1个，按比例
    # base_price_evaluatee(channelId='10000060', pid='0', productId='41567', ip='127.0.0.1', freqLimitType='0') # 按机型调价（有sku+等级）1个，按金额
    # base_price_evaluatee(channelId='10000060', pid='0', productId='41567', ip='127.0.0.1', freqLimitType='0') # 按机型调价（有sku+等级）2个，都是按比例
    # base_price_evaluatee(channelId='10000060', pid='0', productId='41567', ip='127.0.0.1', freqLimitType='0') # 按机型调价（有sku+等级）2个，都是按金额
    # base_price_evaluatee(channelId='10000060', pid='0', productId='41567', ip='127.0.0.1', freqLimitType='0') # 按机型调价（有sku+等级）2个，1个按比例，1个按金额
    # base_price_evaluatee(channelId='10000060', pid='0', productId='41567', ip='127.0.0.1', freqLimitType='0') # 按机型调价（有sku+等级）不限sku 不限等级

    # base_price_evaluatee(channelId='10000060', pid='0', productId='41567', ip='127.0.0.1', freqLimitType='0') # 按机型调价（有穷举调价，在有效期内）
    # base_price_evaluatee(channelId='10000060', pid='0', productId='41567', ip='127.0.0.1', freqLimitType='0') # 按机型调价（有穷举调价，不在有效期内）

    '''一、【自主调价 - 不自动使用 - 未命中】渠道 - 当前使用的定价版本时间：2021-05-25 23:05:43 | 回收定价有更新 | 历史版本 基准价 未命中调价方案规则'''
    # iPhone X， 历史版本：1395  基准价：1958  |  线上版本：1396  基准价：2002
    # 不使用自动使用版本方案，没有命中基础加成方案，重新计算现网系数价格  |  再用机型现网版本计算获取一次定价价格，即为最终价格（不再匹配调价规则了）
    base_price_evaluatee(channelId='10000060', pid='0', productId='41567', ip='127.0.0.1', freqLimitType='0')  # 按机型调价（有穷举调价，不在有效期内）

    # evaType：价格2.0 质检类型，1-57标准质检，2-大质检  |  暂不测试

'''
【外部接口】 【销售价应用方案估价接口】【第一版】【商家自检 - 价格查询 当下在用】

【BasePriceEvaluate】
【基础】
formParam: {ChannelId:10000060 Pid:0 ProductId:41567 EvaType:0 Select:[] Ip:127.0.0.1 UserId:1002 SkuItem:[12 471 18 2236 38 1091 2242] OptItem:[8297 8301 8305 8309 8312 8316 8320 8323 8326 8333 8336 8339 8343 8349 8351 8359 8361 8364 8367 8371 8375 8378 8382 8385 8389 8393 8397 8403 8408 8412 8416 8419 8422 8425 8429 8432 8436 8441 8444 8449] PriceType:2 FreqLimitType:0}
redigo: HGET BasePriceProduct 41567 &{ProductId:41567 ClassId:1 BrandId:2 Status:1 PriceState:1 PauState:1 RecycState:1 SyncPriceState:1 UserName:张金发_TEST CreateTime:2021-01-28 16:56:39 +0000 UTC UpdateTime:2021-05-19 15:03:55.246 +0000 UTC}
baseProductInfo: {ProductId:41567 ClassId:1 BrandId:2 Status:1 PriceState:1 PauState:1 RecycState:1 SyncPriceState:1 UserName:张金发_TEST CreateTime:2021-01-28 16:56:39 +0000 UTC UpdateTime:2021-05-19 15:03:55.246 +0000 UTC}
redigo: HGET ChannelAdjustPlan 10000060#0#2 &{Id:97 ChId:10000060 Pid:0 PlanId:54 ChType:1 PriceType:2 Status:1 CreateTime:2021-05-25 23:09:42.232 +0000 UTC UpdateTime:0001-01-01 00:00:00 +0000 UTC UserName:张金发_TEST}
redigo: HGET AdjustPlan 54 &{PlanId:54 PlanName:0525-回收-自主调价-不自动使用（金发测试验证，大家勿动） Remarks:0525-回收-自主调价-不自动使用（金发测试验证，大家勿动） AdjustmentType:1 BasePlanId:0 State:1 CreateTime:2021-05-25 23:05:43.011 +0000 UTC UpdateTime:2021-05-26 16:04:41.125 +0000 UTC UserName:张金发_TEST PriceType:2 BeginTime:2021-05-12 23:04:43 +0000 UTC EndTime:2021-06-12 23:04:43 +0000 UTC PlanVersion:3 AutomaticVersion:0 VersionTime:2021-05-25 23:05:43 +0000 UTC ClassBranchPriceRule:[{ClassList:[1] BrandList:[2] PricePlusList:[{Begin:100 End:200000 Percent:99 Absolute:0 Type:1 PriceType:1}]}] ProductRule:[]}
不自动使用版本, 时间: 2021-05-25 23:05:43 +0000 UTC
filter: map[Fcreate_time:map[$lte:2021-05-25 23:05:43 +0000 UTC] Fproduct_id:41567]
result: ......   ReviewId:1395    ......

【获取回收定价价格】
checkSkuItem() Start ...
GetLevelStandardLevelId() Start ...
optItem: [8297 8301 8305 8309 8312 8316 8320 8323 8326 8333 8336 8339 8343 8349 8351 8359 8361 8364 8367 8371 8375 8378 8382 8385 8389 8393 8397 8403 8408 8412 8416 8419 8422 8425 8429 8432 8436 8441 8444 8449]

【获取 机型 关联的商品等级标准】
levelOrderMap: map[0:600 1:590 2:580 3:570 4:530 5:520 6:510 7:460 8:450 9:440 10:430 11:429 12:428 13:427 14:426 15:425 16:424 17:423 18:422 19:370 20:360 21:350 22:340 23:330 24:329 25:328 26:327 27:270 28:260 29:250 30:240 31:230 32:220 33:210 34:200 35:190 36:189 37:188 38:180 39:170 40:160 41:150 42:149 43:148 44:147 45:140 46:130 47:120 48:110 49:100 50:90 51:80 52:70 53:60 54:50 55:40 56:39 57:38]
levelSaleMap: map[38:50 39:50 40:60 50:60 60:60 70:90 80:90 90:100 100:100 110:130 120:130 130:140 140:140 147:170 148:170 149:170 150:170 160:180 170:180 180:180 188:210 189:210 190:210 200:220 210:220 220:220 230:260 240:260 250:270 260:270 270:270 327:350 328:350 329:350 330:350 340:360 350:360 360:360 370:370 422:450 423:450 424:450 425:450 426:450 427:460 428:460 429:480 430:480 440:490 450:490 460:500 510:510 520:520 530:530 570:570 580:580 590:590 600:600]
match order: 18, itemComb: [8309 8312 8305]
match level: 422, saleLevel: 450
redigo: HGET BaseLevelInfo 422 &{Id:422 Name:C12 Status:1 ClassId:1}
redigo: HGET SaleLevelInfo 450 &{Id:450 Name:C2 Desc: Status:1 ClassId:1}
HMGET [LevelLabelInfo 6 3 5 4] map[interface {}]interface {}{3:(*commodel.TPriceLevelLabel)(0xc0002d2240), 4:(*commodel.TPriceLevelLabel)(0xc0002d22a0), 5:(*commodel.TPriceLevelLabel)(0xc0002d2270), 6:(*commodel.TPriceLevelLabel)(0xc0002d2210)}

checkCombPrice() Start ...
basePrice: 195800.000000
sku: 12 value: 500.000000 price: 196300.000000              大陆国行
sku: 18 value: 0.000000 price: 196300.000000                剩余保修期不足一个月或过保
sku: 38 value: 35510.000000 price: 231810.000000            256GB
sku: 471 value: -1660.000000 price: 230150.000000           移动联通
sku: 1091 value: 0.000000 price: 230150.000000              深空灰色
sku: 2236 value: 0.000000 price: 230150.000000              3GB
sku: 2242 value: -5650.000000 price: 224500.000000          A1903
level: 422 value: 840 price: 188580.000000

【基准回收价】
公式：（（1 - 等级预期毛利率） *  等级系数  * （ 初始化价格 + sku差值 ）/ 1.03* 1.01）
也即：（（1 - 等级预期毛利率） *  回收定价 ）/ 1.03* 1.01）
(1 - 220/1000.0) * 188580.000000 / 1.03 * 1.01
gmv price: 144236.234375
Format Evaluate Price: 144236.234375
base price: 144236.234375 -> 144200

【走回收调价方案逻辑】
GetAdjustPrice() Start ...
AdjustPlanInfo: &{Price:144200 Level:422 ProductId:41567 ClassId:1 BrandId:2 BasePrice:195800 Skuitem:[12 18 38 471 1091 2236 2242] PriceAdjPlan:0xc000620240 PriceAdjPlan2nd:<nil>}

【匹配回收调价方案，调价规则】
Matching Product Rule
Matching Class Brand Price Rule

【命中调价规则】
BasePriceType matching!!! BasePrice: 195800
    【命中1：按按类目+品牌+初始化价格范围调价 规则 - 按比例加成】
    rule value: {Begin:100 End:200000 Percent:99 Absolute:0 Type:1 PriceType:1}
    144200.000000 * ((99 / 1000) + 1) = 158475.796875
    Price: 158475.796875
    Format Evaluate Price: 158475.796875
    
    
    【命中2：按按类目+品牌+初始化价格范围调价 规则 - 按绝对值加成】
    
    【命中3：按机型调价 规则 - 按比例加成】
    
    【命中4：按机型调价 规则 - 按绝对值金额加成】
    
【生成定价估价记录】
Mgo Query: map[_id:eva_record_2105]
Mgo Change: {Update:map[$inc:map[sequence_value:1]] Replace:false Remove:false Upsert:false ReturnNew:false}
Mgo Result: {Sequence:101741}
EvaRecord: &{EvaluateId:101741 ProductId:41567 BasePrice:195800 SbuType:2 EvaType:0 VersionId:10 OptLevelId:422 Select:[12 471 18 2236 38 1091 2242 8297 8301 8305 8309 8312 8316 8320 8323 8326 8333 8336 8339 8343 8349 8351 8359 8361 8364 8367 8371 8375 8378 8382 8385 8389 8393 8397 8403 8408 8412 8416 8419 8422 8425 8429 8432 8436 8441 8444 8449] SkuItem:[12 18 38 471 1091 2236 2242] OptItem:[8297 8301 8305 8309 8312 8316 8320 8323 8326 8333 8336 8339 8343 8349 8351 8359 8361 8364 8367 8371 8375 8378 8382 8385 8389 8393 8397 8403 8408 8412 8416 8419 8422 8425 8429 8432 8436 8441 8444 8449] LevelTempId:0 Quatation:158400 ErrorCode:0 ErrorInfo:Success SpendTime:51 CreateTime:2021-05-26 16:17:40.747341382 +0000 UTC Interface:evaluate EvaBasePrice:144200 IP:127.0.0.1 UserId:1002 ChannelId:10000060 Pid:0 LevelStandId:2 SaleLevelId:450 BaseLevelTag:[6 3] SaleLevelTag:[5 4] AdjPlanId:54 AdjPlanVer:3 AdjustPrice:158400 AdjPlanId2nd:0 AdjPlanVer2nd:0 AdjustPrice2nd:0 OptLevelName:C12 SaleLevelName:C2}
'''

'''
【不自动使用】【未命中】
【1. 用历史版本先计算一次】
不自动使用版本, 时间: 2021-05-25 23:05:43 +0000 UTC
定价价格计算开始 ...
校验SKU选项 ...
机况-匹配价格等级标准开始 ...
...
机况-匹配价格等级标准结束 ...
匹配穷举价格 ...
按系数计算定价价格 ...
定价价格计算结束 ...
加成价格计算开始 ...
不进行2次加成计算
加成价格计算结束 ...
不使用自动使用版本方案，没有命中基础加成方案，重新计算现网系数价格

【2. 用现网版本再计算一次】
定价价格计算开始 ...
校验SKU选项 ...
机况-匹配价格等级标准开始 ...
机况-匹配价格等级标准结束 ...
匹配穷举价格 ...
按系数计算定价价格 ...
    basePrice: 200200.000000
    sku: 12 value: 400.000000 price: 200600.000000
    sku: 18 value: 100.000000 price: 200700.000000
    sku: 38 value: 35410.000000 price: 236110.000000
    sku: 471 value: -1760.000000 price: 234350.000000
    sku: 1091 value: 100.000000 price: 234450.000000
    sku: 2236 value: 100.000000 price: 234550.000000
    sku: 2242 value: -5550.000000 price: 229000.000000
    level: 422 value: 844 price: 193276.000000
    gmv: (1 - 211/1000.0) * 193276.000000 / 1.03 * 1.01
    gmv price: 149533.703125
定价价格计算结束 ..
【第一次，未命中； 用现网的版本，不匹配调价规则，只计算获取定价价格】
'''