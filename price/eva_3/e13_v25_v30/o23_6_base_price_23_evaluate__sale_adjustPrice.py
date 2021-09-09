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
        # (strSkuList, strSkuDesc, strCheckList, strCheckDesc) = self.product_check_item_34(productId=productId)
        strSkuList = ['14', '130', '17', '2236', '38', '42', '2241']
        strCheckList = ['9015', '9019', '9027', '9028', '9035', '9039', '9047', '7481', '9057', '9059', '9062', '9067', '9071', '9074', '7559', '9077', '9079', '7570', '7574', '9082', '9084', '7589', '9090', '9094', '9098', '9102', '9106', '9111', '9117', '9120']

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

        # print('========>1.『{0}』 产品的『检测标准化选项-sku』(随机取)为：\n'.format(productId), strSkuList)
        # print('\n========>2. 以上『检测标准化选项-sku』为：\n', '{' + strSkuDesc[:-1] + '}')
        # print('\n========>3.『{0}』 产品的『检测标准化选项-机况-34』(随机取)为：\n'.format(productId), strCheckList)
        # print('\n========>4. 以上『检测标准化选项-机况-34』为：\n', '{' + strCheckDesc[:-1] + '}')
        hsb_response_print(respone=respone)

if __name__ == '__main__':
    baseprice_23 = Base_Price_Evaluatee()
    '''一、销售价应用 - 自主运营（销售调价，接口返回是没有 定价和销售等级标签概念的，没有用到等级标准）'''

    ''' 一次加成渠道 '''
    # 7. 34项标准质检模板：34项苹果定价模板v1（iPhoneX及以上）（ID 25）
    baseprice_23.base_price_evaluatee(channelId='10000837', pid='3413', productId='41567', ip='127.0.0.1', freqLimitType='0') #商家自检-卖家参考价 | iPhone X

    # 非 channelId='10000837', pid='3413' 渠道，也走到 3.0销售方案估价逻辑出4个，走默认 二次加成渠道 的对应返回字段逻辑
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='1001', productId='41567', ip='127.0.0.1', freqLimitType='0') #商家自检-卖家参考价 | iPhone X

'''
【外部接口】 【销售价应用方案估价接口】【第一版】【商家自检 - 价格查询 当下在用】

【补充：销售价应用方案 - 加成规则】
    priceType：价格类型，1-基准价，2-价格结果 ----------2021.5 专业版-价格查询新增
    
【BasePriceEvaluate】
{"_head": {"_interface": "evaluate", "_msgType": "request", "_remark": "", "_version": "0.01", "_timestamps": "1525332832", "_invokeId": "mikingzhang_adjustPrice", "_callerServiceId": "116006", "_groupNo": "1"}, "_param": {"channelId": "10000837", "pid": "3413", "productId": "41567", "evaType": "3", "skuItem": ["14", "130", "17", "2236", "38", "42", "2241"], "optItem": ["9015", "9019", "9027", "9028", "9035", "9039", "9047", "7481", "9057", "9059", "9062", "9067", "9071", "9074", "7559", "9077", "9079", "7570", "7574", "9082", "9084", "7589", "9090", "9094", "9098", "9102", "9106", "9111", "9117", "9120"], "ip": "127.0.0.1", "userId": "1002", "priceType": "1", "freqLimitType": "0"}}
20210827-105411-698|INFO|443346|a013befec8341fa8|8|10.0.30.113|BasePriceEvaluate|evaluate_api.go|eva_services_go/application/base-price-evaluate/router/api.Evaluate|29|formParam: {ChannelId:10000837 Pid:3413 ProductId:41567 EvaType:3 Select:[] Ip:127.0.0.1 UserId:1002 SkuItem:[14 130 17 2236 38 42 2241] OptItem:[9015 9019 9027 9028 9035 9039 9047 7481 9057 9059 9062 9067 9071 9074 7559 9077 9079 7570 7574 9082 9084 7589 9090 9094 9098 9102 9106 9111 9117 9120] PriceType:1 FreqLimitType:0}

【基础】
formParam: {ChannelId:10000837 Pid:3413 ProductId:41567 EvaType:3 Select:[] Ip:127.0.0.1 UserId:1002 SkuItem:[14 130 17 2236 38 42 2241] OptItem:[9015 9019 9027 9028 9035 9039 9047 7481 9057 9059 9062 9067 9071 9074 7559 9077 9079 7570 7574 9082 9084 7589 9090 9094 9098 9102 9106 9111 9117 9120] PriceType:1 FreqLimitType:0}

【v2.5】 到 【v3.0】
params: &{PlanId:9 ProductId:41567 EvaType:3 Select:[] SkuItem:[14 130 17 2236 38 42 2241] OptItem:[9015 9019 9027 9028 9035 9039 9047 7481 9057 9059 9062 9067 9071 9074 7559 9077 9079 7570 7574 9082 9084 7589 9090 9094 9098 9102 9106 9111 9117 9120] Ip:127.0.0.1 UserId:1002 FreqLimitType:0}
rrdisCmd: hget V3BasePriceProduct 41567: {"ProductId":41567,"ClassId":1,"BrandId":2,"Status":1,"PriceState":1,"PauState":1,"RecycState":1,"SyncPriceState":1,"UserName":"陈亮","CreateTime":"2021-01-28T16:56:39Z","UpdateTime":"2021-01-28T16:56:39Z"}
baseProductInfo: {ProductId:41567 ClassId:1 BrandId:2 OsType:0 Status:1 PriceState:1 PauState:1 RecycState:1 SyncPriceState:1 UserName:陈亮 CreateTime:2021-01-28 16:56:39 +0000 UTC UpdateTime:2021-01-28 16:56:39 +0000 UTC}
rrdisCmd: hget V3SaleApplyPlan 9: {"PlanId":9,"PlanName":"071202测试方案007","Remarks":"071202测试方案002","State":1,"DelFlag":0,"CreateTime":"2021-07-12T17:13:45.629Z","UpdateTime":"2021-07-12T17:13:45.629Z","UserName":"张金发_TEST","PlanVersion":1,"PlanInfo":{"SellerPrice":{"ClassBranchPriceRule":[{"ClassList":[1],"BrandList":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],"PricePlusList":[{"Begin":100,"End":30000,"Percent":-50,"Absolute":0,"Type":1,"PriceType":2},{"Begin":30100,"End":100000,"Percent":-20,"Absolute":0,"Type":1,"PriceType":2},{"Begin":100100,"End":200000,"Percent":-20,"Absolute":0,"Type":1,"PriceType":2},{"Begin":200100,"End":9999900,"Percent":-10,"Absolute":0,"Type":1,"PriceType":2}]}],"ProductRule":[]},"SellerMaxPrice":{"ClassBranchPriceRule":[{"ClassList":[1],"BrandList":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26],"PricePlusList":[{"Begin":100,"End":30000,"Percent":150,"Absolute":0,"Type":1,"PriceType":2},{"Begin":30100,"End":100000,"Percent":80,"Absolute":0,"Type":1,"PriceType":2},{"Begin":100100,"End":200000,"Percent":60,"Absolute":0,"Type":1,"PriceType":2},{"Begin":200100,"End":9999900,"Percent":40,"Absolute":0,"Type":1,"PriceType":2}]}],"ProductRule":[]},"BuyerPrice":{"ClassBranchPriceRule":[{"ClassList":[1],"BrandList":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],"PricePlusList":[{"Begin":100,"End":30000,"Percent":110,"Absolute":0,"Type":1,"PriceType":2},{"Begin":30100,"End":100000,"Percent":90,"Absolute":0,"Type":1,"PriceType":2},{"Begin":100100,"End":200000,"Percent":70,"Absolute":0,"Type":1,"PriceType":2},{"Begin":200100,"End":9999900,"Percent":50,"Absolute":0,"Type":1,"PriceType":2}]}],"ProductRule":[]}}}
rrdisCmd: hget V3BasePriceItemParams 41567: redis: nil
filter: map[Fproduct_id:41567]

【获取定价价格】
定价价格计算开始 ...
校验SKU选项 ...
    filter: map[Fcreate_time:map[$lte:2021-08-27 10:54:11.701992969 +0000 UTC] Flevel_temp_id:map[$ne:0] Fproduct_id:41567]
    result: {ProductId:41567 BasePrice:0 CombPriceInfo:[] LevelParamsInfo:[] LevelTempId:15 SkuParamsInfo:{Type:0 ItemAddSub:[]} UserName: VersionId:0 MaxPrice:{LevelId:0 Price:0 Sku:[]} MinPrice:{LevelId:0 Price:0 Sku:[]} BasePriceStaId:0 DetectStaId:0 LevelStaId:0 CreateTime:2021-08-27 10:53:49.589 +0000 UTC UpdateTime:0001-01-01 00:00:00 +0000 UTC SubmitTime:0001-01-01 00:00:00 +0000 UTC ReviewId:0 ReviewTime:0001-01-01 00:00:00 +0000 UTC}
    LevelTempId: 15
机况-匹配价格等级模板开始 ...
    optItem: [9015 9019 9027 9028 9035 9039 9047 7481 9057 9059 9062 9067 9071 9074 7559 9077 9079 7570 7574 9082 9084 7589 9090 9094 9098 9102 9106 9111 9117 9120]
    使用34项等级模板配置匹配等级
    matching!!!
    match order: 0, itemComb: [9027]
    match level: 600
    rrdisCmd: hget V3BaseLevel 600: {"Id":600,"Name":"S","Status":1,"ClassId":1}
机况-匹配价格等级模板结束 ...
匹配穷举价格 ...
【定价定价】按系数计算定价价格 ...
    basePrice: 178100.000000
    sku: 14 value: -10000.000000 price: 168100.000000
    sku: 17 value: 5500.000000 price: 173600.000000
    sku: 38 value: 38509.000000 price: 212109.000000
    sku: 42 value: 10000.000000 price: 222109.000000
    sku: 130 value: 0.000000 price: 222109.000000
    sku: 2236 value: 0.000000 price: 222109.000000
    sku: 2241 value: 0.000000 price: 222109.000000
    level: 600 value: 1598 price: 354930.187500
    Format Evaluate Price: 354930.187500
    base price: 354930.187500 -> 354900
定价价格计算结束 ...

【卖家参考价】【Price: 354900.000000 基于定价价格计算】加成价格计算开始 ...
    AdjustPlanInfo: &{Price:354900 Level:600 ProductId:41567 ClassId:1 BrandId:2 BasePrice:178100 Skuitem:[14 17 38 42 130 2236 2241] PriceAdjPlan:0xc000e5fd40 PriceAdjPlan2nd:<nil>}
    Matching Product Rule
    Matching Class Brand Price Rule
    ResultPriceType matching!!! Price: 354900.000000
    rule value: {Begin:200100 End:9999900 Percent:-10 Absolute:0 Type:1 PriceType:2}
    354900.000000 * ((-10 / 1000) + 1) = 351351.000000
    Price: 351351.000000
    Format Evaluate Price: 351351.000000
    不进行2次加成计算
加成价格计算结束 ...

【卖家最高价】【Price: 351300.000000 基于卖家参考价计算】加成价格计算开始 ...
    AdjustPlanInfo: &{Price:351300 Level:600 ProductId:41567 ClassId:1 BrandId:2 BasePrice:178100 Skuitem:[14 17 38 42 130 2236 2241] PriceAdjPlan:0xc000e5fe60 PriceAdjPlan2nd:<nil>}
    Matching Product Rule
    Matching Class Brand Price Rule
    ResultPriceType matching!!! Price: 351300.000000
    rule value: {Begin:200100 End:9999900 Percent:40 Absolute:0 Type:1 PriceType:2}
    351300.000000 * ((40 / 1000) + 1) = 365352.000000
    Price: 365352.000000
    Format Evaluate Price: 365352.000000
    不进行2次加成计算
加成价格计算结束 ...

【买家参考价】【Price: 351300.000000 基于卖家参考价计算】加成价格计算开始 ...
    AdjustPlanInfo: &{Price:351300 Level:600 ProductId:41567 ClassId:1 BrandId:2 BasePrice:178100 Skuitem:[14 17 38 42 130 2236 2241] PriceAdjPlan:0xc000d54000 PriceAdjPlan2nd:<nil>}
    Matching Product Rule
    Matching Class Brand Price Rule
    ResultPriceType matching!!! Price: 351300.000000
    rule value: {Begin:200100 End:9999900 Percent:50 Absolute:0 Type:1 PriceType:2}
    351300.000000 * ((50 / 1000) + 1) = 368864.968750
    Price: 368864.968750
    Format Evaluate Price: 368864.968750
    不进行2次加成计算
加成价格计算结束 ...
    
【生成定价估价记录】
Mgo Query: map[_id:eva_record_2108]
Mgo Change: {Update:map[$inc:map[sequence_value:1]] Replace:false Remove:false Upsert:true ReturnNew:true}
Mgo Result: {Sequence:998428}

【最终返回】
{"_head":{"_callerServiceId":"116006","_groupNo":"1","_interface":"evaluate","_invokeId":"mikingzhang_adjustPrice","_msgType":"response","_remark":"","_timestamps":"1630032851","_version":"0.01"},"_data":{"_errStr":"SUCCESS","_data":{"quotation":"368800","evaBasePrice":"354900","adjustPrice":"368800","adjustPrice2nd":"365300","recordId":"92108998428","levelId":"600","levelName":"S","saleLevelId":"0","saleLevelName":"","baseLevelTag":[],"saleLevelTag":[]},"_errCode":"0","_ret":"0"}}

"quotation":"368800",       ---卖家参考价
"evaBasePrice":"354900",    ---定价价格   
"adjustPrice":"368800",     ---卖家参考价
"adjustPrice2nd":"365300"   ---卖家最高价
'''