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
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test, hsb_eva_ipProxy_k8s_test, hsb_response_print

class Base_Price_Evaluatee:
    def product_check_item_34(self, productId):
        param = {"_head": {"_interface": "product_check_item_34", "_msgType": "request", "_remark": "", "_version": "0.01","_timestamps": "123456", "_invokeId": "test_zhangjinfa", "_callerServiceId": "112006", "_groupNo": "1"},"_param": {"productId": productId}}
        secret_key = "gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU"
        callerserviceid = "112006"
        url = "http://codserver.huishoubao.com/detect/product_check_item"
        md5value = json.dumps(param) + "_" + secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID": callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典
        checkList = respone_dict['_data']['_data']['checkList']
        skuList = respone_dict['_data']['_data']['skuList']

        strCheckList = []
        strCheckDesc = ''
        for info in checkList:
            answerList = info['answerList']
            '''第一种方式：在answerList下随机取1个'''
            # index = random.randint(0, len(answerList) - 1)
            # strCheckList.append(answerList[index]['answerId'])
            # strCheckDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'

            '''第二种方式：在answerList下取answerWeight最大的那个'''
            index = sorted(answerList, key=lambda x: int(x['answerWeight']), reverse=True)[0]
            strCheckList.append(index['answerId'])
            strCheckDesc += '"' + info['questionName'] + ":" + index['answerName'] + '",'

        strSkuList = []
        strSkuDesc = ''
        for info in skuList:
            answerList = info['answerList']
            index = random.randint(0, len(answerList) - 1)
            strSkuList.append(answerList[index]['answerId'])
            strSkuDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'

        return strSkuList, strSkuDesc, strCheckList, strCheckDesc

    def base_price_evaluatee(self, channelId, pid, productId, ip, freqLimitType):
        (strSkuList, strSkuDesc, strCheckList, strCheckDesc) = self.product_check_item_34(productId=productId)
        # strSkuList = ['12', '471', '18', '2236', '38', '1091', '2242']
        # strCheckList = ['9016', '9019', '9027', '9029', '9037', '9039', '9052', '9056', '9057', '9059', '9062', '9070', '9072', '9074', '7559', '9078', '9079', '9081', '7575', '9082', '9086', '9088', '9090', '9095', '9099', '9104', '9106', '9113', '9117', '7532']

        # evaType：3-34标准质检  |  priceType：价格类型，1-销售定价
        param = {"_head":{"_interface":"evaluate","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"1525332832","_invokeId":"mikingzhang_adjustPrice","_callerServiceId":"116006","_groupNo":"1"},"_param":{"channelId":channelId, "pid":pid, "productId":productId, "evaType":"3", "skuItem":strSkuList, "optItem":strCheckList, "ip":ip, "userId":"1002", "priceType":"1", "freqLimitType":freqLimitType}}
        secret_key = "R2gFCRbILiNhwv3YbtaGceYJlPS5Ku02"
        callerserviceid = "116006"
        url = "http://bpeserver.huishoubao.com/base_price/evaluate"
        md5value = json.dumps(param) + "_" + secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_k8s_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典

        print('========>1.『{0}』 产品的『检测标准化选项-sku』(随机取)为：\n'.format(productId), strSkuList)
        print('\n========>2. 以上『检测标准化选项-sku』为：\n', '{' + strSkuDesc[:-1] + '}')
        print('\n========>3.『{0}』 产品的『检测标准化选项-机况-34』(随机取)为：\n'.format(productId), strCheckList)
        print('\n========>4. 以上『检测标准化选项-机况-34』为：\n', '{' + strCheckDesc[:-1] + '}')
        hsb_response_print(respone=respone)

if __name__ == '__main__':
    baseprice_23 = Base_Price_Evaluatee()
    '''一、销售价应用 - 自主运营（销售调价，接口返回是没有 定价和销售等级标签概念的，没有用到等级标准）'''
    # strSkuList = ['12', '471', '18', '2236', '38', '1091', '2242']
    # strCheckList = ['9016', '9019', '9027', '9029', '9037', '9039', '9052', '9056', '9057', '9059', '9062', '9070','9072', '9074', '7559', '9078', '9079', '9081', '7575', '9082', '9086', '9088', '9090', '9095','9099', '9104', '9106', '9113', '9117', '7532']  # 9027，命中，"levelId":"600","levelName":"S"

    # 正常场景：渠道 - 命中：按类目+品牌+初始化价格范围调价 - 价格结果范围 - 按比例加成  |  正常
    # 1. 34项苹果安卓定价模板v1（iPhone3G-3GS或低端安卓）（ID 34）
    # baseprice_23.base_price_evaluatee(channelId='10000837', pid='3413', productId='23007', ip='127.0.0.1', freqLimitType='0') #商家自检-卖家参考价（无sku机型） | 小米 1
    # 2. 34项苹果定价模板v1（iPhone4-5c）（ID 28）
    # baseprice_23.base_price_evaluatee(channelId='10000837', pid='3413', productId='3', ip='127.0.0.1', freqLimitType='0') #商家自检-卖家参考价 | iPhone 4
    # baseprice_23.base_price_evaluatee(channelId='10000837', pid='3413', productId='30751', ip='127.0.0.1', freqLimitType='0') #商家自检-卖家参考价 | iPhone 5  未定价机型
    # baseprice_23.base_price_evaluatee(channelId='10000837', pid='3413', productId='31238', ip='127.0.0.1', freqLimitType='0') #商家自检-卖家参考价 | iPhone 7  下架机型
    # 3. 34项安卓定价模板v1（安卓简易无指纹）（ID 33）
    # baseprice_23.base_price_evaluatee(channelId='10000837', pid='3413', productId='30932', ip='127.0.0.1', freqLimitType='0') #商家自检-卖家参考价 | 乐视 乐Max Pro
    # 4. 34项标准质检模板：34项安卓定价模板v1（安卓简易有指纹）（ID 32）
    # baseprice_23.base_price_evaluatee(channelId='10000837', pid='3413', productId='64000', ip='127.0.0.1', freqLimitType='0') #商家自检-卖家参考价 | 华为 P40（5G）
    # baseprice_23.base_price_evaluatee(channelId='10000837', pid='3413', productId='63904', ip='127.0.0.1', freqLimitType='0') #商家自检-卖家参考价 | vivo iQOO 3（5G）
    # baseprice_23.base_price_evaluatee(channelId='10000837', pid='3413', productId='3121', ip='127.0.0.1', freqLimitType='0') #商家自检-卖家参考价 | vivo X7
    # baseprice_23.base_price_evaluatee(channelId='10000837', pid='3413', productId='59939', ip='127.0.0.1', freqLimitType='0') #商家自检-卖家参考价 | 小米 9
    # baseprice_23.base_price_evaluatee(channelId='10000837', pid='3413', productId='60107', ip='127.0.0.1', freqLimitType='0') #商家自检-卖家参考价 | vivo X27
    # baseprice_23.base_price_evaluatee(channelId='10000837', pid='3413', productId='64536', ip='127.0.0.1', freqLimitType='0') #商家自检-卖家参考价 | 华为 Mate 40 Pro+（5G）
    # 6. 34项标准质检模板：34项苹果定价模板v1（iPhone6-8P及以上）（ID 26）
    # baseprice_23.base_price_evaluatee(channelId='10000837', pid='3413', productId='38201', ip='127.0.0.1', freqLimitType='0') #商家自检-卖家参考价 | iPhone 8 Plus
    # baseprice_23.base_price_evaluatee(channelId='10000837', pid='3413', productId='38200', ip='127.0.0.1', freqLimitType='0') #商家自检-卖家参考价 | iPhone 8
    # baseprice_23.base_price_evaluatee(channelId='10000837', pid='3413', productId='30833', ip='127.0.0.1', freqLimitType='0') #商家自检-卖家参考价 | iPhone 6s Plus
    # baseprice_23.base_price_evaluatee(channelId='10000837', pid='3413', productId='30832', ip='127.0.0.1', freqLimitType='0') #商家自检-卖家参考价 | iPhone 7 Plus
    # 7. 34项标准质检模板：34项苹果定价模板v1（iPhoneX及以上）（ID 25）
    # baseprice_23.base_price_evaluatee(channelId='10000837', pid='3413', productId='41567', ip='127.0.0.1', freqLimitType='0') #商家自检-卖家参考价 | iPhone X
    # baseprice_23.base_price_evaluatee(channelId='10000837', pid='3413', productId='63330', ip='127.0.0.1', freqLimitType='0') #商家自检-卖家参考价 | iPhone 11
    # baseprice_23.base_price_evaluatee(channelId='10000837', pid='3413', productId='64494', ip='127.0.0.1', freqLimitType='0') #商家自检-卖家参考价 | iPhone 12
    # baseprice_23.base_price_evaluatee(channelId='10000837', pid='3413', productId='64493', ip='127.0.0.1', freqLimitType='0') #商家自检-卖家参考价 | iPhone 12 mini
    # baseprice_23.base_price_evaluatee(channelId='10000837', pid='3413', productId='64495', ip='127.0.0.1', freqLimitType='0') #商家自检-卖家参考价 | iP/hone 12 Pro
    # baseprice_23.base_price_evaluatee(channelId='10000837', pid='3413', productId='64496', ip='127.0.0.1', freqLimitType='0') #商家自检-卖家参考价 | iPhone 12 Pro Max
    # baseprice_23.base_price_evaluatee(channelId='10000837', pid='3413', productId='54789', ip='127.0.0.1', freqLimitType='0') #商家自检-卖家参考价 | iPhone XS Max
    # baseprice_23.base_price_evaluatee(channelId='10000837', pid='3413', productId='54790', ip='127.0.0.1', freqLimitType='0') #商家自检-卖家参考价 | iPhone XS
    # baseprice_23.base_price_evaluatee(channelId='10000837', pid='3413', productId='54791', ip='127.0.0.1', freqLimitType='0') #商家自检-卖家参考价 | iPhone XR
    # baseprice_23.base_price_evaluatee(channelId='10000837', pid='3413', productId='63328', ip='127.0.0.1', freqLimitType='0') #商家自检-卖家参考价 | iPhone 11 Pro
    # baseprice_23.base_price_evaluatee(channelId='10000837', pid='3413', productId='63329', ip='127.0.0.1', freqLimitType='0') #商家自检-卖家参考价 | iPhone 11 Pro
    # baseprice_23.base_price_evaluatee(channelId='10000837', pid='3413', productId='63330', ip='127.0.0.1', freqLimitType='0') #商家自检-卖家参考价 | iPhone 11

    # 正常场景：渠道 - 命中：按类目+品牌+初始化价格范围调价 - 价格结果范围 - 按金额加成  |  正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', ip='127.0.0.1', freqLimitType='0')

    # 正常场景：渠道 - 命中：按类目+品牌+初始化价格范围调价 - 初始化价格范围 - 按比例加成  |  拿 机型基准价 去匹配 初始化价格范围  |  正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', ip='127.0.0.1', freqLimitType='0')

    # 正常场景：渠道 - 命中：按类目+品牌+初始化价格范围调价 - 初始化价格范围 - 按金额加成  |  拿 机型基准价 去匹配 初始化价格范围  |  正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', ip='127.0.0.1', freqLimitType='0')

    # 正常场景：渠道 - 按类目+品牌+初始化价格范围调价 - 初始化价格范围 or 价格结果范围  范围段符合，但是  类目 or 品牌 不符合【未命中】  |  不走调价，正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', ip='127.0.0.1', freqLimitType='0')

    # 正常场景：渠道 - 命中：按机型调价规则 - 按比例加成  |  正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', ip='127.0.0.1', freqLimitType='0')

    # 正常场景：渠道 - 命中：按机型调价规则 - 按金额加成  |  正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', ip='127.0.0.1', freqLimitType='0')

    # 正常场景：渠道 - 同时命中：按类目+品牌+初始化价格范围调价 以及 按机型调价规则   |  正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', ip='127.0.0.1', freqLimitType='0')

    # 正常场景：渠道 - 没有命中任何规则  |  正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', ip='127.0.0.1', freqLimitType='0')

    baseprice_23.base_price_evaluatee(channelId='10000837', pid='3413', productId='30932', ip='127.0.0.1', freqLimitType='0')

'''
【外部接口】 【销售价应用方案估价接口】【第一版】【商家自检 - 价格查询 当下在用】

【补充：销售价应用方案 - 加成规则】
    priceType：价格类型，1-基准价，2-价格结果 ----------2021.5 专业版-价格查询新增
    
【BasePriceEvaluate】
【基础】
formParam: {ChannelId:40000001 Pid:0 ProductId:41567 EvaType:3 Select:[] Ip:127.0.0.1 UserId:1002 SkuItem:[12 471 18 2236 38 1091 2242] OptItem:[9016 9019 9027 9029 9037 9039 9052 9056 9057 9059 9062 9070 9072 9074 7559 9078 9079 9081 7575 9082 9086 9088 9090 9095 9099 9104 9106 9113 9117 7532] PriceType:1 FreqLimitType:0}
redigo: HGET BasePriceProduct 41567 &{ProductId:41567 ClassId:1 BrandId:2 Status:1 PriceState:1 PauState:1 RecycState:1 SyncPriceState:1 UserName:张金发_TEST CreateTime:2021-01-28 16:56:39 +0000 UTC UpdateTime:2021-05-19 15:03:55.246 +0000 UTC}
baseProductInfo: {ProductId:41567 ClassId:1 BrandId:2 Status:1 PriceState:1 PauState:1 RecycState:1 SyncPriceState:1 UserName:张金发_TEST CreateTime:2021-01-28 16:56:39 +0000 UTC UpdateTime:2021-05-19 15:03:55.246 +0000 UTC}
redigo: HGET ChannelAdjustPlan 40000001#0#1 &{Id:15 ChId:40000001 Pid:0 PlanId:51 ChType:1 PriceType:1 Status:1 CreateTime:2021-04-15 18:38:04.6 +0000 UTC UpdateTime:0001-01-01 00:00:00 +0000 UTC UserName:张金发_TEST}
redigo: HGET AdjustPlan 51 &{PlanId:51 PlanName:0522-自主运营（金发测试验证，大家勿动） Remarks:0522-自主运营（金发测试验证，大家勿动，谢谢） AdjustmentType:1 BasePlanId:0 State:1 CreateTime:2021-05-22 17:29:28.719 +0000 UTC UpdateTime:2021-05-22 17:29:37.148 +0000 UTC UserName:张金发_TEST PriceType:1 BeginTime:2021-05-21 17:25:54 +0000 UTC EndTime:2021-06-21 17:25:54 +0000 UTC PlanVersion:1 AutomaticVersion:1 VersionTime:0001-01-01 00:00:00 +0000 UTC ClassBranchPriceRule:[{ClassList:[1] BrandList:[2] PricePlusList:[{Begin:100 End:999900 Percent:111 Absolute:0 Type:1 PriceType:2}]}] ProductRule:[]}

【获取定价价格】
checkSkuItem() Start ...
GetLevelTempLevelId() Start ...
optItem: [9016 9019 9027 9029 9037 9039 9052 9056 9057 9059 9062 9070 9072 9074 7559 9078 9079 9081 7575 9082 9086 9088 9090 9095 9099 9104 9106 9113 9117 7532]
使用34项>等级模板配置等级
levelOrderMap: map[0:600 1:590 2:580 3:570 4:560 5:550 6:540 7:530 8:520 9:510 10:500 11:490 12:460 13:450 14:440 15:430 16:420 17:410 18:400 19:370 20:360 21:350 22:340 23:330 24:320 25:310 26:300 27:290 28:270 29:260 30:250 31:220 32:210 33:180 34:170 35:160 36:150 37:140 38:130 39:100 40:90 41:60 42:50 43:30 44:20]
match order: 0, itemComb: [9027]
match level: 600
redigo: HGET BaseLevelInfo 600 &{Id:600 Name:S Status:1 ClassId:1}

checkCombPrice() Start ...
basePrice: 161600.000000
sku: 12 value: 1.000000 price: 161601.000000
sku: 18 value: 0.000000 price: 161601.000000
sku: 38 value: 53419.000000 price: 215020.000000
sku: 471 value: -1767.000000 price: 213253.000000
sku: 1091 value:1.000000 price: 213254.000000
sku: 2236 value:0.000000 price: 213254.000000
sku: 2242 value:-5753.000000 price: 207501.000000
level: 600 value:1410 price: 292576.406250
base price: 292576.406250 -> 292500

【走销售价应用方案逻辑】
GetAdjustPrice() Start ...
AdjustPlanInfo: &{Price:292500 Level:600 ProductId:41567 ClassId:1 BrandId:2 BasePrice:161600 Skuitem:[12 18 38 471 1091 2236 2242] PriceAdjPlan:0xc0000b0240 PriceAdjPlan2nd:<nil>}
【匹配销售价应用方案，调价规则】
Matching Product Rule
Matching Class Brand Price Rule
【命中调价规则】
matching!!!
    【命中1：按按类目+品牌+初始化价格范围调价 规则 - 按比例加成】
    rule value: {Begin:100 End:999900 Percent:111 Absolute:0 Type:1 PriceType:2}
    292500.000000 * ((111 / 1000) + 1) = 324967.531250
    Price: 324967.531250
    【命中2：按按类目+品牌+初始化价格范围调价 规则 - 按绝对值加成】
    
    【命中3：按机型调价 规则 - 按比例加成】
    【命中4：按机型调价 规则 - 按绝对值金额加成】
    
【生成定价估价记录】
Mgo Query: map[_id:eva_record_2105]
Mgo Change: {Update:map[$inc:map[sequence_value:1]] Replace:false Remove:false Upsert:false ReturnNew:false}
Mgo Result: {Sequence:89632}
EvaRecord: &{EvaluateId:89632 ProductId:41567 BasePrice:161600 SbuType:2 EvaType:3 VersionId:196 OptLevelId:600 Select:[12 471 18 2236 38 1091 2242 9016 9019 9027 9029 9037 9039 9052 9056 9057 9059 9062 9070 9072 9074 7559 9078 9079 9081 7575 9082 9086 9088 9090 9095 9099 9104 9106 9113 9117 7532] SkuItem:[12 18 38 471 1091 2236 2242] OptItem:[9016 9019 9027 9029 9037 9039 9052 9056 9057 9059 9062 9070 9072 9074 7559 9078 9079 9081 7575 9082 9086 9088 9090 9095 9099 9104 9106 9113 9117 7532] LevelTempId:15 Quatation:324900 ErrorCode:0 ErrorInfo:Success SpendTime:23 CreateTime:2021-05-23 20:56:00.819300037 +0000 UTC Interface:evaluate EvaBasePrice:292500 IP:127.0.0.1 UserId:1002 ChannelId:40000001 Pid:0 LevelStandId:0 SaleLevelId:0 BaseLevelTag:[] SaleLevelTag:[] AdjPlanId:51 AdjPlanVer:1 AdjustPrice:324900 AdjPlanId2nd:0 AdjPlanVer2nd:0 AdjustPrice2nd:0 OptLevelName:S SaleLevelName:}
'''