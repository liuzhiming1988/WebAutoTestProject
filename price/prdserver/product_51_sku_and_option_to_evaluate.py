#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 51.商品库sku信息加大质检机况用户估价接口(回收宝专业版使用) - http://wiki.huishoubao.com/web/#/105?page_id=13254
    1. 对应服务：server-evaluate_detect（服务器应用名：server-evaluate_detect）
    2. 对应URL http://codserver.huishoubao.com

    入参：channel_id：必填，渠道id，各个产品在不同渠道有不同的价格，可传””，但必须传递 | pid：必填，pid，可为空 | platformType：必填，平台类型，可为空
        productId：必填，修改产品后的产品id，优先使用这个，未传递则使用DB中的 | skuList：必填，商品库sku答案选项 | optionList：必填，大质检答案选项
        userId：必填，检测工程师id | ip：非必填，用户公网访问IP
    出参：select：转换出来的估价选项 | selectName：转化后的选项的选项描述 | price：用户估价价格,单位为分 | evaluateId：估价Id
        insured：保价标记，1-保价，0-不保价 | orderId：订单Id | productId：产品Id | transformList：转换出来的估价选项详细信息
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test, hsb_response_print

class Sku_And_Option_To_Evaluate:
    def __init__(self):
        self.secret_key = "gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU"
        self.callerserviceid = "112006"

    def get_sku_option_item_by_channel_id(self, productId, platformType, channelId, pid):
        param = {"_head": {"_interface": "get_sku_option_item_by_channel_id", "_msgType": "request", "_remark": "","_version": "0.01", "_timestamps": "123456", "_invokeId": "123456","_callerServiceId": "112006", "_groupNo": "1"},"_param": {"productId": productId, "platformType": platformType, "channelId": channelId, "pid": pid,"ip": "127.0.0.1"}}
        url = "http://codserver.huishoubao.com/detect/get_sku_option_item_by_channel_id"
        md5value = json.dumps(param) + "_" + self.secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID": self.callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典
        options_list = respone_dict['_data']['_data']['itemList']

        str_sku_list = []
        str_options_list = []
        for info in options_list:
            # conftype：类型id，1-是包括SKU类，2-是单选类，3-是功能性类
            conftypeList = info['conftype']
            # 分开取，conftypeList == "1"，为sku
            if conftypeList == "1":
                answerList = info['question']
                index = random.randint(0, len(answerList) - 1)
                str_sku_list.append(answerList[index]['id'])
            # 分开取，conftypeList == "2" 或者 "3"，为机况
            else:
                answerList = info['question']
                index = random.randint(0, len(answerList) - 1)
                str_options_list.append(answerList[index]['id'])
        # 分开返回sku与机况数据
        return str_sku_list, str_options_list

    def sku_and_option_to_evaluate(self,channelId, productId, pid, platformType):
        # (skuList, optionList) = self.get_sku_option_item_by_channel_id(productId=productId, platformType=platformType, channelId=channelId, pid=pid)
        skuList = ['7630', '130', '18', '2236', '36', '42', '1773']
        optionList = ['7473', '7518', '7418', '7515', '7506', '7503', '7423', '7494', '7492', '7425', '7487', '7483', '7429', '7524', '7471', '7468', '7433', '7466', '7462', '7461', '7440', '7452', '7450', '7447', '7442', '7614', '7603', '7589', '7587', '7581', '7579', '7574', '7572', '7562', '7559', '7558', '7554', '7548', '7541', '7537', '7532', '7528']
        param = {"_head":{"_interface":"sku_and_option_to_evaluate","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"123456","_invokeId":"123456","_callerServiceId":"112006","_groupNo":"1"},"_param":{"channelId":channelId,"productId":productId,"skuList":skuList,"optionList":optionList,"userId":"135","ip":"127.0.0.1","pid":pid,"platformType":platformType}}
        url = "http://codserver.huishoubao.com/detect/sku_and_option_to_evaluate"
        md5value = json.dumps(param) + "_" + self.secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":self.callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置

        print('==========>1. 接口响应『json』格式数据，{0} 产品的商品库sku答案选项为：\n'.format(productId), skuList)
        print()
        print('==========>2. 接口响应『json』格式数据，{0} 产品的大质检机况答案选项为：\n'.format(productId), optionList)
        print()
        hsb_response_print(respone=respone)

if __name__ == '__main__':
    product_51 = Sku_And_Option_To_Evaluate()

    # skuList = ["12","130","18","2236","36","1091","2242"]
    # optionList = ["82","63","66","236","58","73","77","56","7641","6930","5534","24","224","20","1078","2170","3245"]
    # product_51.sku_and_option_to_evaluate(channelId='40000001',productId='41567', pid='1001',platformType='') # iPhone x

    # skuList = ["12", "130", "2238", "37", "2591"]
    # optionList = ["63", "65", "59", "3247", "73", "56", "78", "9", "53", "7641", "224", "6931", "24", "6703", "3246", "21", "2170", "5534"]
    # product_51.sku_and_option_to_evaluate(channelId='40000001',productId='63446', pid='1001',platformType='') # 华为 Mate 30 Pro（5G）
    # product_51.sku_and_option_to_evaluate(channelId='10000135',productId='63446', pid='', platformType='') # 华为 Mate 30 Pro（5G） | 闲鱼信用速卖
    # product_51.sku_and_option_to_evaluate(channelId='10000135',productId='63446', pid='', platformType='1') # 华为 Mate 30 Pro（5G） | 闲鱼信用速卖
    # product_51.sku_and_option_to_evaluate(channelId='10000135',productId='63446', pid='', platformType='2') # 华为 Mate 30 Pro（5G） | 闲鱼信用速卖
    # product_51.sku_and_option_to_evaluate(channelId='10000135',productId='63446', pid='', platformType='10') # 华为 Mate 30 Pro（5G） | 闲鱼信用速卖
    # product_51.sku_and_option_to_evaluate(channelId='10000135',productId='63446', pid='1001', platformType='') # 华为 Mate 30 Pro（5G） | 闲鱼信用速卖

    # product_51.sku_and_option_to_evaluate(channelId='40000001',productId='63330', pid='1001',platformType='') # iPhone 11
    # product_51.sku_and_option_to_evaluate(channelId='10000255',productId='63330', pid='',platformType='') # iPhone 11 | B端帮卖平台

    ''' 2021年5月27日 对接口list进行严格校验'''
    # "_errStr":"转换估价sku错误,估价sku问题项 制式 没有匹配上任何答案项"
    # product_51.sku_and_option_to_evaluate(channelId='10000255', productId='41567', pid='', platformType='') #skuList = [] optionList = []

    # "_errStr": "skuList 参数格式错误"
    # product_51.sku_and_option_to_evaluate(channelId='10000255', productId='41567', pid='', platformType='') #skuList = [""] optionList = [""]

    # skuList = ['7630', '130', '18', '2236', '36', '42', '1773']   optionList = []  |  "_errStr":"价格计算失败"
    # product_51.sku_and_option_to_evaluate(channelId='10000255', productId='41567', pid='', platformType='')

    # skuList = ['7630', '130', '18', '2236', '36', '42', '1773']   optionList = [""] | "_errStr":"optionList 参数格式错误"
    # product_51.sku_and_option_to_evaluate(channelId='10000255', productId='41567', pid='', platformType='')

    # skuList = ['7630', '130', '18', '2236', '36', '42', '1773']   optionList = ["abc"] | "_errStr":"optionList 参数格式错误"
    product_51.sku_and_option_to_evaluate(channelId='10000255', productId='41567', pid='', platformType='')


'''
POST_DATA = {"_head": {"_interface": "sku_and_option_to_evaluate", "_msgType": "request", "_remark": "", "_version": "0.01", "_timestamps": "123456", "_invokeId": "123456", "_callerServiceId": "112006", "_groupNo": "1"}, "_param": {"channelId": "40000001", "productId": "41567", "skuList": ["12", "130", "18", "2236", "36", "1091", "2242"], "optionList": ["82", "63", "66", "236", "58", "73", "77", "56", "7641", "6930", "5534", "24", "224", "20", "1078", "2170", "3245"], "userId": "135", "ip": "127.0.0.1", "pid": "1001", "platformType": ""}}

【base_product】
curl -H 'HSB-OPENAPI-SIGNATURE:ab34e1ce17c27735d35dccf7743c59f1' -H 'HSB-OPENAPI-CALLERSERVICEID:216008' -d '{"_head":{"_callerServiceId":"216008","_groupNo":"1","_interface":"eva_option_get","_invokeId":"34682fe7a503ce7e193d64feea1a379b","_msgType":"request","_remark":"","_timestamps":"1605491337","_version":"0.01"},"_param":{"channel_id":"40000001","ip":"127.0.0.1","pid":"1001","platform_type":"","product_id":"41567","user_name":"server-evaluate_detect"}}' http://prdserver.huishoubao.com/rpc/new_product_lib

【rpc_evaluate_server】
curl -d '{"head":{"interface":"evaluate","msgtype":"request","remark":"","version":"0.01"},"params":{"channel_id":"40000001","cookies":"server-evaluate_detect.PNSFDLEU","ip":"127.0.0.1","pid":"1001","productid":"41567","select":["12","1091","36","1634","18","82","63","66","236","58","73","77","56","7641","6930","5534","24","224","20","1078","2170","3245"],"userid":"135"}}' http://evaserver.huishoubao.com/rpc/evaluate

    select t_tag.Ftag_id, t_tag.Fchannel_id, t_channel.Fchannel_flag  from t_maptag  left join t_tag on t_tag.Ftag_id = t_maptag.Ftag_id  left join t_channel on t_channel.Fchannel_id = t_tag.Fchannel_id  where Fp_id = 1001;
    
    select Fplatform_type from t_eva_channel_platform_map  where Fvalid=1 and Fdelete_flag=0 and Fchannel_id=40000001;
    
    select Fplatform_name from t_eva_platform_type  where Fplatform_type = 1;
    productId:41567 pId:1001 channelId:40000001 platformType:1

SELECT * FROM recycle.t_eva_item_base where Fid in ("12", "130", "2238", "37", "2591");
SELECT * FROM recycle.t_eva_item_base 
    where Fid in ("63","65","59","3247","73","56","78","9","53","7641","224","6931","24","6703","3246","21","2170","5534");
				  "63","65","59","3247","73","56","78","9","53","7641","224","6931","24","6703","3246","21","2170","5534"
SELECT * FROM recycle.t_eva_item_base where Fid in ("12","879","2591");
    
'''