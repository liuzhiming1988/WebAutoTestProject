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

class Base_Price_Evaluatee:
    def pdt_sku_query(self, productId):
        param = {"_head": {"_interface": "pdt_sku_query", "_msgType": "request", "_remark": "", "_version": "0.01","_timestamps": "123", "_invokeId": "111", "_callerServiceId": "112002", "_groupNo": "1"},"_param": {"subInterface": "sku_option_combination_get","info": {"productId": productId}}}
        secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
        callerserviceid = "112002"
        url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
        md5value = json.dumps(param) + "_" + secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID": callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典
        optionsList = respone_dict['_body']['_data']['options']

        str_sku_answer_list = []
        str_Option_answer_desc = ''
        for info in optionsList:
            answerList = info['aInfo']
            index = random.randint(0, len(answerList) - 1)
            str_sku_answer_list.append(answerList[index]['aId'])
            str_Option_answer_desc += '"' + info['qName'] + ":" + answerList[index]['aName'] + '",'

        return str_sku_answer_list, str_Option_answer_desc

    def product_6_eva_option_get(self, channel_id, product_id, pid):
        param = {"_head": {"_interface": "eva_option_get", "_msgType": "request", "_remark": "hello", "_version": "0.01","_timestamps": "123", "_invokeId": "111", "_callerServiceId": "112002", "_groupNo": "1"},"_param": {"channel_id": channel_id, "product_id": product_id, "pid": pid}}
        secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
        callerserviceid = "112002"
        url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
        md5value = json.dumps(param) + "_" + secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID": callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典
        print(respone_dict)
        options_list = respone_dict['_body']['_data']['itemList']

        str_options_list = []
        str_options_list_desc = ''
        for info in options_list:
            answerList = info['question']
            index = random.randint(0, len(answerList) - 1)
            if info['conftype'] != '1':
                str_options_list.append(answerList[index]['id'])
                str_options_list_desc += '"' + info['name'] + ":" + answerList[index]['name'] + '",'

        return str_options_list, str_options_list_desc

    def base_price_evaluatee(self, channelId, pid, productId, ip, freqLimitType):
        (str_sku_answer_list, str_Option_answer_desc) = self.pdt_sku_query(productId=productId)
        # (str_options_list, str_options_list_desc) = self.product_6_eva_option_get(channel_id=channelId, product_id=productId, pid=pid)
        str_options_list = ['82', '62', '66', '58', '236', '5530', '55', '78', '7642', '6931', '23', '5534', '224', '20', '1078', '2171', '3245']

        # "evaType":"2" 大质检； "priceType":"1" 销售定价
        param = {"_head":{"_interface":"evaluate","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"1525332832","_invokeId":"mikingzhang_adjustPrice","_callerServiceId":"116006","_groupNo":"1"},"_param":{"channelId":channelId, "pid":pid, "productId":productId, "evaType":"2","skuItem":str_sku_answer_list, "optItem":str_options_list, "ip":ip, "userId":"1002","priceType":"1", "freqLimitType":freqLimitType}}
        secret_key = "R2gFCRbILiNhwv3YbtaGceYJlPS5Ku02"
        callerserviceid = "116006"
        url = "http://bpeserver.huishoubao.com/base_price/evaluate"
        md5value = json.dumps(param) + "_" + secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典

        print('========>1.『{0}』 产品的『标准sku，ID』(随机取)为：\n'.format(productId), str_sku_answer_list)
        print('\n========>2. 以上『标准sku，名称』为：\n', '{' + str_Option_answer_desc[:-1] + '}')
        # print('\n========>3.『{0}』 产品的『大质检机况17，ID』(随机取)为：\n'.format(productId), str_options_list)
        # print('\n========>4. 以上『大质检机况17，名称』为：\n', '{' + str_options_list_desc[:-1] + '}')
        hsb_response_print(respone=respone)

if __name__ == '__main__':
    baseprice_23 = Base_Price_Evaluatee()
    '''【evaType：价格2.0质检类型，2-大质检】【标准SKU + 估价机况】一、销售价应用 - 自主运营'''
    # strSkuList = ['6116', '130', '18', '2236', '38', '1091', '1773']
    # strCheckList = ['82', '62', '66', '58', '236', '5530', '55', '78', '7642', '6931', '23', '5534', '224', '20', '1078', '2171', '3245']

    # 正常场景：渠道 - 命中：按类目+品牌+初始化价格范围调价 - 价格结果范围 - 按比例加成  |  正常
    baseprice_23.product_6_eva_option_get(channel_id='10000060', pid='1196', product_id='41567')
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', ip='127.0.0.1', freqLimitType='0')

    # 正常场景：渠道 - 命中：按类目+品牌+初始化价格范围调价 - 价格结果范围 - 按金额加成  |  正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # 正常场景：渠道 - 命中：按类目+品牌+初始化价格范围调价 - 初始化价格范围 - 按比例加成  |  拿 机型基准价 去匹配 初始化价格范围  |  正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # 正常场景：渠道 - 命中：按类目+品牌+初始化价格范围调价 - 初始化价格范围 - 按金额加成  |  拿 机型基准价 去匹配 初始化价格范围  |  正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # 正常场景：渠道 - 按类目+品牌+初始化价格范围调价 - 初始化价格范围 or 价格结果范围  范围段符合，但是  类目 or 品牌 不符合【未命中】  |  不走调价，正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # 正常场景：渠道 - 命中：按机型调价规则 - 按比例加成  |  正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # 正常场景：渠道 - 命中：按机型调价规则 - 按金额加成  |  正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # 正常场景：渠道 - 同时命中：按类目+品牌+初始化价格范围调价 以及 按机型调价规则   |  正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # 正常场景：渠道 - 没有命中任何规则  |  正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='1117', productId='41567', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # evaType：价格2.0 质检类型，1-57标准质检，2-大质检  |  暂不测试

'''
【外部接口】 【销售价应用方案估价接口】【第一版】【商家自检 - 价格查询 当下在用】

【补充：销售价应用方案 - 加成规则】
    priceType：价格类型，1-基准价，2-价格结果 ----------2021.5 专业版-价格查询新增

【BasePriceEvaluate】
【基础】
formParam: {ChannelId:40000001 Pid:0 ProductId:41567 EvaType:2 Select:[] Ip:127.0.0.1 UserId:1002 SkuItem:[6116 130 18 2236 38 1091 1773] OptItem:[82 62 66 58 236 5530 55 78 7642 6931 23 5534 224 20 1078 2171 3245] PriceType:1 FreqLimitType:0}
redigo: HGET BasePriceProduct 41567 &{ProductId:41567 ClassId:1 BrandId:2 Status:1 PriceState:1 PauState:1 RecycState:1 SyncPriceState:1 UserName:张金发_TEST CreateTime:2021-01-28 16:56:39 +0000 UTC UpdateTime:2021-05-19 15:03:55.246 +0000 UTC}
baseProductInfo: {ProductId:41567 ClassId:1 BrandId:2 Status:1 PriceState:1 PauState:1 RecycState:1 SyncPriceState:1 UserName:张金发_TEST CreateTime:2021-01-28 16:56:39 +0000 UTC UpdateTime:2021-05-19 15:03:55.246 +0000 UTC}
redigo: HGET ChannelAdjustPlan 40000001#0#1 &{Id:15 ChId:40000001 Pid:0 PlanId:51 ChType:1 PriceType:1 Status:1 CreateTime:2021-04-15 18:38:04.6 +0000 UTC UpdateTime:0001-01-01 00:00:00 +0000 UTC UserName:张金发_TEST}
redigo: HGET AdjustPlan 51 &{PlanId:51 PlanName:0522-销售-自主运营（金发测试验证，大家勿动） Remarks:0522-销售-自主运营（金发测试验证，大家勿动，谢谢） AdjustmentType:1 BasePlanId:0 State:1 CreateTime:2021-05-22 17:29:28.719 +0000 UTC UpdateTime:2021-06-05 15:27:28.41 +0000 UTC UserName:张金发_TEST PriceType:1 BeginTime:2021-05-20 17:25:54 +0000 UTC EndTime:2021-06-20 17:25:54 +0000 UTC PlanVersion:77 AutomaticVersion:1 VersionTime:0001-01-01 00:00:00 +0000 UTC ClassBranchPriceRule:[{ClassList:[2] BrandList:[2] PricePlusList:[{Begin:100 End:200000 Percent:151 Absolute:0 Type:1 PriceType:1}]} {ClassList:[1] BrandList:[1 2] PricePlusList:[{Begin:100 End:292500 Percent:149 Absolute:0 Type:1 PriceType:2}]}] ProductRule:[]}

【获取定价价格】
定价价格计算开始 ...
校验SKU选项 ...
机况-匹配价格等级模板开始 ...
optItem: [82 62 66 58 236 5530 55 78 7642 6931 23 5534 224 20 1078 2171 3245]
使用17项等级模板配置匹配等级
levelOrderMap: map[0:600 1:590 2:580 3:570 4:560 5:550 6:540 7:530 8:520 9:510 10:500 11:490 12:460 13:450 14:440 15:430 16:420 17:410 18:400 19:370 20:360 21:350 22:340 23:330 24:320 25:310 26:300 27:290 28:270 29:260 30:250 31:220 32:210 33:180 34:170 35:160 36:150 37:140 38:130 39:100 40:90 41:60 42:50 43:30 44:20]
matching!!!
match order: 0, itemComb: [20]
match level: 600
redigo: HGET BaseLevelInfo 600 &{Id:600 Name:S Status:1 ClassId:1}
机况-匹配价格等级模板结束 ...

匹配穷举价格 ...
按系数计算定价价格 ...
basePrice: 161600.000000
sku: 18 value: 0.000000 price: 161600.000000            剩余保修期不足一个月或过保
sku: 38 value: 53419.000000 price: 215019.000000        256GB
sku: 130 value: 0.000000 price: 215019.000000           全网通
sku: 1091 value: 1.000000 price: 215020.000000          深空灰色
sku: 1773 value: -3307.000000 price: 211713.000000      A1901
sku: 2236 value: 0.000000 price: 211713.000000          3GB
sku: 6116 value: -1928.000000 price: 209785.000000      国行BS机
level: 600 value: 1410 price: 295796.843750
base price: 295796.843750 -> 295700
价价格计算结束 ...

【走销售价应用方案逻辑】
加成价格计算开始 ...
AdjustPlanInfo: &{Price:118600 Level:20 ProductId:41567 ClassId:1 BrandId:2 BasePrice:161600 Skuitem:[18 36 42 471 2236 2242 8012] PriceAdjPlan:0xc0004e06c0 PriceAdjPlan2nd:<nil>}
【匹配销售价应用方案，调价规则】
Matching Product Rule
Matching Class Brand Price Rule
【命中调价规则】
ResultPriceType matching!!! Price: 118600.000000
    【命中1：按按类目+品牌+初始化价格范围调价 规则 - 按比例加成】
    rule value: {Begin:100 End:292500 Percent:149 Absolute:0 Type:1 PriceType:2}
    118600.000000 * ((149 / 1000) + 1) = 136271.406250
    Price: 136271.406250
    不进行2次加成计算
    加成价格计算结束 ...
    【命中2：按按类目+品牌+初始化价格范围调价 规则 - 按绝对值加成】
    
    【命中3：按机型调价 规则 - 按比例加成】
    【命中4：按机型调价 规则 - 按绝对值金额加成】
    
【生成定价估价记录】
Mgo Query: map[_id:eva_record_2105]
Mgo Change: {Update:map[$inc:map[sequence_value:1]] Replace:false Remove:false Upsert:false ReturnNew:false}
Mgo Result: {Sequence:89632}
EvaRecord: &{EvaluateId:89632 ProductId:41567 BasePrice:161600 SbuType:2 EvaType:3 VersionId:196 OptLevelId:600 Select:[12 471 18 2236 38 1091 2242 9016 9019 9027 9029 9037 9039 9052 9056 9057 9059 9062 9070 9072 9074 7559 9078 9079 9081 7575 9082 9086 9088 9090 9095 9099 9104 9106 9113 9117 7532] SkuItem:[12 18 38 471 1091 2236 2242] OptItem:[9016 9019 9027 9029 9037 9039 9052 9056 9057 9059 9062 9070 9072 9074 7559 9078 9079 9081 7575 9082 9086 9088 9090 9095 9099 9104 9106 9113 9117 7532] LevelTempId:15 Quatation:324900 ErrorCode:0 ErrorInfo:Success SpendTime:23 CreateTime:2021-05-23 20:56:00.819300037 +0000 UTC Interface:evaluate EvaBasePrice:292500 IP:127.0.0.1 UserId:1002 ChannelId:40000001 Pid:0 LevelStandId:0 SaleLevelId:0 BaseLevelTag:[] SaleLevelTag:[] AdjPlanId:51 AdjPlanVer:1 AdjustPrice:324900 AdjPlanId2nd:0 AdjPlanVer2nd:0 AdjustPrice2nd:0 OptLevelName:S SaleLevelName:}
'''