#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 估价服务 - 26 销售价应用方案估价接口 -  http://wiki.huishoubao.com/web/#/138?page_id=15625
    入参：planId：销售应用方案id，1、2、3 …	是
        productId：产品机型id	41567 …	是
        evaType：价格2.0 质检类型，1-57标准质检，2-大质检，3-34标准质检，0-价格3.0，0 1 2 3	是
        skuItem：sku答案选项id，“12”等，否，无sku机型可以不穿或者传空数组
        optItem：机况答案选项id，“7422”等，是
        ip：用户IP，127.0.0.1 … 是  |  userId：用户ID，123456 …	是
        priceType：价格类型，1-销售定价，2-回收定价，1，2	是
        freqLimitType：频率限制类型，0-不限制，1-IP，2-UserId	0 1 2 （外部对到用户端系统，建议增加限频；内部系统可以不限频），是
    出参：evaBasePrice：销售定价价格，单位:分  |  sellerPrice：卖家参考价，单位:分
        sellerMaxPrice：卖家最高价考价，单位:分  |  buyerPrice：买家参考价，单位:分
        recordId：估价唯一id（id 会超过int(11)，请不要用int保存）（可通过：24 获取定价估价记录接口，获取信息）
        levelId：价格3.0-定价等级id  |  levelName：价格3.0-定价等级名称
        saleLevelId：价格3.0-销售等级id （价格2.0为空）  |  saleLevelName：价格3.0-销售等级名称 （价格2.0为空）
        baseLevelTag：价格3.0-定价等级标签
            baseLevelTag.tagId：定价等级标签id  |  baseLevelTag.tagName：定价等级标签名称
        saleLevelTag：价格3.0-销售等级标签
            saleLevelTag.tagId：销售等级标签id  |  saleLevelTag.tagName：销售等级标签名称

    错误码：900 未知错误  |  901 参数错误  |  902 获取数据失败  |  903 下架状态  |  904 产品配置数据错误
        905 等级匹配失败  |  906 生成估价记录失败  |  907 未定价状态机型  |  999 频率限制

    场景逻辑：
        1、按比例加成  定价价格 * (( 按比例加成值 / 1000 ) + 1)
        2、按金额加成  定价价格 + 按金额加成值
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test, hsb_response_print

class Sale_Apply_Price:
    def pdt_sku_query(self, productId):
        param = {"_head": {"_interface": "pdt_sku_query", "_msgType": "request", "_remark": "", "_version": "0.01","_timestamps": "123", "_invokeId": "111", "_callerServiceId": "112002", "_groupNo": "1"},"_param": {"subInterface": "sku_option_combination_get", "info": {"productId": productId}}}
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

    def sale_apply_price(self, planId, productId, evaType, ip, freqLimitType):
        # (str_sku_answer_list, str_Option_answer_desc) = self.pdt_sku_query(productId=productId)
        # (str_options_list, str_options_list_desc) = self.product_6_eva_option_get(channel_id=channelId, product_id=productId, pid=pid)

        '''1. iPhone X'''
        str_sku_answer_list = ['13', '471', '18', '2236', '38', '42', '2241']
        str_options_list = ['82', '62', '66', '58', '236', '5530', '55', '78', '7642', '6931', '23', '5534', '224','20', '1078', '2171', '3245']

        param = {"_head":{"_interface":"sale_apply_price","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"1525332832","_invokeId":"mikingzhang_adjustPrice","_callerServiceId":"116006","_groupNo":"1"},"_param":{"planId":planId, "productId":productId,"evaType":evaType, "skuItem":str_sku_answer_list, "optItem":str_options_list, "ip":ip, "userId":"1895", "freqLimitType":freqLimitType}}
        secret_key = "R2gFCRbILiNhwv3YbtaGceYJlPS5Ku02"
        callerserviceid = "116006"
        url = "http://bpeserver.huishoubao.com/adjustment_price/sale_apply_price"
        md5value = json.dumps(param) + "_" + secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())

        # print('========>1.『{0}』 产品的『标准sku，ID』(随机取)为：\n'.format(productId), str_sku_answer_list)
        # print('\n========>2. 以上『标准sku，名称』为：\n', '{' + str_Option_answer_desc[:-1] + '}')
        # print('\n========>3.『{0}』 产品的『大质检机况17，ID』(随机取)为：\n'.format(productId), str_options_list)
        # print('\n========>4. 以上『大质检机况17，名称』为：\n', '{' + str_options_list_desc[:-1] + '}')
        hsb_response_print(respone=respone)

if __name__ == '__main__':
    bpeserver_26 = Sale_Apply_Price()
    ''' 1. evaType：质检类型，1-57标准质检，2-大质检，3-34标准质检，0-价格3.0
    2. 卖家参考价：“卖家参考价”在“销售定价”基础上加成，如卖家参考价未配置或未命中加成规则，则不向业务侧输出卖家参考价
    3. 卖家最高价：“卖家最高价”在“卖家参考价”基础上加成，如卖家参考价/卖家最高价未配置或未命中加成规则，或则不向业务侧输出卖家最高价
    4. 买家参考价：“买家参考价”在“卖家参考价”基础上加成，如卖家参考价/买家参考价未配置或未命中加成规则，或则不向业务侧输出买家参考价
    5. 卖家参考价 无加成规则、or机型未命中，则卖家最高价、买家参考价价格都一律返回为0
    6. 卖家参考价 有加成规则，且机型命中，但价格为0（按机型加成 - 按比例加成 -101%），则卖家最高价、买家参考价价格都一律返回为0
    '''

    # 1. 正常场景
    bpeserver_26.sale_apply_price(planId='14', productId='41567', evaType='2', ip='127.0.0.1', freqLimitType='0')

    # 2. 3个价格加成规则均为空
    # "evaBasePrice":"19000","sellerPrice":"0","sellerMaxPrice":"0","buyerPrice":"0"  |  销售参考价，无加成规则，价格为0， | 正常
    # bpeserver_26.sale_apply_price(planId='16', productId='41567', evaType='2', ip='127.0.0.1', freqLimitType='0')

    # 3. 卖家参考价 规则为空，卖家最高价/买家参考价 规则不为空 | "evaBasePrice":"19000","sellerPrice":"0","sellerMaxPrice":"0","buyerPrice":"0" | 正常
    # bpeserver_26.sale_apply_price(planId='17', productId='41567', evaType='2', ip='127.0.0.1', freqLimitType='0')

    # 4. 卖家参考价/卖家最高价 规则为空，买家参考价 规则不为空 | "evaBasePrice":"19000","sellerPrice":"0","sellerMaxPrice":"0","buyerPrice":"0" | 正常
    # bpeserver_26.sale_apply_price(planId='18', productId='41567', evaType='2', ip='127.0.0.1', freqLimitType='0')

    # 5. 卖家最高价 规则为空，卖家参考价/买家参考价 规则不为空 | "evaBasePrice":"19000","sellerPrice":"22000","sellerMaxPrice":"0","buyerPrice":"26500" | 正常
    # bpeserver_26.sale_apply_price(planId='19', productId='41567', evaType='2', ip='127.0.0.1', freqLimitType='0')

    # 6. 买家参考价 规则为空，卖家参考价/卖家最高价 规则不为空 | "evaBasePrice":"19000","sellerPrice":"22100","sellerMaxPrice":"27100","buyerPrice":"0" | 正常
    # bpeserver_26.sale_apply_price(planId='20', productId='41567', evaType='2', ip='127.0.0.1', freqLimitType='0')

    # 7. 卖家参考价/买家参考价 规则为空，卖家最高价 规则不为空 | "evaBasePrice":"19000","sellerPrice":"0","sellerMaxPrice":"0","buyerPrice":"0" | 正常
    # bpeserver_26.sale_apply_price(planId='21', productId='41567', evaType='2', ip='127.0.0.1', freqLimitType='0')

    # 8. 卖家最高价/买家参考价 规则为空，卖家参考价 规则不为空 | "evaBasePrice":"73100","sellerPrice":"88400","sellerMaxPrice":"0","buyerPrice":"0" | 正常
    # bpeserver_26.sale_apply_price(planId='22', productId='41567', evaType='2', ip='127.0.0.1', freqLimitType='0')

    # 9. 3个选择的价格范围都是：初始化价格范围 | 初始化价格未命中 | "evaBasePrice":"19000","sellerPrice":"0","sellerMaxPrice":"0","buyerPrice":"0" | 正常
    # bpeserver_26.sale_apply_price(planId='23', productId='41567', evaType='2', ip='127.0.0.1', freqLimitType='0')

    # 10. 3个选择的价格范围都是：初始化价格范围 | 初始化价格命中 | 举例：按初始化价格范围 加成，是加成的条件规则，比如，初始化价格范围500-1000时，加成2%（在销售定价基础上加2%）
    # "evaBasePrice":"19000","sellerPrice":"21600","sellerMaxPrice":"24800","buyerPrice":"25700" | 正常
    # bpeserver_26.sale_apply_price(planId='27', productId='41567', evaType='2', ip='127.0.0.1', freqLimitType='0')

    # 11. 同时命中 按类目+品牌+初始化价格范围调价 + 按机型调价 | "evaBasePrice":"19000","sellerPrice":"20100","sellerMaxPrice":"21500","buyerPrice":"21600" | 正常
    # bpeserver_26.sale_apply_price(planId='28', productId='41567', evaType='2', ip='127.0.0.1', freqLimitType='0')

    # 12. 命中 按机型调价（按比例加成 -101%） |
    # "evaBasePrice":"73100","sellerPrice":"0","sellerMaxPrice":"0","buyerPrice":"0" | 正常
    # "evaBasePrice":"73100","sellerPrice":"81100","sellerMaxPrice":"0","buyerPrice":"0" | 正常
    # "evaBasePrice":"19000","sellerPrice":"21000","sellerMaxPrice":"23700","buyerPrice":"0" | 正常
    # bpeserver_26.sale_apply_price(planId='29', productId='41567', evaType='2', ip='127.0.0.1', freqLimitType='0')

    # 13. 34项，10套模板
    # bpeserver_26.sale_apply_price(planId='24', productId='4001', evaType='2', ip='127.0.0.1', freqLimitType='0') #模板ID：34 | 无SKU机型 | 华为 A199
    # bpeserver_26.sale_apply_price(planId='24', productId='4301', evaType='2', ip='127.0.0.1', freqLimitType='0') #模板ID：33 | 无SKU机型 | 华为 C8818
    # bpeserver_26.sale_apply_price(planId='24', productId='4310', evaType='2', ip='127.0.0.1', freqLimitType='0') #模板ID：32 | 华为 畅享6s
    # bpeserver_26.sale_apply_price(planId='24', productId='10392', evaType='2', ip='127.0.0.1', freqLimitType='0') #模板ID：31 | 三星 Galaxy Folder
    # bpeserver_26.sale_apply_price(planId='24', productId='2071', evaType='2', ip='127.0.0.1', freqLimitType='0') #模板ID：30 | 品牌机型未命中调价规则 | OPPO A57
    # bpeserver_26.sale_apply_price(planId='24', productId='3006', evaType='2', ip='127.0.0.1', freqLimitType='0') #模板ID：29 | 品牌机型未命中调价规则 | vivo S7t
    # bpeserver_26.sale_apply_price(planId='24', productId='3', evaType='2', ip='127.0.0.1', freqLimitType='0') #模板ID：28 | iPhone 4
    # bpeserver_26.sale_apply_price(planId='24', productId='30749', evaType='2', ip='127.0.0.1', freqLimitType='0') #模板ID：27 | iPhone 5s
    # bpeserver_26.sale_apply_price(planId='24', productId='30747', evaType='2', ip='127.0.0.1', freqLimitType='0') #模板ID：26 | iPhone 6 Plus
    # bpeserver_26.sale_apply_price(planId='24', productId='64494', evaType='2', ip='127.0.0.1', freqLimitType='0') #模板ID：25 | iPhone 12
    # bpeserver_26.sale_apply_price(planId='24', productId='63330', evaType='2', ip='127.0.0.1', freqLimitType='0') #模板ID：25 | iPhone 11
    # bpeserver_26.sale_apply_price(planId='24', productId='54791', evaType='2', ip='127.0.0.1', freqLimitType='0') #模板ID：25 | iPhone XR
    # bpeserver_26.sale_apply_price(planId='24', productId='54790', evaType='2', ip='127.0.0.1', freqLimitType='0') #模板ID：25 | iPhone XS
    # bpeserver_26.sale_apply_price(planId='24', productId='54789', evaType='2', ip='127.0.0.1', freqLimitType='0') #模板ID：25 | iPhone XS Max

''' 
【外部接口】 【销售价应用方案估价接口】【第二版】【调用方传planId，返回4个价格方案】【暂未使用】

【BasePriceEvaluate】
【基础】
formParam: {PlanId:14 ProductId:41567 EvaType:2 Select:[] SkuItem:[13 471 18 2236 38 42 2241] OptItem:[82 62 66 58 236 5530 55 78 7642 6931 23 5534 224 20 1078 2171 3245] Ip:127.0.0.1 UserId:1895 FreqLimitType:0}
redigo: HGET BasePriceProduct 41567 &{ProductId:41567 ClassId:1 BrandId:2 Status:1 PriceState:1 PauState:1 RecycState:1 SyncPriceState:1 UserName:陈亮 CreateTime:2021-01-28 16:56:39 +0000 UTC UpdateTime:2021-06-17 17:11:12.635 +0000 UTC}
baseProductInfo: {ProductId:41567 ClassId:1 BrandId:2 Status:1 PriceState:1 PauState:1 RecycState:1 SyncPriceState:1 UserName:陈亮 CreateTime:2021-01-28 16:56:39 +0000 UTC UpdateTime:2021-06-17 17:11:12.635 +0000 UTC}
redigo: HGET SaleApplyPlan 14 &{PlanId:14 PlanName:071202测试方案012 Remarks: State:1 DelFlag:0 CreateTime:2021-07-12 17:15:33.109 +0000 UTC UpdateTime:2021-07-12 17:15:33.109 +0000 UTC UserName:张金发_TEST PlanVersion:1 PlanInfo:{SellerPrice:{ClassBranchPriceRule:[{ClassList:[1] BrandList:[1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28] PricePlusList:[{Begin:100 End:30000 Percent:-50 Absolute:0 Type:1 PriceType:2} {Begin:30100 End:100000 Percent:-20 Absolute:0 Type:1 PriceType:2} {Begin:100100 End:200000 Percent:-20 Absolute:0 Type:1 PriceType:2} {Begin:200100 End:9999900 Percent:-10 Absolute:0 Type:1 PriceType:2}]}] ProductRule:[]} SellerMaxPrice:{ClassBranchPriceRule:[{ClassList:[1] BrandList:[1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26] PricePlusList:[{Begin:100 End:30000 Percent:150 Absolute:0 Type:1 PriceType:2} {Begin:30100 End:100000 Percent:80 Absolute:0 Type:1 PriceType:2} {Begin:100100 End:200000 Percent:60 Absolute:0 Type:1 PriceType:2} {Begin:200100 End:9999900 Percent:40 Absolute:0 Type:1 PriceType:2}]}] ProductRule:[]} BuyerPrice:{ClassBranchPriceRule:[{ClassList:[1] BrandList:[1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28] PricePlusList:[{Begin:100 End:30000 Percent:110 Absolute:0 Type:1 PriceType:2} {Begin:30100 End:100000 Percent:90 Absolute:0 Type:1 PriceType:2} {Begin:100100 End:200000 Percent:70 Absolute:0 Type:1 PriceType:2} {Begin:200100 End:9999900 Percent:50 Absolute:0 Type:1 PriceType:2}]}] ProductRule:[]}}}

【获取定价价格】
定价价格计算开始 ...
校验SKU选项 ...
机况-匹配价格等级模板开始 ...
optItem: [82 62 66 58 236 5530 55 78 7642 6931 23 5534 224 20 1078 2171 3245]
使用17项等级模板配置匹配等级
levelOrderMap: map[0:600 1:590 2:580 3:570 4:569 5:560 6:550 7:540 8:530 9:520 10:510 11:509 12:508 13:507 14:506 15:505 16:500 17:490 18:460 19:450 20:440 21:430 22:429 23:428 24:427 25:426 26:425 27:424 28:423 29:422 30:420 31:419 32:418 33:417 34:416 35:415 36:414 37:413 38:412 39:411 40:410 41:409 42:408 43:400 44:370 45:360 46:350 47:340 48:330 49:329 50:328 51:327 52:326 53:325 54:324 55:320 56:310 57:300 58:290 59:270 60:260 61:250 62:240 63:230 64:229 65:228 66:227 67:220 68:210 69:200 70:190 71:189 72:188 73:187 74:186 75:185 76:184 77:183 78:182 79:181 80:180 81:179 82:178 83:177 84:176 85:170 86:160 87:150 88:149 89:148 90:147 91:146 92:145 93:144 94:140 95:130 96:120 97:110 98:109 99:108 100:107 101:106 102:105 103:104 104:100 105:90 106:80 107:70 108:69 109:68 110:67 111:66 112:65 113:64 114:60 115:50 116:40 117:39 118:38 119:37 120:36 121:35 122:34 123:33 124:31 125:30 126:20 127:10 128:9 129:8 130:7 131:6 132:5 133:4 134:3 135:2]
matching!!!
match order: 115, itemComb: [82 62]
match level: 50
redigo: HGET BaseLevelInfo 50 &{Id:50 Name:J2 Status:1 ClassId:1}
机况-匹配价格等级模板结束 ...

匹配穷举价格 ...
按系数计算定价价格 ...
basePrice: 33300.000000
sku: 13 value: -8081.000000 price: 25219.000000
sku: 18 value: 0.000000 price: 25219.000000
sku: 38 value: 32617.000000 price: 57836.000000
sku: 42 value: 0.000000 price: 57836.000000
sku: 471 value: -1530.000000 price: 56306.000000
sku: 2236 value: 0.000000 price: 56306.000000
sku: 2241 value: 0.000000 price: 56306.000000
level: 50 value: 339 price: 19087.732422
Format Evaluate Price: 19087.732422
base price: 19087.732422 -> 19000
定价价格计算结束 ...

【走销售价应用方案逻辑】【匹配销售价应用方案，调价规则】
===================1. 卖家参考价===================
加成价格计算开始 ...
    GetAdjustPrice|37|AdjustPlanInfo: &{Price:19000 Level:50 ProductId:41567 ClassId:1 BrandId:2 BasePrice:33300 Skuitem:[13 18 38 42 471 2236 2241] PriceAdjPlan:0xc0002ba000 PriceAdjPlan2nd:<nil>}
    Matching Product Rule
    Matching Class Brand Price Rule
【命中调价规则】
    ResultPriceType matching!!! Price: 19000.000000
【命中1：按按类目+品牌+初始化价格范围调价 规则 - 按比例加成】
    rule value: {Begin:100 End:30000 Percent:-50 Absolute:0 Type:1 PriceType:2}
    19000.000000 * ((-50 / 1000) + 1) = 18050.000000
    getAdjustPrice1nd|289|Price: 18050.000000
    Format Evaluate Price: 18050.000000
    不进行2次加成计算
【命中2：按按类目+品牌+初始化价格范围调价 规则 - 按绝对值加成】
【命中3：按机型调价 规则 - 按比例加成】
【命中4：按机型调价 规则 - 按绝对值金额加成】
加成价格计算结束 ...

    
===================2. 卖家最高价===================
加成价格计算开始 ...
    GetAdjustPrice|37|AdjustPlanInfo: &{Price:18000 Level:50 ProductId:41567 ClassId:1 BrandId:2 BasePrice:33300 Skuitem:[13 18 38 42 471 2236 2241] PriceAdjPlan:0xc0002ba120 PriceAdjPlan2nd:<nil>}
    Matching Product Rule
    Matching Class Brand Price Rule
    ResultPriceType matching!!! Price: 18000.000000
【命中1：按按类目+品牌+初始化价格范围调价 规则 - 按比例加成】
    rule value: {Begin:100 End:30000 Percent:150 Absolute:0 Type:1 PriceType:2}
    18000.000000 * ((150 / 1000) + 1) = 20700.000000
    getAdjustPrice1nd|289|Price: 20700.000000
    Format Evaluate Price: 20700.000000
    不进行2次加成计算
【命中2：按按类目+品牌+初始化价格范围调价 规则 - 按绝对值加成】
【命中3：按机型调价 规则 - 按比例加成】
【命中4：按机型调价 规则 - 按绝对值金额加成】
加成价格计算结束 ...

===================2. 买家最高价===================
加成价格计算开始 ...
    GetAdjustPrice|37|AdjustPlanInfo: &{Price:18000 Level:50 ProductId:41567 ClassId:1 BrandId:2 BasePrice:33300 Skuitem:[13 18 38 42 471 2236 2241] PriceAdjPlan:0xc0002ba240 PriceAdjPlan2nd:<nil>}
    Matching Product Rule
    Matching Class Brand Price Rule
    ResultPriceType matching!!! Price: 18000.000000
【命中1：按按类目+品牌+初始化价格范围调价 规则 - 按比例加成】
    rule value: {Begin:100 End:30000 Percent:110 Absolute:0 Type:1 PriceType:2}
    18000.000000 * ((110 / 1000) + 1) = 19980.000000
    getAdjustPrice1nd|289|Price: 19980.000000
    Format Evaluate Price: 19980.000000
    不进行2次加成计算
【命中2：按按类目+品牌+初始化价格范围调价 规则 - 按绝对值加成】
【命中3：按机型调价 规则 - 按比例加成】
【命中4：按机型调价 规则 - 按绝对值金额加成】
加成价格计算结束 ...

【生成定价估价记录】
Mgo Query: map[_id:eva_record_2107]
Mgo Change: {Update:map[$inc:map[sequence_value:1]] Replace:false Remove:false Upsert:false ReturnNew:false}
Mgo Result: {Sequence:58707}
EvaRecord: &{EvaluateId:58708 ProductId:41567 BasePrice:33300 CurBasePrice:33300 SbuType:2 EvaType:2 PriceType:3 VersionId:239 CurVersionId:239 OptLevelId:50 Select:[13 471 18 2236 38 42 2241 82 62 66 58 236 5530 55 78 7642 6931 23 5534 224 20 1078 2171 3245] SkuItem:[13 18 38 42 471 2236 2241] OptItem:[82 62 66 58 236 5530 55 78 7642 6931 23 5534 224 20 1078 2171 3245] LevelList:[] LevelTempId:15 Quotation:19000 LevelListPrice:[{Level:0 Price:18000} {Level:0 Price:20700} {Level:0 Price:19900}] ErrorCode:0 ErrorInfo:Success SpendTime:29 CreateTime:2021-07-13 23:29:54.301646018 +0000 UTC Interface:evaluate_sale_price EvaBasePrice:19000 IP:127.0.0.1 UserId:1895 ChannelId:0 Pid:0 BasePriceStaId:0 LevelStandId:0 SaleLevelId:0 BaseLevelTag:[] SaleLevelTag:[] AdjPlanId:14 AdjPlanVer:1 AdjustPrice:0 AdjPlanId2nd:0 AdjPlanVer2nd:0 AdjustPrice2nd:0 OptLevelName:J2 SaleLevelName:}

{"_data":{"_errStr":"SUCCESS","_data":{"evaBasePrice":"19000","sellerPrice":"18000","sellerMaxPrice":"20700","buyerPrice":"19900","recordId":"9210758708","levelId":"50","levelName":"J2","saleLevelId":"0","saleLevelName":"","baseLevelTag":[],"saleLevelTag":[]},"_errCode":"0","_ret":"0"},"_head":{"_callerServiceId":"116006","_groupNo":"1","_interface":"sale_apply_price","_invokeId":"mikingzhang_adjustPrice","_msgType":"response","_remark":"","_timestamps":"1626190194","_version":"0.01"}}
'''