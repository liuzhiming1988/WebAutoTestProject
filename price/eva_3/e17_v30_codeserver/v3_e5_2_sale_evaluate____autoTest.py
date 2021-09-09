#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 估价服务 - 估价3.0 - 5.检测模板获取销售价  - http://wiki.huishoubao.com/web/#/138?page_id=15853
    入参：planId：方案id，111 …  |  productId：产品机型id	41567 …	是
        checkType：检测类型、检测场景，例如顺丰上门场景，或是闲鱼验机场景	1,2	是
        optItem：机况答案选项id  |  skuItem：标准sku答案选项id  |  userId：检测人
        ip：用户IP  |  freqLimitType：频率限制类型，0-不限制、1-IP、2-UserId	0 1 2 （外部对到用户端系统，建议增加限频；内部系统可以不限频）
    出参：evaBasePrice：销售定价价格 单位:分
        sellerPrice：卖家参考价 单位:分
        sellerMaxPrice：卖家最高价考价 单位:分
        buyerPrice：买家参考价 单位:分
        recordId：估价唯一id（id 会超过int(11)，请不要用int保存）（可通过：24 获取定价估价记录接口，获取信息）
        levelId：价格3.0-定价等级id  |  levelName：价格3.0-定价等级名称
        saleLevelId：价格3.0-销售等级id （价格2.0为空）  |  saleLevelName：价格3.0-销售等级名称 （价格2.0为空）
        baseLevelTag：价格3.0-定价等级标签
            baseLevelTag.tagId：定价等级标签id  |  baseLevelTag.tagName：定价等级标签名称
        saleLevelTag：价格3.0-销售等级标签
            saleLevelTag.tagId：销售等级标签id  |  saleLevelTag.tagName：销售等级标签名称
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

class V3_Sale_Evaluate:
    def v3_product_check_item(self, productId, checkType):
        param = {"_head": {"_interface": "product_check_item", "_msgType": "request", "_remark": "", "_version": "0.01","_timestamps": "1525332832", "_invokeId": "152533283241636", "_callerServiceId": "216002","_groupNo": "1"},"_param": {"productId": productId, "checkType": checkType, "userId": "1895","freqLimitType": "1", "ip": "127.0.0.1"}}
        secret_key = "rAfnRwyWfh2N9vXVgWwdpJxaXgOCd8af"
        callerserviceid = "216002"
        url = "http://codserver.huishoubao.com/detect_v3/product_check_item"
        md5value = json.dumps(param) + "_" + secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID": callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典
        checkList = respone_dict['_data']['_data']['checkList']
        skuList = respone_dict['_data']['_data']['skuList']

        strCheckList = []
        strCheckDesc = ''
        for info_question in checkList:
            questionList = info_question['questionList']
            for info_answer in questionList:
                answerList = info_answer['answerList']
                '''第一种方式：在answerList下随机取1个'''
                # index = random.randint(0, len(answerList) - 1)
                # strCheckList.append(answerList[index]['answerId'])
                # strCheckDesc += '"' + info_answer['questionName'] + ":" + answerList[index]['answerName'] + '",'

                '''第二种方式：在answerList下取answerWeight最大的那个'''
                index = sorted(answerList, key=lambda x: int(x['answerWeight']), reverse=True)[0]
                strCheckList.append(index['answerId'])
                strCheckDesc += '"' + info_answer['questionName'] + '":"' + index['answerName'] + '",'

        strSkuList = []
        strSkuDesc = ''
        for info in skuList:
            answerList = info['answerList']
            index = random.randint(0, len(answerList) - 1)
            strSkuList.append(answerList[index]['answerId'])
            strSkuDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'
        return strSkuList, strSkuDesc, strCheckList, strCheckDesc

    def v3_sale_evaluate(self, planId, productId, checkType):
        (strSkuList, strSkuDesc, strCheckList, strCheckDesc) = self.v3_product_check_item(productId=productId, checkType=checkType)

        param = {"_head":{"_interface":"sale_evaluate","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"1525332832","_invokeId":"152533283241636","_callerServiceId":"216002","_groupNo":"1"},"_param":{"planId":planId, "productId":productId, "checkType":checkType, "optItem":strCheckList, "skuItem":strSkuList, "userId":"1895", "freqLimitType": "1", "ip": "127.0.0.1"}}
        secret_key = "rAfnRwyWfh2N9vXVgWwdpJxaXgOCd8af"
        callerserviceid = "216002"
        url = "http://codserver.huishoubao.com/detect_v3/sale_evaluate"
        md5value = json.dumps(param) + "_" + secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())

        print('========>1.『{0}』 产品的『标准sku』(随机取)为：\n'.format(productId), strSkuList)
        print('\n========>2. 以上『标准sku』为：\n', '{' + strSkuDesc[:-1] + '}')
        print('\n========>3.『{0}』 产品的『检测模板选项-机况-价格3.0』(随机取)为：\n'.format(productId), strCheckList)
        print('\n========>4. 以上『检测模板选项-机况-价格3.0』为：\n', '{' + strCheckDesc[:-1] + '}')
        hsb_response_print(respone=respone)

if __name__ == '__main__':
    v3_e5 = V3_Sale_Evaluate()
    # v3_e5.v3_sale_evaluate(planId='10', productId='1008', checkType='2') #34项苹果安卓定价模板v1（iPhone3G-3GS或低端安卓）(ID:13)
    # v3_e5.v3_sale_evaluate(planId='10', productId='1132', checkType='2') #34项安卓定价模板v1（安卓简易无指纹）(ID:12)
    # v3_e5.v3_sale_evaluate(planId='10', productId='6027', checkType='2') #34项安卓定价模板v1（安卓简易有指纹）(ID:11)
    # v3_e5.v3_sale_evaluate(planId='10', productId='30780', checkType='2') #34项安卓定价模板v1（安卓无面容无指纹）(ID:10)
    # v3_e5.v3_sale_evaluate(planId='10', productId='58960', checkType='2') #34项安卓定价模板v1（安卓-面容）(ID:9)
    # v3_e5.v3_sale_evaluate(planId='10', productId='2063', checkType='2') #34项安卓定价模板v1（安卓指纹）(ID:8)
    # v3_e5.v3_sale_evaluate(planId='10', productId='59998', checkType='2') #34项安卓定价模板v1（安卓面容+指纹）(ID:7)
    # v3_e5.v3_sale_evaluate(planId='10', productId='30750', checkType='2') #34项苹果定价模板v1（iPhone4-5c）(ID:6)
    # v3_e5.v3_sale_evaluate(planId='10', productId='38201', checkType='2') #34项苹果定价模板v1（iPhone5s-8P及以上）(ID:5)
    # v3_e5.v3_sale_evaluate(planId='10', productId='41567', checkType='2')  # 34项苹果定价模板v1（iPhoneX及以上）(ID:4)
    v3_e5.v3_sale_evaluate(planId='11', productId='41567', checkType='1')


'''
【EvaluateCheckV3】 【前提：定价等级模板 要切换到 定价等级标准】
【价格3.0一期，B端寄卖切换会使用】

【入参】
{"_head": {"_interface": "sale_evaluate", "_msgType": "request", "_remark": "", "_version": "0.01", "_timestamps": "1525332832", "_invokeId": "152533283241636", "_callerServiceId": "216002", "_groupNo": "1"}, "_param": {"planId": "10", "productId": "41567", "checkType": "16", "optItem": ["8162", "8351", "8359", "8148", "8173", "8323", "8315", "8090", "8290", "8101"], "skuItem": ["12", "18", "38", "1091", "130", "2241", "2236"], "userId": "1895", "freqLimitType": "1", "ip": "127.0.0.1"}}
formParam: {PlanId:10 ProductId:41567 SkuItem:[12 18 38 1091 130 2241 2236] OptItem:[8162 8351 8359 8148 8173 8323 8315 8090 8290 8101] CheckType:16 UserId:1895 Ip:127.0.0.1 FreqLimitType:1}
rrdisCmd: hget V3EvaPrdCheckSubTemp t16-p41567: 48
redis checkSubTempId: 48

【根据 checkType='16'，得出关联的检测模板信息，同时得出配置了该机型的检测子模板信息】
rrdisCmd: hget V3EvaCheckSubTemplate 48: {"TemplateId":29,"SubTemplateId":48,"SubTemplateName":"29第一个子模板-按机型配置","Remarks":"29第一个子模板-按机型配置","SubTemplateVersion":2,"TemplateItem":[{"ItemType":8036,"Order":1,"ItemList":[{"Qid":8161,"Order":1,"Single":1,"Source":2,"Answer":[{"Aid":8164,"Order":1,"Single":1},{"Aid":8163,"Order":2,"Single":1},{"Aid":8162,"Order":3,"Single":1}]},{"Qid":8350,"Order":2,"Single":1,"Source":1,"Answer":[{"Aid":8355,"Order":1,"Single":1},{"Aid":8354,"Order":2,"Single":1},{"Aid":8353,"Order":3,"Single":1},{"Aid":8352,"Order":4,"Single":1},{"Aid":8351,"Order":5,"Single":1}]},{"Qid":8356,"Order":3,"Single":1,"Source":1,"Answer":[{"Aid":8359,"Order":1,"Single":1},{"Aid":8358,"Order":2,"Single":1},{"Aid":8357,"Order":3,"Single":1}]}]},{"ItemType":9581,"Order":2,"ItemList":[{"Qid":8147,"Order":1,"Single":1,"Source":2,"Answer":[{"Aid":8149,"Order":1,"Single":1},{"Aid":8148,"Order":2,"Single":1}]},{"Qid":8172,"Order":2,"Single":1,"Source":2,"Answer":[{"Aid":8177,"Order":1,"Single":1},{"Aid":8174,"Order":2,"Single":1},{"Aid":8175,"Order":3,"Single":1},{"Aid":8176,"Order":4,"Single":1},{"Aid":8173,"Order":5,"Single":1}]},{"Qid":8322,"Order":3,"Single":1,"Source":1,"Answer":[{"Aid":8324,"Order":1,"Single":1},{"Aid":8323,"Order":2,"Single":1}]}]},{"ItemType":9580,"Order":3,"ItemList":[{"Qid":8314,"Order":1,"Single":1,"Source":1,"Answer":[{"Aid":8317,"Order":1,"Single":1},{"Aid":8316,"Order":2,"Single":1},{"Aid":8315,"Order":3,"Single":1}]},{"Qid":8089,"Order":2,"Single":2,"Source":2,"Answer":[{"Aid":8095,"Order":1,"Single":2},{"Aid":8094,"Order":2,"Single":2},{"Aid":8093,"Order":3,"Single":2},{"Aid":8092,"Order":4,"Single":2},{"Aid":8091,"Order":5,"Single":2},{"Aid":8090,"Order":6,"Single":1}]},{"Qid":8289,"Order":3,"Single":2,"Source":2,"Answer":[{"Aid":8293,"Order":1,"Single":2},{"Aid":8294,"Order":2,"Single":2},{"Aid":8292,"Order":3,"Single":2},{"Aid":8291,"Order":4,"Single":2},{"Aid":8290,"Order":5,"Single":1}]},{"Qid":8100,"Order":4,"Single":1,"Source":2,"Answer":[{"Aid":8103,"Order":1,"Single":1},{"Aid":8102,"Order":2,"Single":1},{"Aid":8101,"Order":3,"Single":1}]}]}],"PriceStadId":16,"Status":1,"SpuType":2,"CreateTime":"2021-08-31T11:40:01.219Z","UpdateTime":"2021-08-31T11:40:14.066Z","UserName":"张金发_TEST"}

rrdisCmd: hget V3BasePriceStad 16: redis: nil
filter: map[Fid:map[$in:[16]] Fstatus:1]

SkuItem:[12 18 38 1091 130 2241 2236]
入参："optItem": ["8162", "8351", "8359", "8148", "8173", "8323", "8315", "8090", "8290", "8101"]
checkOpt（入参检测选项）:   [8162（质检） 8351（定价） 8359（定价） 8148（质检) 8173（质检） 8323（定价） 8315（定价） 8090（质检） 8290（质检） 8101（质检）]
baseStanOpt（定价标准选项）:[8371        8351       8359        8361       8378        8323       8315        8308]
rrdisCmd: get E_FL_TD_BPE_3: redis: nil

【根据 planId='10'，拿取销售价应用方案信息】
rrdisCmd: hget V3BasePriceProduct 41567: {"ProductId":41567,"ClassId":1,"BrandId":2,"OsType":1,"Status":1,"PriceState":1,"PauState":1,"RecycState":1,"SyncPriceState":1,"UserName":"陈亮","CreateTime":"2021-01-28T16:56:39Z","UpdateTime":"2021-01-28T16:56:39Z"}
baseProductInfo: {ProductId:41567 ClassId:1 BrandId:2 OsType:1 Status:1 PriceState:1 PauState:1 RecycState:1 SyncPriceState:1 UserName:陈亮 CreateTime:2021-01-28 16:56:39 +0000 UTC UpdateTime:2021-01-28 16:56:39 +0000 UTC}
rrdisCmd: hget V3SaleApplyPlan 10: redis: nil
Mgo query: map[Fid:map[$in:[10]]]
Mgo selector: map[]
Mgo result: [{PlanId:10 PlanName:071202测试方案008 Remarks: State:1 DelFlag:0 CreateTime:2021-07-12 17:13:50.872 +0000 UTC UpdateTime:2021-08-27 19:40:10.003 +0000 UTC UserName:张金发_TEST PlanVersion:3 PlanInfo:{SellerPrice:{ClassBranchPriceRule:[{ClassList:[1] BrandList:[1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28] PricePlusList:[{Begin:100 End:30000 Percent:-50 Absolute:0 Type:1 PriceType:2} {Begin:30100 End:100000 Percent:-20 Absolute:0 Type:1 PriceType:2} {Begin:100100 End:200000 Percent:-20 Absolute:0 Type:1 PriceType:2} {Begin:200100 End:9999900 Percent:-10 Absolute:0 Type:1 PriceType:2}]} {ClassList:[2] BrandList:[2] PricePlusList:[{Begin:100 End:999999900 Percent:110 Absolute:0 Type:1 PriceType:1}]} {ClassList:[3] BrandList:[2] PricePlusList:[{Begin:100 End:99999900 Percent:0 Absolute:900 Type:2 PriceType:2}]}] ProductRule:[{PrdId:41567 PrdAdjust:{Percent:110 Absolute:0 Type:1} SkuRule:[] CombRule:[]}]} SellerMaxPrice:{ClassBranchPriceRule:[{ClassList:[1] BrandList:[1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26] PricePlusList:[{Begin:100 End:30000 Percent:150 Absolute:0 Type:1 PriceType:2} {Begin:30100 End:100000 Percent:80 Absolute:0 Type:1 PriceType:2} {Begin:100100 End:200000 Percent:60 Absolute:0 Type:1 PriceType:2} {Begin:200100 End:9999900 Percent:40 Absolute:0 Type:1 PriceType:2}]}] ProductRule:[]} BuyerPrice:{ClassBranchPriceRule:[{ClassList:[1] BrandList:[1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28] PricePlusList:[{Begin:100 End:30000 Percent:110 Absolute:0 Type:1 PriceType:2} {Begin:30100 End:100000 Percent:90 Absolute:0 Type:1 PriceType:2} {Begin:100100 End:200000 Percent:70 Absolute:0 Type:1 PriceType:2} {Begin:200100 End:9999900 Percent:50 Absolute:0 Type:1 PriceType:2}]}] ProductRule:[]}}}]

【获取定价价格】
定价价格计算开始 ...
校验SKU选项 ...
机况-匹配价格等级标准开始 ...
    optItem: [8371 8351 8359 8361 8378 8323 8315 8308]
    rrdisCmd: hget V3BasePriceLevelStad 2: redis: nil
    filter: map[Fid:2]
    levelOrderMap: map[0:600 1:590 2:580 3:570 4:530 5:520 6:510 7:460 8:450 9:440 10:430 11:429 12:428 13:427 14:426 15:425 16:424 17:423 18:422 19:370 20:360 21:350 22:340 23:330 24:329 25:328 26:327 27:270 28:260 29:250 30:240 31:230 32:220 33:210 34:200 35:190 36:189 37:188 38:180 39:170 40:160 41:150 42:149 43:148 44:147 45:140 46:130 47:120 48:110 49:100 50:90 51:80 52:70 53:60 54:50 55:40 56:39 57:38]
    levelSaleMap: map[38:50 39:50 40:60 50:60 60:60 70:90 80:90 90:100 100:100 110:130 120:130 130:140 140:140 147:170 148:170 149:170 150:170 160:180 170:180 180:180 188:210 189:210 190:210 200:220 210:220 220:220 230:260 240:260 250:270 260:270 270:270 327:350 328:350 329:350 330:350 340:360 350:360 360:360 370:370 422:450 423:450 424:450 425:450 426:450 427:460 428:460 429:480 430:480 440:490 450:490 460:500 510:510 520:520 530:530 570:570 580:580 590:590 600:600]
    matching!!!
    match order: 0, itemComb: [8359]
    match level: 600, saleLevel: 600
    rrdisCmd: hget V3BaseLevel 600: {"Id":600,"Name":"S","Status":1,"ClassId":1}
    rrdisCmd: hget V3SaleLevel 600: redis: nil
    filter: map[Fid:map[$in:[600]]]
    rrdisCmd: hset V3SaleLevel 600 {"Id":600,"Name":"S","Desc":"","Status":1,"ClassId":1}: 1
    
    rrdisCmd: hmset V3LevelLabel 8 {"Id":8,"Name":"手机定价等级标签2","Status":1,"ClassId":1,"TypeId":1} 9 {"Id":9,"Name":"手机定价等级标签3","Status":1,"ClassId":1,"TypeId":1} 10 {"Id":10,"Name":"手机销售等级标签1","Status":1,"ClassId":1,"TypeId":2} 11 {"Id":11,"Name":"手机销售等级标签2","Status":1,"ClassId":1,"TypeId":2} 12 {"Id":12,"Name":"手机销售等级标签3","Status":1,"ClassId":1,"TypeId":2} 1 {"Id":1,"Name":"定价-测试标签","Status":0,"ClassId":3,"TypeId":1} 2 {"Id":2,"Name":"销售-测试标签","Status":0,"ClassId":3,"TypeId":2} 7 {"Id":7,"Name":"手机定价等级标签1","Status":1,"ClassId":1,"TypeId":1}: true
机况-匹配价格等级标准结束 ...

匹配穷举价格 ...
【定价定价】按系数计算定价价格 ...
    basePrice: 177900.000000
    sku: 12 value: 0.000000 price: 177900.000000        大陆国行
    sku: 18 value: 0.000000 price: 177900.000000        剩余保修期不足一个月或过保
    sku: 38 value: 38509.000000 price: 216409.000000    256GB
    sku: 130 value: 0.000000 price: 216409.000000       全网通
    sku: 1091 value: 0.000000 price: 216409.000000      深空灰色
    sku: 2236 value: 0.000000 price: 216409.000000      3GB
    sku: 2241 value: 0.000000 price: 216409.000000      A1865
    level: 600 value: 1598 price: 345821.593750
    Format Evaluate Price: 345821.593750
    base price: 345821.593750 -> 345800
定价价格计算结束 ...

【卖家参考价】【Price: 345800.000000 基于定价价格计算】加成价格计算开始 ...
    AdjustPlanInfo: &{Price:345800 Level:600 ProductId:41567 ClassId:1 BrandId:2 BasePrice:177900 Skuitem:[12 18 38 130 1091 2236 2241] PriceAdjPlan:0xc0002b7680 PriceAdjPlan2nd:<nil>}
    Matching Product Rule
    matching!!!
    product: 41567 value: {Percent:110 Absolute:0 Type:1}
    calculate product adjust
    345800.000000 * ((110 / 1000) + 1)
    Price: 383838.000000
    Format Evaluate Price: 383838.000000
    不进行2次加成计算
加成价格计算结束 ...

【卖家最高价】【Price: 383800.000000 基于卖家参考价计算】加成价格计算开始 ...
    AdjustPlanInfo: &{Price:383800 Level:600 ProductId:41567 ClassId:1 BrandId:2 BasePrice:177900 Skuitem:[12 18 38 130 1091 2236 2241] PriceAdjPlan:0xc0002b77a0 PriceAdjPlan2nd:<nil>}
    Matching Product Rule
    Matching Class Brand Price Rule
    ResultPriceType matching!!! Price: 383800.000000
    rule value: {Begin:200100 End:9999900 Percent:40 Absolute:0 Type:1 PriceType:2}
    383800.000000 * ((40 / 1000) + 1) = 399152.000000
    Price: 399152.000000
    Format Evaluate Price: 399152.000000
    不进行2次加成计算
加成价格计算结束 ...

【买家参考价】【Price: 383800.000000 基于卖家参考价计算】加成价格计算开始 ...
    AdjustPlanInfo: &{Price:383800 Level:600 ProductId:41567 ClassId:1 BrandId:2 BasePrice:177900 Skuitem:[12 18 38 130 1091 2236 2241] PriceAdjPlan:0xc0002b78c0 PriceAdjPlan2nd:<nil>}
    Matching Product Rule
    Matching Class Brand Price Rule
    ResultPriceType matching!!! Price: 383800.000000
    rule value: {Begin:200100 End:9999900 Percent:50 Absolute:0 Type:1 PriceType:2}
    383800.000000 * ((50 / 1000) + 1) = 402989.968750
    Price: 402989.968750
    Format Evaluate Price: 402989.968750
    不进行2次加成计算
加成价格计算结束 ...

【生成定价估价记录】
    Mgo Query: map[_id:eva_record_2108]
    Mgo Change: {Update:map[$inc:map[sequence_value:1]] Replace:false Remove:false Upsert:true ReturnNew:true}
    Mgo Result: {Sequence:1260553}

【最终返回】
    {"_head":{"_callerServiceId":"216002","_groupNo":"1","_interface":"sale_evaluate","_invokeId":"152533283241636","_msgType":"response","_remark":"","_timestamps":"1630392637","_version":"0.01"},"_data":{"_errStr":"SUCCESS","_data":{"evaBasePrice":"345800","sellerPrice":"383800","sellerMaxPrice":"399100","buyerPrice":"402900","recordId":"921081262041","levelId":"600","levelName":"S","saleLevelId":"600","saleLevelName":"S","saleLevelDesc":"","baseLevelTag":[{"tagId":"8","tagName":"手机定价等级标签2"},{"tagId":"7","tagName":"手机定价等级标签1"}],"saleLevelTag":[{"tagId":"11","tagName":"手机销售等级标签2"},{"tagId":"10","tagName":"手机销售等级标签1"}]},"_errCode":"0","_ret":"0"}}
'''