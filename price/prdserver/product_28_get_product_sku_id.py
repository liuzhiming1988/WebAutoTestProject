#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 28.根据产品ID和SKU选项获取产品SKUID - http://wiki.huishoubao.com/index.php?s=/105&page_id=5569

    1-对应服务：server-base_product（base_product）  |  2-对应URL：http://prdserver.huishoubao.com
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

class Get_Product_Sku_Id:
    def __init__(self):
        self.secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
        self.callerserviceid = "112002"

    def pdt_sku_query(self, productId):
        param = {"_head":{"_interface":"pdt_sku_query","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"123","_invokeId":"111","_callerServiceId":"112002","_groupNo":"1"},"_param":{"subInterface":"sku_option_combination_get","info":{"productId":productId}}}
        url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
        md5value = json.dumps(param) + "_" + self.secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":self.callerserviceid}
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

        return str_sku_answer_list,str_Option_answer_desc

    def get_product_sku_id(self, productId):
        (skuArray,str_Option_answer_desc) = self.pdt_sku_query(productId=productId)
        param = {"_head":{"_interface":"get_product_sku_id","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"","_invokeId":"","_callerServiceId":"112002","_groupNo":"1"},"_param":{"productId":productId, "skuArray":skuArray}}
        url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
        md5value = json.dumps(param) + "_" + self.secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":self.callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())

        print('==========>1.【sku】选项-答案项ID（随机取）：\n', skuArray)
        print('\n')
        print('==========>2. 以上【sku】选项名称+答案项名称：\n', '{' + str_Option_answer_desc[:-1] + '}' + '\n')
        hsb_response_print(respone=respone)

if __name__ == '__main__':
    producy_25 = Get_Product_Sku_Id()
    producy_25.get_product_sku_id(productId='41567')
    # producy_25.get_product_sku_id(productId='63330')
    # producy_25.get_product_sku_id(productId='64247')
    # producy_25.get_product_sku_id(productId='1')

'''
测试
select Fid, Faid_list from t_pdt_sku  where Faid_list in ('#2236#471#42#36#18#15#');
'''