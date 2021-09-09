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

    def base_price_evaluatee(self, channelId, pid, productId, evaType, ip, priceType, freqLimitType):
        (strSkuList, strSkuDesc, strCheckList, strCheckDesc) = self.product_check_item_34(productId=productId)

        # strSkuList = []
        # strCheckList = ['8297', '8301',    '8305', '8309', '8312',    '8316', '8320', '8323', '8326', '8333', '8336', '8339', '8343', '8349', '8351', '8359', '8361', '8364', '8367', '8371', '8375', '8378', '8382', '8385', '8389', '8393', '8397', '8403', '8408', '8412', '8416', '8419', '8422', '8425', '8429', '8432', '8436', '8441', '8444', '8449']

        # 1. 苹果 iPhone X | 销售定价
        # strSkuList = ['12', '471', '18', '2236', '38', '1091', '2242']
        # strCheckList = ['9016', '9019', '9027', '9029', '9037', '9039', '9052', '9056', '9057', '9059', '9062', '9070','9072', '9074', '7559', '9078', '9079', '9081', '7575', '9082', '9086', '9088', '9090', '9095','9099', '9104', '9113', '9117', '7532',   '9107', '9108', '9109']

        # 2. 安卓 华为 P40（5G） | 销售定价
        # strSkuList = ['2492', '130', '2237', '38', '2355']
        # strCheckList = ['9018', '9021',    '9027',    '9029', '9037', '9039', '9049', '9056', '9057', '9060', '9065', '9067', '9071', '9074', '7559', '9077', '9080', '9081', '7575', '9083', '7586', '9089', '9091', '9097', '9101', '9105', '9107', '9113', '9118', '7534']

        # 3. 安卓 华为 P40（5G） | 回收定价
        # strSkuList = ['2492', '130', '2237', '38', '2355']
        # strCheckList = ['8297', '8301',    '8305', '8309', '8312',    '8316', '8320', '8323', '8326', '8333', '8336', '8339', '8343', '8349', '8351', '8359', '8361', '8364', '8367', '8371', '8375', '8378', '8382', '8385', '8389', '8393', '8397', '8403', '8408', '8412', '8416', '8419', '8422', '8425', '8429', '8432', '8436', '8441', '8444', '8449']

        # 4. 安卓 iPhone 3G | 销售定价  |  无sku机型
        # strSkuList = []
        # strCheckList = ['9015', '9019',    '9027',     '9030', '9037', '9045', '9051', '9056', '9058', '9059', '9062', '9070', '9073', '9074', '9076', '9078', '9080', '9081', '7574', '9083', '9086', '7589', '9090', '9094', '9099', '9103', '9109', '9113', '9118', '7533']

        # 4. 安卓 iPhone 3G | 回收定价  |  无sku机型
        # strSkuList = []
        # strCheckList = ['8297', '8301',    '8305', '8309', '8312',    '8316', '8320', '8323', '8326', '8333', '8336', '8339', '8343', '8349', '8351', '8359', '8361', '8364', '8367', '8371', '8375', '8378', '8382', '8385', '8389', '8393', '8397', '8403', '8408', '8412', '8416', '8419', '8422', '8425', '8429', '8432', '8436', '8441', '8444', '8449']

        param = {"_head":{"_interface":"evaluate","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"1525332832","_invokeId":"mikingzhang_adjustPrice","_callerServiceId":"116006","_groupNo":"1"},"_param":{"channelId":channelId, "pid":pid, "productId":productId, "evaType":evaType,"skuItem":strSkuList, "optItem":strCheckList, "ip":ip, "userId":"1002","priceType":priceType, "freqLimitType":freqLimitType}}

        secret_key = "R2gFCRbILiNhwv3YbtaGceYJlPS5Ku02"
        callerserviceid = "116006"
        url = "http://bpeserver.huishoubao.com/base_price/evaluate"
        md5value = json.dumps(param) + "_" + secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_k8s_test())

        # print('========>1.『{0}』 产品的『检测标准化选项-sku』(随机取)为：\n'.format(productId), strSkuList)
        # print('\n========>2. 以上『检测标准化选项-sku』为：\n', '{' + strSkuDesc[:-1] + '}')
        # print('\n========>3.『{0}』 产品的『检测标准化选项-机况-34』(随机取)为：\n'.format(productId), strCheckList)
        # print('\n========>4. 以上『检测标准化选项-机况-34』为：\n', '{' + strCheckDesc[:-1] + '}')
        hsb_response_print(respone=respone)

if __name__ == '__main__':
    '''evaType：3-34标准质检(销售定价），价格3.0-填0（回收定价） |  priceType：价格类型：1-销售定价，2-回收定价'''
    baseprice_23 = Base_Price_Evaluatee()
    # strSkuList = ['12', '471', '18', '2236', '38', '1091', '2242']
    # strCheckList = ['9016', '9019', '9027', '9029', '9037', '9039', '9052', '9056', '9057', '9059', '9062', '9070','9072', '9074', '7559', '9078', '9079', '9081', '7575', '9082', '9086', '9088', '9090', '9095','9099', '9104', '9106', '9113', '9117', '7532']  # 9027，命中，"levelId":"600","levelName":"S"

    # priceType，传空  |  "_errStr":"请求参数错误 [PriceType为必填字段]"  |  正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', evaType='3', ip='127.0.0.1', priceType='', freqLimitType='0')

    # priceType，传错  |  "_errStr":"请求参数错误 [PriceType必须是[1 2]中的一个]"  |  正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', evaType='3', ip='127.0.0.1', priceType='55', freqLimitType='0')

    # evaType，传空  | "_errStr":"请求参数错误 [EvaType为必填字段]"  |  正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', evaType='', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # evaType，传错  |  "_errStr":"请求参数错误 [EvaType必须是[0 1 2 3]中的一个]"  |  正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', evaType='55', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # productId，传空  |  "_errStr":"请求参数错误 [ProductId为必填字段]"  |  正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # productId，产品为下架状态  |  "_errStr":"产品为下架状态"
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='54801', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # productId，30835，无销售定价，销售定价状态未启用  |  "_errStr":"未定价状态机型"  |  正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='30835', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # productId，54791，有销售定价，销售定价状态未启用  |  "_errStr":"未定价状态机型"  |  正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='54791', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # 渠道 PID 传空  | "_errStr":"请求参数错误 [ChannelId为必填字段]"  |  正常
    # baseprice_23.base_price_evaluatee(channelId='', pid='', productId='41567', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # PID传空  |  "_errStr":"请求参数错误 [Pid为必填字段]"  |  正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='', productId='41567', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # 渠道ID传空 | "_errStr":"请求参数错误 [ChannelId为必填字段]"  |  正常
    # baseprice_23.base_price_evaluatee(channelId='', pid='0', productId='41567', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')
    # baseprice_23.base_price_evaluatee(channelId='', pid='1001', productId='41567', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # 同传渠道 PID  |  用的是PID（及PID关联渠道），如果要到渠道层级，pid需传0  |  正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='1001', productId='41567', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # 同传渠道 PID，渠道 与 PID  不对应  |  不报错，不会走到调价逻辑  |  正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='1118', productId='41567', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # 同传渠道 PID，渠道 与 PID  不对应 | 40000001下面没有1004这个pid，但是30000001下面有1004，关联了同一个方案  |   不报错，不会走到调价逻辑  |  正常
    # Mgo query: map[Fchannel_id:40000001 Fpid:1004 Fprice_type:1 Fstatus:1]  结果是空
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='1004', productId='41567', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # 传渠道 PID， 渠道PID为禁用状态  |  正常，不会走到调价逻辑
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='1117', productId='41567', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # 销售价应用方案，为禁用状态 | 正常，不会走到调价逻辑
    baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='30748', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # 销售价应用方案，过了有效期  |  正常，不会走到调价逻辑
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # 销售价应用方案，还未到有效期  |  正常，不会走到调价逻辑
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # 不传sku，少传sku  |  "_errStr":"SKU个数错误: U[0] P[7]"  |  正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # 不传机况  |   "_errStr":"请求参数错误 [select optItem 不能同时为空]"  |  正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # 少传机况  |   正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # 入参机况未匹配到选项等级组合  strCheckList = ['9016']  |  "_errStr":"机况选项未匹配到选项等级组合"  |  正常
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # 入参机况， 某个问题项，传了多个答案项（多选）  |   正常
    # strCheckList = ['9016', '9019', '9027', '9029', '9037', '9039', '9052', '9056', '9057', '9059', '9062', '9070', '9072', '9074', '7559', '9078', '9079', '9081', '7575', '9082', '9086', '9088', '9090', '9095', '9099', '9104', '9113', '9117', '7532', '9107', '9108', '9109']
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='41567', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')

    # evaType：价格2.0 质检类型，1-57标准质检，2-大质检  |  暂不测试

    '''evaType：3-34标准质检(销售定价），价格3.0-填0（回收定价） |  priceType：价格类型：1-销售定价，2-回收定价'''
    # 安卓，销售定价 | 华为 P40（5G） |  销售价应用方案 - 自主运营
    # "quotation":"18900","evaBasePrice":"13600","adjustPrice":"18900","adjustPrice2nd":"0"
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='64000', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')
    # "quotation":"5400","evaBasePrice":"3900","adjustPrice":"5400","adjustPrice2nd":"0"
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='4157', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0') # 华为 OPhone  无sku

    # 安卓，销售定价 | 华为 P40（5G） |  销售价应用方案 - 在其他应用方案基础上运营
    # "quotation":"31100","evaBasePrice":"13600","adjustPrice":"18900","adjustPrice2nd":"31100"
    # baseprice_23.base_price_evaluatee(channelId='10000012', pid='1003', productId='64000', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0')
    # "quotation":"17600","evaBasePrice":"3900","adjustPrice":"5400","adjustPrice2nd":"17600"
    # baseprice_23.base_price_evaluatee(channelId='10000012', pid='1003', productId='4157', evaType='3', ip='127.0.0.1', priceType='1', freqLimitType='0') # 华为 OPhone  无sku

    # 安卓，销售定价 | 华为 P40（5G） |  回收-自主调价-自动使用
    # "quotation":"22900","evaBasePrice":"17800","adjustPrice":"22900","adjustPrice2nd":"0"
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='64000', evaType='0', ip='127.0.0.1', priceType='2', freqLimitType='0')
    # "quotation":"5400","evaBasePrice":"4200","adjustPrice":"5400","adjustPrice2nd":"0"
    # baseprice_23.base_price_evaluatee(channelId='40000001', pid='0', productId='4157', evaType='0', ip='127.0.0.1', priceType='2', freqLimitType='0') # 华为 OPhone  无sku

    # 安卓，销售定价 | 华为 P40（5G） |  回收-自主调价-不自动使用
    # "quotation":"62200","evaBasePrice":"17800","adjustPrice":"62200","adjustPrice2nd":"0"
    # baseprice_23.base_price_evaluatee(channelId='10000060', pid='0', productId='64000', evaType='0', ip='127.0.0.1', priceType='2', freqLimitType='0')
    # "quotation":"48600","evaBasePrice":"4200","adjustPrice":"48600","adjustPrice2nd":"0"
    # baseprice_23.base_price_evaluatee(channelId='10000060', pid='0', productId='4157', evaType='0', ip='127.0.0.1', priceType='2', freqLimitType='0') # 华为 OPhone  无sku

    # 安卓，销售定价 | 华为 P40（5G） |  回收-在其他调价方案基础上调价-自动
    # "quotation":"27100","evaBasePrice":"18500","adjustPrice":"23800","adjustPrice2nd":"27100"
    # baseprice_23.base_price_evaluatee(channelId='10000079', pid='0', productId='64000', evaType='0', ip='127.0.0.1', priceType='2', freqLimitType='0')
    # "quotation":"8700","evaBasePrice":"4200","adjustPrice":"5400","adjustPrice2nd":"8700"
    # baseprice_23.base_price_evaluatee(channelId='10000079', pid='0', productId='4157', evaType='0', ip='127.0.0.1', priceType='2', freqLimitType='0') # 华为 OPhone  无sku

    # 安卓，销售定价 | 华为 P40（5G） |  回收-在其他调价方案基础上调价-不自动
    # "quotation":"62200","evaBasePrice":"17800","adjustPrice":"62200","adjustPrice2nd":"0"
    # baseprice_23.base_price_evaluatee(channelId='30000001', pid='0', productId='64000', evaType='0', ip='127.0.0.1', priceType='2', freqLimitType='0')
    # "quotation":"69900","evaBasePrice":"4200","adjustPrice":"48600","adjustPrice2nd":"69900"
    # baseprice_23.base_price_evaluatee(channelId='30000001', pid='0', productId='4157', evaType='0', ip='127.0.0.1', priceType='2', freqLimitType='0') # 华为 OPhone  无sku
'''
【外部接口】 【销售价应用方案估价接口】【第一版】【商家自检 - 价格查询 当下在用】

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

'''
【错误分析】
"_errStr":"sku选项错误，产品不存在sku: 2238","_data":null,"_errCode":"901","_ret":"901"
可能是商品库新增的SKU
    定价系统 - 销售定价 - 定价参数维护，会同步，但是没有编辑过系数并提交过审核，是没有记录的
    可以在，定价系统 - 销售价查询，查看是否有这个SKU
    解决方法：在 定价系统 - 销售定价 - 定价参数维护，编辑SKU系数，提交审核，审核通过，即可
'''