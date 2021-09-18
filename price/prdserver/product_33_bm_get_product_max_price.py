#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 33.帮买根据产品SKU给出N成新最高价 - http://wiki.huishoubao.com/index.php?s=/105&page_id=6028
    server-bangmai_pro_eva
    入参：pid：必传，pid  |  productId：产品Id  |  skuList：产品SKU列表 没有则传空列表
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

class BM_Get_Product_Max_Price:
    def __init__(self):
        self.secret_key = "c36691ced620bf82ad3fc4642f8a6427"
        self.callerserviceid = "110001"

    def bm_get_product_sku(self,pid,productId):
        param = {"_head":{"_interface":"bm_get_product_sku","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"","_invokeId":"","_callerServiceId":"110001","_groupNo":"1"},"_param":{"pid":pid,"productId":productId}}
        url = "http://bmserver.huishoubao.com/bangmai/bm_get_product_sku"
        md5value = json.dumps(param) + "_" + self.secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":self.callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典
        options_list = respone_dict['_data']['_data']['options']

        str_options_list = []
        str_options_desc_show = ''
        for info in options_list:
            answerList = info['aInfo']
            index = random.randint(0, len(answerList) - 1)
            str_options_list.append(answerList[index]['aId'])
            # 以下只为打印输出随机取的估价选项数据
            str_options_desc_show += '"' + info['qName'] + ":" + answerList[index]['aName'] + '",'
        str_options_desc_show = str_options_desc_show[:-1]

        return str_options_list, str_options_desc_show

    def bm_get_product_max_price(self, pid, productId):
        (skuList, str_options_desc_show) = self.bm_get_product_sku(pid=pid,productId=productId)
        param = {"_head":{"_interface":"bm_get_product_max_price","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"","_invokeId":"","_callerServiceId":"110001","_groupNo":"1"},"_param":{"pid":pid,"productId":productId, "skuList":skuList}}
        url = "http://bmserver.huishoubao.com/bangmai/bm_get_product_max_price"
        md5value = json.dumps(param) + "_" + self.secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":self.callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())

        print('==========>1. 估价答案项ID传参数据为（随机取）：\n', skuList)
        print('==========>2. 以上估价答案项ID对应的选项+答案项名称：\n', '{' + str_options_desc_show[:-1] + '}' + '\n')
        hsb_response_print(respone=respone)

if __name__ == '__main__':
    product_33 = BM_Get_Product_Max_Price()
    # product_33.bm_get_product_max_price(pid='1405',productId='63330')
    # product_33.bm_get_product_max_price(pid='1405',productId='41567')
    product_33.bm_get_product_max_price(pid='1405',productId='38200')