#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 定价系统+商品库系统+调价系统+估价系统 - 3.0用户估价接口 - http://wiki.huishoubao.com/web/#/347?page_id=15687
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

class V3_Evaluate:
    def __init__(self):
        self.secret_key_v3_eva_option_get = "R2gFCRbILiNhwv3YbtaGceYJlPS5Ku02"
        self.secret_key_v3_evaluate = "9aee61caf448b65fdf84c0e7d77c7348"
        self.callerserviceid = "816006"

    def v3_eva_option_get(self, channel_id, pid, product_id):
        param = {"_head": {"_interface": "eva_option_get", "_msgType": "request", "_remark": "eva_product_v3", "_version": "0.01", "_timestamps": "123", "_invokeId": "eva_product_v3", "_callerServiceId": "816006", "_groupNo": "1"},"_param": {"channel_id": channel_id, "product_id": product_id, "pid": pid}}
        url = "http://prdserver.huishoubao.com/eva_product_v3/eva_option_get"
        md5value = json.dumps(param) + "_" + self.secret_key_v3_eva_option_get
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value), "HSB-OPENAPI-CALLERSERVICEID":self.callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典
        # print(respone_dict)
        options_list = respone_dict['_body']['_data']['item_list']

        str_options_list = []
        str_options_desc = ''
        for info in options_list:
            answerList = info['question']
            index = random.randint(0, len(answerList) - 1)
            str_options_list.append(answerList[index]['id'])
            str_options_desc += '"' + info['name'] + '":"' + answerList[index]['name'] + '",'

        return str_options_list, str_options_desc

    def v3_evaluate(self, channel_id, pid, product_id):
        (str_options_list, str_options_desc) = self.v3_eva_option_get(channel_id=channel_id, pid=pid, product_id=product_id)
        param = {"_head":{"_interface":"evaluate","_msgType":"request","_remark":"zhangjinfa_autoTest","_version":"0.01","_timestamps":"123","_invokeId":"111","_callerServiceId":"816006","_groupNo":"1"},"_param":{"productid":product_id, "ip":"127.0.0.1", "cookies":"zhangjinfa_autoTest", "userid":"1895", "select":str_options_list, "pid":pid, "channel_id":channel_id}}
        url = "http://evaserver.huishoubao.com/evaluate_price_v3/evaluate"
        md5value = json.dumps(param) + "_" + self.secret_key_v3_evaluate
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":self.callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典

        print('========>1.『{0}』 产品的『估价选项-答案项ID』(随机取)为：\n'.format(product_id), str_options_list)
        print('\n========>2. 以上『估价选项-问题项名称：答案项名称』为：\n', '{' + str_options_desc[:-1] + '}')
        hsb_response_print(respone=respone)

if __name__ == '__main__':
    ''' 估价系统 与 定价系统 区分开理解，此处，不考虑机型的 定价状态'''
    v3_e133 = V3_Evaluate()
    '''1. 回收调价方案 | 自主调价 | 自动使用最新的回收定价版本 | 53'''
    # v3_e133.v3_evaluate(channel_id='40000001', pid='1001', product_id='41567')
    # v3_e133.v3_evaluate(channel_id='40000001', pid='1001', product_id='64000') #有聚合类SKU的机型
    # v3_e133.v3_evaluate(channel_id='40000001', pid='1001', product_id='3088') #没有编辑过SKU的机型
    # v3_e133.v3_evaluate(channel_id='40000001', pid='1001', product_id='30783') #没有编辑过SKU的机型

    '''2. 回收调价方案 | 自主调价 | 不自动使用最新的回收定价版本 | 54'''
    # v3_e133.v3_evaluate(channel_id='40000001', pid='1117', product_id='41567')
    # v3_e133.v3_evaluate(channel_id='40000001', pid='1117', product_id='64000') #有聚合类SKU的机型

    '''3. 回收调价方案 | 在其他调价方案基础上调价（自主调价 - 自动使用最新的回收定价版本 - 53） | 55'''
    # v3_e133.v3_evaluate(channel_id='40000001', pid='1575', product_id='41567')
    # v3_e133.v3_evaluate(channel_id='40000001', pid='1575', product_id='64000') #有聚合类SKU的机型

    '''4. 回收调价方案 | 在其他调价方案基础上调价（自主调价 - 不自动使用最新的回收定价版本 - 54 | 56'''
    # v3_e133.v3_evaluate(channel_id='40000001', pid='1603', product_id='41567')
    # v3_e133.v3_evaluate(channel_id='40000001', pid='1603', product_id='64000') #有聚合类SKU的机型

    '''5. 未关联回收调价方案（直接拿定价价格，算等级权重加成）'''
    # v3_e133.v3_evaluate(channel_id='40000001', pid='1647', product_id='41567')

    '''6. 渠道关联了（1次）回收调价方案，渠道是禁用的（直接拿定价价格，算等级权重加成）'''
    # v3_e133.v3_evaluate(channel_id='40000001', pid='1647', product_id='41567')

    '''7. 渠道关联了（1次）回收调价方案，调价方案是禁用的（直接拿定价价格，算等级权重加成）'''
    # v3_e133.v3_evaluate(channel_id='40000001', pid='1647', product_id='41567')

    '''8. 渠道关联了（1次）回收调价方案，未命中调价方案（直接拿定价价格，算等级权重加成）'''
    # v3_e133.v3_evaluate(channel_id='40000001', pid='1647', product_id='41567')

    '''9. 渠道关联了（2次）回收调价方案，命中2次方案（未命中规则），命中1次（命中规则）（用1次调价价格算权重加成）'''
    # v3_e133.v3_evaluate(channel_id='40000001', pid='1647', product_id='41567')

    '''10. 渠道关联了（2次）回收调价方案，未命中2次方案（方案未在有效期），命中1次（命中规则）（渠道调价方案有效期不匹配!，不走渠道调价加成）'''
    # v3_e133.v3_evaluate(channel_id='40000001', pid='1647', product_id='41567')

    '''11. 渠道关联了（2次）回收调价方案，未命中2次方案（方案禁用），命中1次（命中规则）（渠道调价方案状态无效!，不走渠道调价加成）'''
    # v3_e133.v3_evaluate(channel_id='40000001', pid='1647', product_id='41567')

    '''12. 渠道关联了（2次）回收调价方案，命中2次方案（命中规则），命中1次方案（未命中规则）（用2次调价价格算权重加成）'''
    # v3_e133.v3_evaluate(channel_id='40000001', pid='1647', product_id='41567')

    '''13. 渠道关联了（2次）回收调价方案，命中2次方案（命中规则），未命中1次方案（方案未在有效期 或 禁用）（渠道基础调价方案不在有效期内，用2次调价价格算权重加成）'''
    # v3_e133.v3_evaluate(channel_id='40000001', pid='1647', product_id='41567')

    # v3_e133.v3_evaluate(channel_id='40000001', pid='1647', product_id='64000') #有聚合类SKU的机型

    # v3_e133.v3_evaluate(channel_id='10000164', pid='1405', product_id='41567')
    # v3_e133.v3_evaluate(channel_id='10000165', pid='1406', product_id='41567')
    # v3_e133.v3_evaluate(channel_id='10000166', pid='1407', product_id='41567')
    v3_e133.v3_evaluate(channel_id='10000167', pid='1408', product_id='38200')
    # v3_e133.v3_evaluate(channel_id='10000168', pid='1409', product_id='41567')
'''
formParam: {ChannelId:40000001 Pid:1001 ProductId:41567 Select:[12 17 38 42 100049] Ip:127.0.0.1 UserId:测试 SkuItem:[] OptItem:[] Cookies:nihao FreqLimitType:}
rrdisCmd: hget V3EvaPriceProduct 41567: {"ProductId":41567,"ProductName":"iPhone X","BrandIdV1":11,"BrandId":2,"BrandName":"苹果","ClassId":1,"ClassName":"手机","KeyWord":"iPhoneX","OsType":1,"OsName":"ios系统","RecycleType":3,"PicId":"41567_20191106154719_960.jpg","PutawayTime":"2017-09-13","EvaStatus":1,"Status":1,"CreateTime":"2021-01-28T16:56:39Z","UpdateTime":"2021-07-22T19:15:37.558Z","UserName":"张金发_TEST"}
evaProductInfo: &{ProductId:41567 ProductName:iPhone X BrandIdV1:11 BrandId:2 BrandName:苹果 ClassId:1 ClassName:手机 KeyWord:iPhoneX OsType:1 OsName:ios系统 RecycleType:3 PicId:41567_20191106154719_960.jpg PutawayTime:2017-09-13 EvaStatus:1 Status:1 CreateTime:2021-01-28 16:56:39 +0000 UTC UpdateTime:2021-07-22 19:15:37.558 +0000 UTC UserName:张金发_TEST}
rrdisCmd: hget V3EvaSpuSku 41567: {"ProductId":41567,"ShowSku":[{"Qid":11,"Order":1,"QidMap":[11],"Answer":[{"Aid":12,"Order":1,"Default":0,"AidMap":[[12]]},{"Aid":13,"Order":2,"Default":0,"AidMap":[[13]]},{"Aid":14,"Order":3,"Default":0,"AidMap":[[14]]},{"Aid":15,"Order":4,"Default":0,"AidMap":[[15]]},{"Aid":1124,"Order":5,"Default":0,"AidMap":[[1124]]},{"Aid":6047,"Order":6,"Default":0,"AidMap":[[6047]]},{"Aid":6116,"Order":7,"Default":0,"AidMap":[[6116]]},{"Aid":7630,"Order":8,"Default":7630,"AidMap":[[7630],[8012]]}]},{"Qid":16,"Order":2,"QidMap":[16],"Answer":[{"Aid":17,"Order":1,"Default":0,"AidMap":[[17]]},{"Aid":18,"Order":2,"Default":0,"AidMap":[[18]]}]},{"Qid":32,"Order":3,"QidMap":[32],"Answer":[{"Aid":36,"Order":1,"Default":0,"AidMap":[[36]]},{"Aid":38,"Order":2,"Default":0,"AidMap":[[38]]}]},{"Qid":39,"Order":4,"QidMap":[39],"Answer":[{"Aid":42,"Order":1,"Default":0,"AidMap":[[42]]},{"Aid":1091,"Order":2,"Default":0,"AidMap":[[1091]]}]}],"HideSku":[{"Qid":122,"Default":130,"Aid":[130,471]},{"Qid":918,"Default":1083,"Aid":[1083,1773,2241,2242]},{"Qid":2232,"Default":2236,"Aid":[2236]}],"Version":32,"CreateTime":"2021-07-26T10:30:20.116Z","UpdateTime":"2021-07-31T16:58:36.645Z","UserName":"张金发_TEST"}
standSkuList:[130 1083 2236]
evaSkuToStandardSku:map[12:[12] 13:[13] 14:[14] 15:[15] 17:[17] 18:[18] 36:[36] 38:[38] 42:[42] 1091:[1091] 1124:[1124] 6047:[6047] 6116:[6116] 7630:[7630]]
standSkuList1: [130 1083 2236 12 17 38 42]
params.OptItem: [100049]
standSkuList2: [130 1083 2236 12 17 38 42]
rrdisCmd: hget V3EvaChannelTempMap c40000001-p1001: 65
rrdisCmd: hget V3EvaLevelWeight p41567-t65: {"Id":240,"ProductId":41567,"TemplateId":65,"SubTemplateId":91,"LevelWeight":[{"EveLevel":600,"Weight":[{"BaseLevel":600,"Value":1000}]},{"EveLevel":255,"Weight":[{"BaseLevel":590,"Value":1000}]},{"EveLevel":250,"Weight":[{"BaseLevel":580,"Value":1000}]},{"EveLevel":240,"Weight":[{"BaseLevel":570,"Value":500},{"BaseLevel":530,"Value":500}]},{"EveLevel":230,"Weight":[{"BaseLevel":520,"Value":330},{"BaseLevel":510,"Value":340},{"BaseLevel":460,"Value":330}]},{"EveLevel":228,"Weight":[{"BaseLevel":450,"Value":1000}]},{"EveLevel":220,"Weight":[{"BaseLevel":440,"Value":1000}]},{"EveLevel":210,"Weight":[{"BaseLevel":428,"Value":330},{"BaseLevel":430,"Value":330},{"BaseLevel":429,"Value":340}]},{"EveLevel":209,"Weight":[{"BaseLevel":427,"Value":550},{"BaseLevel":426,"Value":450}]},{"EveLevel":208,"Weight":[{"BaseLevel":425,"Value":500},{"BaseLevel":370,"Value":500}]},{"EveLevel":200,"Weight":[{"BaseLevel":424,"Value":450},{"BaseLevel":423,"Value":450},{"BaseLevel":422,"Value":100}]}],"WeightVersion":1,"MaxPrice":189500,"Status":1,"CreateTime":"2021-08-03T14:51:55.228Z","UpdateTime":"2021-08-03T15:28:00.024Z","UserName":"张金发_TEST"}
rrdisCmd: hget V3EvaLevelTemplate 54: redis: nil
Mgo filter: map[Fid:54]

机况-匹配价格等级模板开始 ...
    optItem: [100049]
    levelOrderMap: map[1:600 2:255 3:250 4:240 5:230 6:228 7:220 8:210 9:209 10:208 11:200]
    matching!!!
    match order: 1, itemComb: [100049]
    match level: 600
    rrdisCmd: hget V3EvaLevel 600: redis: nil
    Mgo filter: map[Fid:600]
    rrdisCmd: hset V3EvaLevel 600 {"Id":600,"Name":"S","Remarks":"S","ClassId":1,"Status":1,"CreateTime":"2021-07-06T14:40:18.228Z","UpdateTime":"2021-07-14T21:48:31.17Z","UserName":"张金发_TEST"}: 1
机况-匹配价格等级模板结束 ...

rrdisCmd: hget V3BasePriceProduct 41567: {"ProductId":41567,"ClassId":1,"BrandId":2,"Status":1,"PriceState":1,"PauState":1,"RecycState":1,"SyncPriceState":1,"UserName":"陈亮","CreateTime":"2021-01-28T16:56:39Z","UpdateTime":"2021-01-28T16:56:39Z"}
rrdisCmd: hget V3ChannelAdjustPlan 40000001#1001#2: redis: nil
Mgo query: map[Fchannel_id:40000001 Fpid:1001 Fprice_type:2 Fstatus:1]
Mgo count: 1
Mgo result: [{Id:7 ChId:40000001 Pid:1001 PlanId:53 ChType:2 PriceType:2 Status:1 CreateTime:2021-04-15 00:00:00 +0000 UTC UpdateTime:0001-01-01 00:00:00 +0000 UTC UserName:张金发_TEST}]

rrdisCmd: hget V3AdjustPlan 53: redis: nil
Mgo query: map[Fid:map[$in:[53]]]
Mgo selector: map[]
Mgo result: [{PlanId:53 PlanName:0525-回收-自主调价-自动使用（金发测试验证，大家勿动） Remarks:0525-回收-自主调价-自动使用（金发测试验证，大家勿动） AdjustmentType:1 BasePlanId:0 State:1 CreateTime:2021-05-25 16:33:28.921 +0000 UTC UpdateTime:2021-08-03 18:44:01.398 +0000 UTC UserName:张金发_TEST PriceType:2 BeginTime:2021-05-14 16:33:00 +0000 UTC EndTime:2021-06-14 16:33:00 +0000 UTC PlanVersion:77 AutomaticVersion:1 VersionTime:0001-01-01 00:00:00 +0000 UTC ClassBranchPriceRule:[{ClassList:[1 2] BrandList:[1 2] PricePlusList:[{Begin:100 End:999900 Percent:290 Absolute:0 Type:1 PriceType:1}]}] ProductRule:[]}]

定价价格计算开始 ...
    校验SKU选项 ...
    匹配穷举价格 ...
    按系数计算定价价格 ...
    select=['12', '17', '38', '42', '100049']
    basePrice: 211200.000000
    sku: 12 value: 440.000000 price: 211640.000000              大陆国行 (ID:12)
    sku: 17 value: 9710.000000 price: 221350.000000             剩余保修期大于一个月 (ID:17)
    sku: 38 value: 35410.000000 price: 256760.000000            256GB (ID:38)
    sku: 42 value: 100.000000 price: 256860.000000              银色 (ID:42)
    sku: 130 value: 100.000000 price: 256960.000000             全网通(ID:130)
    sku: 1083 value: 3279.000000 price: 260239.000000           其他型号(ID:1083)
    sku: 2236 value: 100.000000 price: 260339.000000            3GB(ID:2236)
    
    level: 600 value: 250 price: 65084.750000（260339 * 0.25）   估价等级ID：600（S） -- 定价等级：S
    
    【基准回收价】
    公式：（（1 - 等级预期毛利率） *  等级系数  * （ 初始化价格 + sku差值 ）/ 1.03* 1.01）
    也即：（（1 - 等级预期毛利率） *  回收定价 ）/ 1.03* 1.01）
    gmv: (1 - 210/1000.0) * 65084.750000 / 1.03 * 1.01
    gmv price: 50418.566406
    Format Evaluate Price: 50418.566406
    base price: 50418.566406 -> 50400
定价价格计算结束 ...

加成价格计算开始 ...
    AdjustPlanInfo: &{Price:50400 Level:600 ProductId:41567 ClassId:1 BrandId:2 BasePrice:211200 Skuitem:[12 17 38 42 130 1083 2236] PriceAdjPlan:0xc0004fcb40 PriceAdjPlan2nd:<nil>}
    Matching Product Rule
    Matching Class Brand Price Rule
    BasePriceType matching!!! BasePrice: 211200
    rule value: {Begin:100 End:999900 Percent:290 Absolute:0 Type:1 PriceType:1}
    50400.000000 * ((290 / 1000) + 1) = 65016.000000
    Price: 65016.000000
    不进行2次加成计算
加成价格计算结束 ...

Mgo Query: map[_id:eva_record_2108]
Mgo Change: {Update:map[$inc:map[sequence_value:1]] Replace:false Remove:false Upsert:true ReturnNew:true}
Mgo Result: {Sequence:31656}
EvaRecord: &{EvaluateId:31656 ProductId:41567 BasePrice:211200 CurBasePrice:211200 SbuType:2 EvaType:0 PriceType:2 VersionId:12 CurVersionId:12 OptLevelId:0 Select:[130 1083 2236 12 17 38 42] SkuItem:[12 17 38 42 130 1083 2236] OptItem:[] LevelList:[600] LevelTempId:0 Quotation:0 LevelListPrice:[{Level:600 Price:65000}] ErrorCode:0 ErrorInfo:Success SpendTime:5 CreateTime:2021-08-03 18:46:30.526527925 +0000 UTC Interface:Evaluate EvaBasePrice:0 IP:127.0.0.1 UserId:测试 ChannelId:40000001 Pid:1001 BasePriceStaId:4 LevelStandId:2 SaleLevelId:0 BaseLevelTag:[] SaleLevelTag:[] AdjPlanId:53 AdjPlanVer:78 AdjustPrice:65000 AdjPlanId2nd:0 AdjPlanVer2nd:0 AdjustPrice2nd:0 OptLevelName: SaleLevelName:}
Mgo insert: t_eva_record_2108, result: &{InsertedID:ObjectID("61091e86a479a35fd3493591")}

调价等级：[600]
调价价格：&{Quotation:0 LevelPriceList:[{Level:600 Price:65000}] EvaBasePrice:0 AdjustPrice:65000 AdjustPrice2nd:0 RecordId:9210831656 LevelId:0 LevelName: SaleLevelId:0 SaleLevelName: BaseLevelTag:[] SaleLevelTag:[]}

等级权重：map[600:1000]
估价等级600计算: (65000 * 1000/1000.0) = 65000.000000
Format Evaluate Price: 65000.000000

Mgo Query: map[_id:eva_record_2108]
Mgo Change: {Update:map[$inc:map[sequence_value:1]] Replace:false Remove:false Upsert:true ReturnNew:true}
Mgo Result: {Sequence:6}
EvaRecord: &{EvaluateId:6 ProductId:41567 EvaLevelTempId:54 EvaLevelTempVersion:2 EvaTempId:65 EvaSubTempId:91 EvaSubTempVersion:3 WeightVersion:1 SkuVersion:32 EvaSkuItem:[] BaseSkuItem:[12 17 38 42 130 1083 2236] BaseRecordId:9210831656 EvaOptionItem:[100049] EvaSelectItem:[12 17 38 42 100049] EvaLevelToBaseLevel:map[600:[600]] EvaLevelListPrice:[{Level:600 Price:65000}] ErrorCode:0 ErrorInfo:Success SpendTime:13 CreateTime:2021-08-03 18:46:30.527817476 +0000 UTC Interface:evaluate IP:127.0.0.1 UserId:测试 ChannelId:40000001 Pid:1001}
Mgo insert: t_eva_record_2108, result: &{InsertedID:ObjectID("61091e86a479a35fd3493592")}
'''