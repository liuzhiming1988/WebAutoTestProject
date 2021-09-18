#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 43.检测通过商品库sku获取估价sku选项  - http://wiki.huishoubao.net/index.php?s=/105&page_id=7607
    1. 对应服务：server-evaluate_detect（服务器应用名：server-evaluate_detect）
    2. 对应URL http://codserver.huishoubao.com

    入参：orderId：订单Id（必填） | productId：产品id（必填） |  skuList：商品库sku列表（必填）
    出参：productId：产品Id | insured：0-过保 1-保价 | orderId：订单Id | itemList：估价sku选项列表 | aId：答案选项ID
        aName：答案选项名称 | qId：问题项ID | qName：问题项名称
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

class Product_Lib_Sku_To_Eva_Sku:
    def pdt_sku_query(self, productId):
        param = {"_head": {"_interface": "pdt_sku_query", "_msgType": "request", "_remark": "", "_version": "0.01","_timestamps": "123", "_invokeId": "111", "_callerServiceId": "112002", "_groupNo": "1"},"_param": {"subInterface": "sku_option_combination_get","info": {"productId":productId, "combination":"1"}}}
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
        # 以下只为打印输出随机取的估价选项数据
            str_Option_answer_desc += '"' + info['qName'] + ":" + answerList[index]['aName'] + '",'
        str_Option_answer_desc = str_Option_answer_desc[:-1]

        print('==========>1. 机型标准SKU为（随机取）：\n', str_sku_answer_list)
        print()
        print('==========>2. 以上SKU答案项ID对应的选项+答案项名称：\n', '{' + str_Option_answer_desc[:-1] + '}' + '\n')
        return str_sku_answer_list

    def product_lib_sku_to_eva_sku(self, orderId, productId):
        skuList = self.pdt_sku_query(productId=productId)
        # skuList = ['14', '130', '18', '2236', '36', '1091', '1083']
        param = {"_head":{"_interface":"product_lib_sku_to_eva_sku","_msgType":"request","_remark":"hello","_version":"0.01","_timestamps":"123","_invokeId":"111","_callerServiceId":"112006","_groupNo":"1"},"_param":{ "orderId":orderId, "productId":productId,"skuList":skuList}}
        secret_key = "gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU"
        callerserviceid = "112006"
        url = "http://codserver.huishoubao.com/detect/product_lib_sku_to_eva_sku"
        md5value = json.dumps(param) + "_" + secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典
        sku_list = respone_dict['_data']['_data']['itemList']

        str_sku_list = []
        str_sku_desc_show = ''
        for index in range(0, len(sku_list)):
            str_sku_list.append(sku_list[index]['aId'])
        # 以下只为打印输出随机取的估价选项数据
            str_sku_desc_show += '"' + sku_list[index]['qName'] + ":" + sku_list[index]['aName'] + '",'
        str_sku_desc_show = str_sku_desc_show[:-1]

        print('接口响应『json』格式数据为：\n', json.dumps(respone_dict, ensure_ascii=False) + '\n')
        print('==========>3. 通过商品库sku获取到的估价sku选项为：\n',str_sku_list)
        print()
        print('==========>4. 以上估价SKU选项信息未：\n', '{' + str_sku_desc_show + '}' + '\n')

if __name__ == '__main__':
    ''' 商品库sku可以从 25接口获取 '''
    prdserver43 = Product_Lib_Sku_To_Eva_Sku()
    # prdserver43.product_lib_sku_to_eva_sku(orderId='7632330', productId='41567')
    prdserver43.product_lib_sku_to_eva_sku(orderId='7632330', productId='63330')

'''
POST_DATA = {"_head": {"_interface": "product_lib_sku_to_eva_sku", "_msgType": "request", "_remark": "hello", "_version": "0.01", "_timestamps": "123", "_invokeId": "111", "_callerServiceId": "112006", "_groupNo": "1"}, "_param": {"orderId": "7598829", "productId": "41567", "skuList": ["14", "130", "17", "2236", "36", "42", "1083"]}}

curl -d '{"head":{"interface":"insured_options","msgtype":"request","remark":"","version":"0.01"},"params":{"order_id":"7598829","productId":"41567","user_name":"server-evaluate_detect"}}' http://evaserver.huishoubao.com/rpc/insured

    curl -H 'HSB-OPENAPI-SIGNATURE:49f7ee7cf1641515fcdc314071c6ad57' -H 'HSB-OPENAPI-CALLERSERVICEID:216009' -d '{"_head":{"_callerServiceId":"216009","_groupNo":"1","_interface":"getOrderInfo","_invokeId":"5db064721c241fef3779ddf1e226a7ef","_msgType":"request","_remark":"","_timestamps":"1604472512","_version":"0.01"},"_param":{"containInfo":["good","basic","evaluation"],"orderId":"7598829"}}' http://ordserver.huishoubao.com/order_center/getOrderInfo
    
    curl -H 'HSB-OPENAPI-SIGNATURE:a2327cec1de453222670f60561e4a787' -H 'HSB-OPENAPI-CALLERSERVICEID:216009' -d '{"_head":{"_callerServiceId":"216009","_groupNo":"1","_interface":"get_eva_record","_invokeId":"00cd15e59d8f290e1a439563205e7fcb","_msgType":"request","_remark":"","_timestamps":"1604472512","_version":"0.01"},"_param":{"evaluateId":"201010419"}}' http://evaserver.huishoubao.com/eva_query/get_eva_record
    
    curl -H 'HSB-OPENAPI-SIGNATURE:0e7fb6e2c0ab6ca27a513b77949d9218' -H 'HSB-OPENAPI-CALLERSERVICEID:212006' -d '{"_head":{"_callerServiceId":"212006","_groupNo":"1","_interface":"product_id_info_get","_invokeId":"352350de8f503b0cea631358f558d119","_msgType":"request","_remark":"","_timestamps":"1604472512","_version":"0.01"},"_param":{"evaFlag":"1","fchannel_id":"40000001","fproduct_id":"41567"}}' http://prdserver.huishoubao.com/rpc/new_product_lib

select Fstandard_price, Fproduct_item, Fshow_item, Fbasic_price, Frick_guarantee, Fprice_control, Fneed_evaluate, Fproduct_id, Fitem_param_id, Fos_type, Fvalid, Fuse_standard_eva, Fitem_template_id, Fsku_map from t_eva_platform_product where Fproduct_id=41567 and Fplatform_type=1 and Fdelete_flag = 1;
'''