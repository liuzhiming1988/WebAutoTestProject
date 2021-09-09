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
    限频风控：redis-cli -h EVA_REDIS_HOST -a hsb_redis_123
        SET E_FL_TD_BPE_1 1          两次请求时间间隔
        SET E_FL_BT_TD_BPE_1 3       计算临时黑名单时间周期(分钟)
        SET E_FL_BT_TC_BPE_1 10     计算临时黑名单时间间隔中的次数(默认10)
        SET E_FL_BT_T_BPE_1 30      进入临时黑名单时间(分钟)    （进入临时黑名单会钉钉告警）
        HSET E_FL_W_BPE_1 127.0.0.1  '"whitelist_127.0.0.1"'   白名单
        HSET E_FL_B_BPE_1 127.0.0.1  '"blacklist_127.0.0.1"'   黑名单
    进入临时黑名单，钉钉通知内容
        告警(环境: dev):
        Service: BPE_1
        Restrictions: 127.10.10.15
        频率限制，进入临时黑名30分钟
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test, hsb_response_print

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
        # print(respone.text)
        checkList = respone_dict['_data']['_data']['checkList']
        skuList = respone_dict['_data']['_data']['skuList']

        strCheckList = []
        strCheckDesc = ''
        for info in checkList:
            answerList = info['answerList']
            index = random.randint(0, len(answerList) - 1)
            strCheckList.append(answerList[index]['answerId'])
            strCheckDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'

        strSkuList = []
        strSkuDesc = ''
        for info in skuList:
            answerList = info['answerList']
            index = random.randint(0, len(answerList) - 1)
            strSkuList.append(answerList[index]['answerId'])
            strSkuDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'

        return strSkuList, strSkuDesc, strCheckList, strCheckDesc

    def base_price_evaluatee(self, channelId, pid, productId, evaType, ip, userId, priceType, freqLimitType):
        # (strSkuList, strSkuDesc, strCheckList, strCheckDesc) = self.product_check_item_34(productId=productId)
        strSkuList = ['12', '471', '18', '2236', '38', '1091', '2242']
        strCheckList = ['9016', '9019', '9027', '9029', '9037', '9039', '9052', '9056', '9057', '9059', '9062', '9070','9072', '9074', '7559', '9078', '9079', '9081', '7575', '9082', '9086', '9088', '9090', '9095','9099', '9104', '9106', '9113', '9117', '7532']
        param = {"_head":{"_interface":"evaluate","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"1525332832","_invokeId":"mikingzhang_adjustPrice","_callerServiceId":"116006","_groupNo":"1"},"_param":{"channelId":channelId, "pid":pid, "productId":productId, "evaType":evaType,"skuItem":strSkuList, "optItem":strCheckList, "ip":ip, "userId":userId,"priceType":priceType, "freqLimitType":freqLimitType}}

        secret_key = "R2gFCRbILiNhwv3YbtaGceYJlPS5Ku02"
        callerserviceid = "116006"
        url = "http://bpeserver.huishoubao.com/base_price/evaluate"
        md5value = json.dumps(param) + "_" + secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典

        # print('========>1.『{0}』 产品的『检测标准化选项-sku』(随机取)为：\n'.format(productId), strSkuList)
        # print('\n========>2. 以上『检测标准化选项-sku』为：\n', '{' + strSkuDesc[:-1] + '}')
        # print('\n========>3.『{0}』 产品的『检测标准化选项-机况-34』(随机取)为：\n'.format(productId), strCheckList)
        # print('\n========>4. 以上『检测标准化选项-机况-34』为：\n', '{' + strCheckDesc[:-1] + '}')
        hsb_response_print(respone=respone)

if __name__ == '__main__':
    baseprice_23 = Base_Price_Evaluatee()
    # strSkuList = ['12', '471', '18', '2236', '38', '1091', '2242']
    # strCheckList = ['9016', '9019', '9027', '9029', '9037', '9039', '9052', '9056', '9057', '9059', '9062', '9070','9072', '9074', '7559', '9078', '9079', '9081', '7575', '9082', '9086', '9088', '9090', '9095','9099', '9104', '9106', '9113', '9117', '7532']  # 9027，命中，"levelId":"600","levelName":"S"

    # freqLimitType 传空 | "_errStr":"请求参数错误 [FreqLimitType为必填字段]"
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', evaType='3', ip='127.0.0.1', userId='052401', priceType='1', freqLimitType='')

    # freqLimitType 传非0 1 2  |  "_errStr":"请求参数错误 [FreqLimitType必须是[0 1 2]中的一个]"
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', evaType='3', ip='127.0.0.1', userId='052401', priceType='1', freqLimitType='55')

    # 【频率限制 UserId】【 两次请求时间间隔 限频】  freqLimitType 传2  |  "_errStr":"操作过于频繁，请稍后再试","_data":null,"_errCode":"999","_ret":"999"
    # for i in range(5):
    #     baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', evaType='3', ip='127.0.0.1', userId='052401', priceType='1', freqLimitType='2')

    # 【频率限制 UserId】【临时黑名单，3分钟触发了5次限频】  freqLimitType 传2
    # AllowedThrough|113|Freq Limit: [052401] In Black Temp List: 2021-05-24 15:54:00
    # "_errStr":"操作过于频繁，请稍后再试"
    # for i in range(2):
    #     baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', evaType='3', ip='127.0.0.1', userId='052401', priceType='1', freqLimitType='2')

    # 【频率限制 IP】【临时黑名单，3分钟触发了5次限频】  freqLimitType 传1
    # Freq Limit: [127.0.0.24] In Black Temp List: 2021-05-24 16:42:49
    # "_errStr":"操作过于频繁，请稍后再试"
    # for i in range(2):
    #     baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', evaType='3', ip='127.0.0.24', userId='052401', priceType='1', freqLimitType='1')

    # 【限频风控】【IP userid 白名单】  |  IP已经入临时黑名单  |  不受白名单影响 （有需求，可以操作删除临时黑名单记录）
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', evaType='3', ip='127.0.0.24', userId='052401', priceType='1', freqLimitType='1')

    # 【限频风控】【IP userid 白名单】  | 请求不受限（包括一秒限频）
    # for i in range(2):
    #     baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', evaType='3', ip='127.0.0.25', userId='052401', priceType='1', freqLimitType='1')
        # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', evaType='3', ip='127.0.0.25', userId='252402', priceType='1', freqLimitType='2')

    # 【限频风控】【IP userid 黑名单】  |  请求受限  |  "_errStr":"操作过于频繁，请稍后再试","_data":null,"_errCode":"999","_ret":"999"
    baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', evaType='3', ip='127.0.0.26', userId='052403', priceType='1', freqLimitType='1')
    baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', evaType='3', ip='127.0.0.26', userId='052403', priceType='1', freqLimitType='2')
'''
【外部接口】 【销售价应用方案估价接口】【第一版】【商家自检 - 价格查询 当下在用】

【限频】
1、临时黑名单是没有记录的（也可以操作删除）
2、已进入临时黑名单的IP，不受白名单的影响（有需求，可以操作删除临时黑名单记录）
3、白黑名单可到IP和UserId

【钉钉通知】EvaluateToolsGo

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