#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 定价系统+商品库系统+调价系统+估价系统 - 获取产品列表（可估价）  - http://wiki.huishoubao.com/web/#/347?page_id=15706
    入参：cookies：用户浏览器使用的cookies，如果没有，给随机字符串，方便问题查找
        ip：用户公网访问IP  |  pid：回收宝对外入口ID  |  channel_id：渠道ID，10000031
        productid：产品Id  |  userid：登录用户ID  |  select：用户选择的估价选项
    出参：quotation：估出的定价价格，单位分  |  evaluateid：估价记录id，(id 会超过int(11)，请不要用int保存）
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def v3_evaluate(productid, pid, channel_id, select):
    param = {"_head":{"_interface":"evaluate","_msgType":"request","_remark":"zhangjinfa_autoTest","_version":"0.01","_timestamps":"123","_invokeId":"111","_callerServiceId":"816006","_groupNo":"1"},"_param":{"productid":productid, "ip":"127.0.0.1", "cookies":"zhangjinfa_autoTest", "userid":"1895", "select":select, "pid":pid, "channel_id":channel_id}}
    secret_key = "9aee61caf448b65fdf84c0e7d77c7348"
    callerserviceid = "816006"
    url = "http://evaserver.huishoubao.com/evaluate_price_v3/evaluate"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    respone.encoding = respone.apparent_encoding  # 编码设置
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    ''' 估价系统 与 定价系统 区分开理解，此处，不考虑机型的 定价状态'''
    # 1、正常流程
    v3_evaluate(channel_id='40000001', pid='1001', productid='41567', select=['12', '17', '38', '42', '100071'])

'''
【EvaluatePrice】 【价格3.0】 【回收定价】

formParam: {ChannelId:40000001 Pid:1001 ProductId:41567 Select:[12 17 38 42 100071] Ip:127.0.0.1 UserId:测试 SkuItem:[] OptItem:[] Cookies:nihao FreqLimitType:}
rrdisCmd: hget V3EvaPriceProduct 41567: {"ProductId":41567,"ProductName":"iPhone X","BrandIdV1":11,"BrandId":2,"BrandName":"苹果","ClassId":1,"ClassName":"手机","KeyWord":"iPhoneX","OsType":1,"OsName":"ios系统","RecycleType":3,"PicId":"41567_20191106154719_960.jpg","PutawayTime":"2017-09-13","EvaStatus":1,"Status":1,"CreateTime":"2021-01-28T16:56:39Z","UpdateTime":"2021-07-22T19:15:37.558Z","UserName":"张金发_TEST"}
rrdisCmd: hget V3EvaSpuSku 41567: {"ProductId":41567,"ShowSku":[{"Qid":11,"Order":1,"QidMap":[11],"Answer":[{"Aid":12,"Order":1,"Default":0,"AidMap":[[12]]},{"Aid":13,"Order":2,"Default":0,"AidMap":[[13]]},{"Aid":14,"Order":3,"Default":0,"AidMap":[[14]]},{"Aid":15,"Order":4,"Default":0,"AidMap":[[15]]},{"Aid":1124,"Order":5,"Default":0,"AidMap":[[1124]]},{"Aid":6047,"Order":6,"Default":0,"AidMap":[[6047]]},{"Aid":6116,"Order":7,"Default":0,"AidMap":[[6116]]},{"Aid":7630,"Order":8,"Default":7630,"AidMap":[[7630],[8012]]}]},{"Qid":16,"Order":2,"QidMap":[16],"Answer":[{"Aid":17,"Order":1,"Default":0,"AidMap":[[17]]},{"Aid":18,"Order":2,"Default":0,"AidMap":[[18]]}]},{"Qid":32,"Order":3,"QidMap":[32],"Answer":[{"Aid":36,"Order":1,"Default":0,"AidMap":[[36]]},{"Aid":38,"Order":2,"Default":0,"AidMap":[[38]]}]},{"Qid":39,"Order":4,"QidMap":[39],"Answer":[{"Aid":42,"Order":1,"Default":0,"AidMap":[[42]]},{"Aid":1091,"Order":2,"Default":0,"AidMap":[[1091]]}]}],"HideSku":[{"Qid":122,"Default":130,"Aid":[130,471]},{"Qid":918,"Default":1083,"Aid":[1083,1773,2241,2242]},{"Qid":2232,"Default":2236,"Aid":[2236]}],"Version":32,"CreateTime":"2021-07-26T10:30:20.116Z","UpdateTime":"2021-07-31T16:58:36.645Z","UserName":"张金发_TEST"}
standSkuList:[130 1083 2236]
evaSkuToStandardSku:map[12:[12] 13:[13] 14:[14] 15:[15] 17:[17] 18:[18] 36:[36] 38:[38] 42:[42] 1091:[1091] 1124:[1124] 6047:[6047] 6116:[6116] 7630:[7630]]
standSkuList1: [130 1083 2236 12 17 38 42]
params.OptItem: [100071]
standSkuList2: [130 1083 2236 12 17 38 42]
rrdisCmd: hget V3EvaChannelTempMap c40000001-p1001: redis: nil
Mgo filter: map[Fstatus:1 Fuses_status:1]
Mgo filter: map[Fchannel_id:40000001 Fpid:1001 Fstatus:1 Ftemplate_id:map[$in:[31 42 60 65]]]
use channel template: 65
Mgo templateId: 65
rrdisCmd: hset V3EvaChannelTempMap c40000001-p1001 65: 1
rrdisCmd: hget V3EvaLevelWeight p41567-t65: {"Id":240,"ProductId":41567,"TemplateId":65,"SubTemplateId":91,"LevelWeight":[{"EveLevel":600,"Weight":[{"BaseLevel":600,"Value":1000}]},{"EveLevel":255,"Weight":[{"BaseLevel":590,"Value":1000}]},{"EveLevel":250,"Weight":[{"BaseLevel":580,"Value":1000}]},{"EveLevel":240,"Weight":[{"BaseLevel":570,"Value":500},{"BaseLevel":530,"Value":500}]},{"EveLevel":230,"Weight":[{"BaseLevel":520,"Value":330},{"BaseLevel":510,"Value":340},{"BaseLevel":460,"Value":330}]},{"EveLevel":228,"Weight":[{"BaseLevel":450,"Value":1000}]},{"EveLevel":220,"Weight":[{"BaseLevel":440,"Value":1000}]},{"EveLevel":210,"Weight":[{"BaseLevel":428,"Value":330},{"BaseLevel":430,"Value":330},{"BaseLevel":429,"Value":340}]},{"EveLevel":209,"Weight":[{"BaseLevel":427,"Value":550},{"BaseLevel":426,"Value":450}]},{"EveLevel":208,"Weight":[{"BaseLevel":425,"Value":500},{"BaseLevel":370,"Value":500}]},{"EveLevel":200,"Weight":[{"BaseLevel":424,"Value":450},{"BaseLevel":423,"Value":450},{"BaseLevel":422,"Value":100}]}],"WeightVersion":1,"MaxPrice":189500,"Status":1,"CreateTime":"2021-08-03T14:51:55.228Z","UpdateTime":"2021-08-03T15:28:00.024Z","UserName":"张金发_TEST"}

机况-匹配价格等级模板开始 ...
    optItem: [100071]
    levelOrderMap: map[1:600 2:255 3:250 4:240 5:230 6:228 7:220 8:210 9:209 10:208 11:200]
    matching!!!
    match order: 11, itemComb: [100071]
    match level: 200
    rrdisCmd: hget V3EvaLevel 200: redis: nil
    Mgo filter: map[Fid:200]
    rrdisCmd: hset V3EvaLevel 200 {"Id":200,"Name":"C1","Remarks":"C1","ClassId":1,"Status":1,"CreateTime":"2021-07-14T22:05:52.338Z","UpdateTime":"2021-07-14T22:05:52.338Z","UserName":"张金发_TEST"}: 1
机况-匹配价格等级模板结束 ...

baseProductInfo: {ProductId:41567 ClassId:1 BrandId:2 Status:1 PriceState:1 PauState:1 RecycState:1 SyncPriceState:1 UserName:陈亮 CreateTime:2021-01-28 16:56:39 +0000 UTC UpdateTime:2021-01-28 16:56:39 +0000 UTC}
rrdisCmd: hget V3ChannelAdjustPlan 40000001#1001#2: {"Id":7,"ChId":40000001,"Pid":1001,"PlanId":53,"ChType":2,"PriceType":2,"Status":1,"CreateTime":"2021-04-15T00:00:00Z","UpdateTime":"0001-01-01T00:00:00Z","UserName":"张金发_TEST"}
rrdisCmd: hget V3AdjustPlan 53: {"PlanId":53,"PlanName":"0525-回收-自主调价-自动使用（金发测试验证，大家勿动）","Remarks":"0525-回收-自主调价-自动使用（金发测试验证，大家勿动）","AdjustmentType":1,"BasePlanId":0,"State":1,"CreateTime":"2021-05-25T16:33:28.921Z","UpdateTime":"2021-08-03T18:46:23.342Z","UserName":"张金发_TEST","PriceType":2,"BeginTime":"2021-08-01T16:33:00Z","EndTime":"2021-08-31T16:33:00Z","PlanVersion":78,"AutomaticVersion":1,"VersionTime":"0001-01-01T00:00:00Z","ClassBranchPriceRule":[{"ClassList":[1,2],"BrandList":[1,2],"PricePlusList":[{"Begin":100,"End":999900,"Percent":290,"Absolute":0,"Type":1,"PriceType":1}]}],"ProductRule":[]}

定价价格计算开始 ...
    校验SKU选项 ...
    
    匹配穷举价格 ...
    按系数计算定价价格 ...
    basePrice: 211200.000000
    sku: 12 value: 440.000000 price: 211640.000000              大陆国行 (ID:12)
    sku: 17 value: 9710.000000 price: 221350.000000             剩余保修期大于一个月 (ID:17)
    sku: 38 value: 35410.000000 price: 256760.000000            256GB (ID:38)
    sku: 42 value: 100.000000 price: 256860.000000              银色 (ID:42)
    sku: 130 value: 100.000000 price: 256960.000000             全网通(ID:130)
    sku: 1083 value: 3279.000000 price: 260239.000000           其他型号(ID:1083)
    sku: 2236 value: 100.000000 price: 260339.000000            3GB(ID:2236)
    level: 424 value: 860 price: 223891.546875（260339 * 0.86）  估价等级ID：200（C1） -- (回收）定价等级：424（C10）  回收定价线上系数：86%  线上预期毛利率：21%
    【基准回收价】
    公式：（（1 - 等级预期毛利率） *  等级系数  * （ 初始化价格 + sku差值 ）/ 1.03 * 1.01）
    也即：（（1 - 等级预期毛利率） *  回收定价 ）/ 1.03 * 1.01）
    gmv: (1 - 210/1000.0) * 223891.546875 / 1.03 * 1.01
    gmv price: 173439.875000
    Format Evaluate Price: 173439.875000
    base price: 173439.875000 -> 173400
    
    匹配穷举价格 ...
    按系数计算定价价格 ...
    basePrice: 211200.000000
    sku: 12 value: 440.000000 price: 211640.000000              大陆国行 (ID:12)
    sku: 17 value: 9710.000000 price: 221350.000000             剩余保修期大于一个月 (ID:17)
    sku: 38 value: 35410.000000 price: 256760.000000            256GB (ID:38)
    sku: 42 value: 100.000000 price: 256860.000000              银色 (ID:42)
    sku: 130 value: 100.000000 price: 256960.000000             全网通(ID:130)
    sku: 1083 value: 3279.000000 price: 260239.000000           其他型号(ID:1083)
    sku: 2236 value: 100.000000 price: 260339.000000            3GB(ID:2236)
    level: 423 value: 850 price: 221288.156250（260339 * 0.85）  估价等级ID：200（C1） -- (回收）定价等级：423（C11）  回收定价线上系数：85%  线上预期毛利率：21%
    【基准回收价】
    公式：（（1 - 等级预期毛利率） *  等级系数  * （ 初始化价格 + sku差值 ）/ 1.03 * 1.01）
    也即：（（1 - 等级预期毛利率） *  回收定价 ）/ 1.03 * 1.01）
    gmv: (1 - 210/1000.0) * 221288.156250 / 1.03 * 1.01
    gmv price: 171423.125000
    Format Evaluate Price: 171423.125000
    base price: 171423.125000 -> 171400
    
    匹配穷举价格 ...
    按系数计算定价价格 ...
    basePrice: 211200.000000
    sku: 12 value: 440.000000 price: 211640.000000              大陆国行 (ID:12)
    sku: 17 value: 9710.000000 price: 221350.000000             剩余保修期大于一个月 (ID:17)
    sku: 38 value: 35410.000000 price: 256760.000000            256GB (ID:38)
    sku: 42 value: 100.000000 price: 256860.000000              银色 (ID:42)
    sku: 130 value: 100.000000 price: 256960.000000             全网通(ID:130)
    sku: 1083 value: 3279.000000 price: 260239.000000           其他型号(ID:1083)
    sku: 2236 value: 100.000000 price: 260339.000000            3GB(ID:2236)
    level: 422 value: 844 price: 219726.109375（260339 * 0.85）  估价等级ID：200（C1） -- (回收）定价等级：422（C12）  回收定价线上系数：84.4%  线上预期毛利率：21.1%
    【基准回收价】
    公式：（（1 - 等级预期毛利率） *  等级系数  * （ 初始化价格 + sku差值 ）/ 1.03 * 1.01）
    也即：（（1 - 等级预期毛利率） *  回收定价 ）/ 1.03 * 1.01）
    gmv: (1 - 211/1000.0) * 219726.109375 / 1.03 * 1.01
    gmv price: 169997.625000
    Format Evaluate Price: 169997.625000
    base price: 169997.625000 -> 169900
定价价格计算结束 ...

加成价格计算开始 ...
    AdjustPlanInfo: &{Price:173400 Level:424 ProductId:41567 ClassId:1 BrandId:2 BasePrice:211200 Skuitem:[12 17 38 42 130 1083 2236] PriceAdjPlan:0xc000138480 PriceAdjPlan2nd:<nil>}
    Matching Product Rule
    Matching Class Brand Price Rule
    BasePriceType matching!!! BasePrice: 211200
    rule value: {Begin:100 End:999900 Percent:290 Absolute:0 Type:1 PriceType:1}
    173400.000000 * ((290 / 1000) + 1) = 223686.000000
    Price: 223686.000000
    Format Evaluate Price: 223686.000000
    不进行2次加成计算
加成价格计算结束 ...

加成价格计算开始 ...
    AdjustPlanInfo: &{Price:171400 Level:423 ProductId:41567 ClassId:1 BrandId:2 BasePrice:211200 Skuitem:[12 17 38 42 130 1083 2236] PriceAdjPlan:0xc000138480 PriceAdjPlan2nd:<nil>}
    Matching Product Rule
    Matching Class Brand Price Rule
    BasePriceType matching!!! BasePrice: 211200
    rule value: {Begin:100 End:999900 Percent:290 Absolute:0 Type:1 PriceType:1}
    171400.000000 * ((290 / 1000) + 1) = 221106.000000
    Price: 221106.000000
    Format Evaluate Price: 221106.000000
    不进行2次加成计算
加成价格计算结束 ...

加成价格计算开始 ...
    AdjustPlanInfo: &{Price:169900 Level:422 ProductId:41567 ClassId:1 BrandId:2 BasePrice:211200 Skuitem:[12 17 38 42 130 1083 2236] PriceAdjPlan:0xc000138480 PriceAdjPlan2nd:<nil>}
    Matching Product Rule
    Matching Class Brand Price Rule
    BasePriceType matching!!! BasePrice: 211200
    rule value: {Begin:100 End:999900 Percent:290 Absolute:0 Type:1 PriceType:1}
    169900.000000 * ((290 / 1000) + 1) = 219171.000000
    Price: 219171.000000
    Format Evaluate Price: 219171.000000
    不进行2次加成计算
加成价格计算结束 ...

Mgo Query: map[_id:eva_record_2108]
Mgo Change: {Update:map[$inc:map[sequence_value:1]] Replace:false Remove:false Upsert:true ReturnNew:true}
Mgo Result: {Sequence:44868}
EvaRecord: &{EvaluateId:44868 ProductId:41567 BasePrice:211200 CurBasePrice:211200 SbuType:2 EvaType:0 PriceType:2 VersionId:12 CurVersionId:12 OptLevelId:0 Select:[130 1083 2236 12 17 38 42] SkuItem:[12 17 38 42 130 1083 2236] OptItem:[] LevelList:[424 423 422] LevelTempId:0 Quotation:0 LevelListPrice:[{Level:424 Price:223600} {Level:423 Price:221100} {Level:422 Price:219100}] ErrorCode:0 ErrorInfo:Success SpendTime:6 CreateTime:2021-08-04 14:14:51.55645713 +0000 UTC Interface:Evaluate EvaBasePrice:0 IP:127.0.0.1 UserId:测试 ChannelId:40000001 Pid:1001 BasePriceStaId:4 LevelStandId:2 SaleLevelId:0 BaseLevelTag:[] SaleLevelTag:[] AdjPlanId:53 AdjPlanVer:78 AdjustPrice:219100 AdjPlanId2nd:0 AdjPlanVer2nd:0 AdjustPrice2nd:0 OptLevelName: SaleLevelName:}
Mgo insert: t_eva_record_2108, result: &{InsertedID:ObjectID("610a305ba479a35fd3493593")}

调价等级：[424 423 422]
调价价格：&{Quotation:0 LevelPriceList:[{Level:424 Price:223600} {Level:423 Price:221100} {Level:422 Price:219100}] EvaBasePrice:0 AdjustPrice:219100 AdjustPrice2nd:0 RecordId:9210844868 LevelId:0 LevelName: SaleLevelId:0 SaleLevelName: BaseLevelTag:[] SaleLevelTag:[]}
等级权重：map[422:100 423:450 424:450]
估价等级200计算: (223600 * 450/1000.0) + (221100 * 450/1000.0) + (219100 * 100/1000.0) = 222025.000000
Format Evaluate Price: 222025.000000

Mgo Query: map[_id:eva_record_2108]
Mgo Change: {Update:map[$inc:map[sequence_value:1]] Replace:false Remove:false Upsert:true ReturnNew:true}
Mgo Result: {Sequence:7}
EvaRecord: &{EvaluateId:7 ProductId:41567 EvaLevelTempId:54 EvaLevelTempVersion:2 EvaTempId:65 EvaSubTempId:91 EvaSubTempVersion:3 WeightVersion:1 SkuVersion:32 EvaSkuItem:[] BaseSkuItem:[12 17 38 42 130 1083 2236] BaseRecordId:9210844868 EvaOptionItem:[100071] EvaSelectItem:[12 17 38 42 100071] EvaLevelToBaseLevel:map[200:[424 423 422]] EvaLevelListPrice:[{Level:200 Price:222000}] ErrorCode:0 ErrorInfo:Success SpendTime:20 CreateTime:2021-08-04 14:14:51.557820084 +0000 UTC Interface:evaluate IP:127.0.0.1 UserId:测试 ChannelId:40000001 Pid:1001}
Mgo insert: t_eva_record_2108, result: &{InsertedID:ObjectID("610a305ba479a35fd3493594")}
'''