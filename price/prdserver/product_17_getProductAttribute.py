#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 17.获取产品属性接口 - http://wiki.huishoubao.com/index.php?s=/105&page_id=3671

    1.对应服务：server-base_product（base_product）  |  2.对应URL：http://prdserver.huishoubao.com
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def getProductAttribute(productId):
    param = {"_head":{"_interface":"getProductAttribute","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"","_invokeId":"","_callerServiceId":"112002","_groupNo":"1"},"_param":{"productId":productId}}
    secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
    callerserviceid = "112002"
    url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # getProductAttribute(productId='')
    # getProductAttribute(productId='41567')
    # getProductAttribute(productId='64000')
    # getProductAttribute(productId='31117')
    # getProductAttribute(productId='31212')
    getProductAttribute(productId='111111111111111111111')

# SELECT t_product.Fproduct_id, t_product.Fproduct_name, t_product.Fproduct_desc, t_product.Fpic_id, t_product.Fkey_word, t_product.Fis_upper, t_product.Fputaway_time, t_product.Fremarks, t_product.Fattribute_id, t_product.Fos_type, t_eva_os_type.Fos_name, t_product.Frecycle_type, t_eva_recycle_type.Frecycle_type AS Frecycle_name, t_product.Fclass_id, t_pdt_class.Fname AS Fclass_name, tnobm.Fold_brand_id, tnobm.Fold_brand_name, tnobm.Fnew_brand_id FROM t_product LEFT JOIN t_pdt_class ON t_pdt_class.Fid = t_product.Fclass_id LEFT JOIN t_new_old_brand_map tnobm ON tnobm.Fnew_brand_id = t_product.Fbrand_id LEFT JOIN t_eva_os_type ON t_product.Fos_type = t_eva_os_type.Fos_id LEFT JOIN t_eva_recycle_type ON t_product.Frecycle_type = t_eva_recycle_type.Frecycle_id WHERE t_product.Fproduct_id in (41567);
# select Fproduct_id, Fvalid_sku_id, Finvalid_sku_id, Fsku_group, Fversion from t_pdt_sku_map  where Fproduct_id=41567;
# select t_a.Fid as Faid, t_a.Fname as Faname, t_q.Fid as Fqid, t_q.Fname as Fqname  from t_eva_item_base as t_a, t_eva_item_base as t_q  where t_a.Fpid=t_q.Fid and t_a.Flevel=3 and t_q.Flevel=2 and t_a.Fid in (1083,1091,1124,12,13,130,14,15,17,1773,18,2236,2241,2242,36,38,42,471,6047,6116,7630);
'''
outPacket=[{"_body":{"_data":{"attrList":[],"brandId":"2","brandName":"苹果","classId":"1","className":"手机","marketTime":"2017-11-03","osId":"1","osName":"ios系统","productId":"41567","productKeyword":"iPhoneX","productLogo":"41567_20191106154719_960.jpg","productName":"iPhone X","recycleName":"正常回收","recycleType":"3","skuList":[{"answerId":"12","answerName":"大陆国行","questionId":"11","questionName":"购买渠道"},{"answerId":"13","answerName":"香港行货","questionId":"11","questionName":"购买渠道"},{"answerId":"14","answerName":"其他国家地区-无锁版","questionId":"11","questionName":"购买渠道"},{"answerId":"15","answerName":"其他国家地区-有锁版","questionId":"11","questionName":"购买渠道"},{"answerId":"17","answerName":"保修一个月以上","questionId":"16","questionName":"保修期"},{"answerId":"18","answerName":"保修一个月以内或过保","questionId":"16","questionName":"保修期"},{"answerId":"36","answerName":"64GB","questionId":"32","questionName":"存储容量"},{"answerId":"38","answerName":"256GB","questionId":"32","questionName":"存储容量"},{"answerId":"42","answerName":"银色","questionId":"39","questionName":"颜色"},{"answerId":"130","answerName":"全网通","questionId":"122","questionName":"制式"},{"answerId":"471","answerName":"移动联通","questionId":"122","questionName":"制式"},{"answerId":"1083","answerName":"其他型号","questionId":"918","questionName":"型号"},{"answerId":"1091","answerName":"深空灰色","questionId":"39","questionName":"颜色"},{"answerId":"1124","answerName":"国行官换机/  翻机","questionId":"11","questionName":"购买渠道"},{"answerId":"1773","answerName":"A1901","questionId":"918","questionName":"型号"},{"answerId":"2236","answerName":"3GB","questionId":"2232","questionName":"机身内存"},{"answerId":"2241","answerName":"A1865","questionId":"918","questionName":"型号"},{"answerId":"2242","answerName":"A1903","questionId":"918","questionName":"型号"},{"answerId":"6047","answerName":"国行展示机","questionId":"11","questionName":"购买渠道"},{"answerId":"6116","answerName":"国行BS机","questionId":"11","questionName":"购买渠道"},{"answerId":"7630","answerName":"监管机","questionId":"11","questionName":"购买渠道"}]},"_ret":"0","_retcode":"0","_retinfo":"成功"},"_head":{"_callerServiceId":"112005","_groupNo":"1","_interface":"getProductAttribute","_invokeId":"65f14171-5fe3-41a7-b4ac-50b9ac575dc3","_msgType":"response","_remark":"","_timestamps":"1602661304","_version":"0.01"}}]
'''