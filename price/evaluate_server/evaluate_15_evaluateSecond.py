#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 估价服务 - 15.用户二次估价接口  -  http://wiki.huishoubao.net/index.php?s=/138&page_id=2212

    入参：pid：回收宝对外入口ip | channel_id：渠道id（渠道ID赋值：代表使用2B估价模型），（有pid时可为空） | productid：估价产品id
        userid：登录用户id（未登录用户可为空） | select：用户选择的估价选项 | isBottomPrice：是否获取保底价，1是，默认为否
    出参：quotation：估算价格，单位分 | evaluateid：估价唯一id（id 会超过int(11)，请不要用int保存）（可通过：12 获取估价记录信息接口，获取信息）
        bottomPrice：保底价/起拍价，单位为分，isBottomPrice不为1时，返回空，isBottomPrice为1时 存在
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

class EvaluateSecond:
    def __init__(self):
        self.secret_key = "gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU"
        self.callerserviceid = "112006"

    def product_check_item(self, productId):
        param = {"_head": {"_interface": "product_check_item", "_msgType": "request", "_remark": "", "_version": "0.01","_timestamps": "123456", "_invokeId": "123456", "_callerServiceId": "112006","_groupNo": "1"}, "_param": {"productId": productId}}
        url = "http://codserver.huishoubao.com/detect/product_check_item"
        md5value = json.dumps(param) + "_" + self.secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID": self.callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典
        skuList = respone_dict['_data']['_data']['skuList']
        checkList = respone_dict['_data']['_data']['checkList']

        strSkuList = []
        strSkuDesc = ''
        for info in skuList:
            answerList = info['answerList']
            index = random.randint(0, len(answerList) - 1)
            strSkuList.append(answerList[index]['answerId'])
            strSkuDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'

        strCheckList = []
        strCheckDesc = ''
        for info in checkList:
            answerList = info['answerList']
            index = random.randint(0, len(answerList) - 1)
            strCheckList.append(answerList[index]['answerId'])
            strCheckDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'
        return strSkuList, strCheckList, strSkuDesc, strCheckDesc

    def convert_check_item_to_eva(self, orderId, productId, isOverInsurance):
        (skuList, checkList, skuDesc, checkDesc) = self.product_check_item(productId=productId)
        param = {"_head": {"_interface": "convert_check_item_to_eva", "_msgType": "request", "_remark": "","_version": "0.01", "_timestamps": "123456", "_invokeId": "123456","_callerServiceId": "112006", "_groupNo": "1"},"_param": {"orderId": orderId, "productId": productId, "skuList": skuList, "checkList": checkList,"isOverInsurance": isOverInsurance}}
        url = "http://codserver.huishoubao.com/detect/convert_check_item_to_eva"
        md5value = json.dumps(param) + "_" + self.secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID": self.callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典

        print('==========1. 产品sku选项-答案项ID（随机取）：\n', skuList)
        print()
        print('==========2. 检测机况选项-答案项ID（随机取）：\n', checkList)
        print()
        print('==========3. 以上【sku】+【机况】选项对应的问题项名称+答案项名称：\n', '{' + skuDesc + checkDesc[:-1] + '}' + '\n')
        return respone_dict['_data']['_data']['select'], respone_dict['_data']['_data']['selectName']

    ''' 估现网价格（目前仅定价系统，阿里渠道 会走这个二次询价逻辑） '''
    def evaluateSecond(self, order_id, productid, isOverInsurance, pid, channel_id):
        (select, select_desc) = self.convert_check_item_to_eva(orderId=order_id, productId=productid, isOverInsurance=isOverInsurance)
        param = {"head":{"interface":"evaluateSecond","msgtype":"request","remark":"","version":"0.01"},"params":{"cookies":"1111","ip":"127.0.0.1","pid":pid, "channel_id":channel_id, "productid":productid, "select":select, "userid":"0"}}
        url = "http://evaserver.huishoubao.com/rpc/evaluate"
        headers = {"Content-Type":"application/json"}
        respone = requests.post(url, data=json.dumps(param), headers=headers, proxies=hsb_eva_ipProxy_test())

        print('==========4. 用户选择的估价选项是：\n', select)
        print()
        print('==========5. 转换后的SKU+机况选项的描述：\n', select_desc)
        print()
        hsb_response_print(respone=respone)

if __name__ == '__main__':
    evaluate_15 = EvaluateSecond()
    # evaluate_15.insured_options(order_id='7573755', productId='41567', isOverInsurance='1')
    # evaluate_15.evaluateSecond(order_id='7609547', productid='63330', isOverInsurance='0', pid='', channel_id='10000254')
    # evaluate_15.evaluateSecond(order_id='7609547', productid='63330', isOverInsurance='0', pid='', channel_id='10000254')
    # evaluate_15.evaluateSecond(order_id='7610414', productid='41567', isOverInsurance='0', pid='', channel_id='10000254')
    # evaluate_15.evaluateSecond(order_id='7610414', productid='41567', isOverInsurance='1', pid='', channel_id='10000254')
    evaluate_15.evaluateSecond(order_id='7610414', productid='41567', isOverInsurance='1', pid='', channel_id='40000001')


'''
# select t_tag.Ftag_id, t_tag.Fchannel_id, t_channel.Fchannel_flag  
	from t_maptag  
	left join t_tag on t_tag.Ftag_id = t_maptag.Ftag_id  
	left join t_channel on t_channel.Fchannel_id = t_tag.Fchannel_id  where Fp_id = '1405' or t_tag.Fchannel_id = '10000164';

Platform Eva Version:88 standardPrice:500
hset Eva_PId_Cache 1405 {"channelFlag":"1","channelId":"10000164","platformId":"1","platformName":"2C","tagId":"1405","time":"1602732115"}

整机项: 500*100/100 = 500
系数特殊规则:500 = 500
选项分组命中等级:100 lType:1 lValue:100 uType:1 uValue:100
选项分组下限百分比:(500*100)/100=500
选项分组上限百分比:(500*100)/100=500
选项分组在上下限范围内, 无需校正
先计算选项分组再计算差值算法 差值:(500+500*0/100+0)*100/100 = 500

outdata={"body":{"data":{"evaluateid":"20104261","quotation":"500"},"ret":"0","retcode":"0","retinfo":"成功"},"head":{"interface":"evaluateSecond","msgtype":"response","remark":"","version":"0.01"}}
'''