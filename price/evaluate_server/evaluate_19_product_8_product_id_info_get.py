#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 1.获取产品详情  +  product_id_info_get
    2.产品服务-8  +  http://wiki.huishoubao.com/index.php?s=/105&page_id=1597
    SELECT Fproduct_id, COUNT(A.Fproduct_id) AS Total FROM hsblog.t_eva_interface_record_2020_01 A WHERE A.Finterface = 'evaluate'
		AND A.Fcreate_date = '2020-01-02' AND A.Fproduct_id IN (SELECT B.Fproduct_id FROM recycle.t_pdt_class_map B
	WHERE B.Fvalid = 1 AND B.Fclass_id = 1) GROUP BY A.Fproduct_id ORDER BY Total DESC;  '''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def product_id_info_get( fproduct_id, fchannel_id ):
    param = {"_head":{"_interface":"product_id_info_get","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"123","_invokeId":"111","_callerServiceId":"110003","_groupNo":"1"},"_param":{ "fproduct_id":fproduct_id,"fchannel_id":fchannel_id }}

    secret_key = "Qqn2QV8pcdCIzhpJeE6paatWZAtc2CTK"
    callerserviceid = "110003"
    url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # product_id_info_get( fproduct_id='41567', fchannel_id='40000001' )
    product_id_info_get( fproduct_id='4006', fchannel_id='10000164' )

# 返回
'''   {"_body":{"_data":{"product_info":[{"fbrand_id":"11","fbrand_id_v2":"2","fbrand_name":"苹果","fclass_id":"1","fclass_name":"手机","fkey_word":"iPhoneXS；XS","fmarket_time":"2018-09-21","fmax_price":"425500","fmin_price":"7200","fos_type_id":"1","fos_type_name":"ios系统","fproduct_desc":"","fproduct_id":"54790","fproduct_logo":"54790_20180922111211_884.png","fproduct_name":"iPhone XS","frecycle_type_id":"3","frecycle_type_name":"正常回收","fvalid":"1"}],"sum_num":"1"},"_ret":"0","_retcode":"0","_retinfo":"成功"},"_head":{"_callerServiceId":"110003","_groupNo":"1","_interface":"product_id_info_get","_invokeId":"111","_msgType":"response","_remark":"","_timestamps":"1581994473","_version":"0.01"}}   '''