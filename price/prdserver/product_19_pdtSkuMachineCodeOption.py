#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 19.根据产品id和sku机器码获取产品sku信息 - http://wiki.huishoubao.com/index.php?s=/105&page_id=2535
    入参：productId：回收宝产品id  |  skuCode：sku机器码
    1-对应服务：server-base_product（base_product）  |  2-对应URL：http://prdserver.huishoubao.com

    估价后台：新产品库 - SPU映射管理模块
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def pdtSkuMachineCodeOption(productId, skuCode):
    param = {"_head":{ "_interface":"pdtSkuMachineCodeOption", "_msgType":"request", "_remark":"", "_version":"0.01", "_timestamps":"123", "_invokeId":"111", "_callerServiceId":"112002", "_groupNo":"1" }, "_param":{ "productId":productId, "skuCode":skuCode}}

    secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
    callerserviceid = "112002"
    url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # pdtSkuMachineCodeOption(productId='',skuCode='')
    # pdtSkuMachineCodeOption(productId='41567',skuCode='')
    # pdtSkuMachineCodeOption(productId='',skuCode='iPhone_x_001')
    # pdtSkuMachineCodeOption(productId='63330',skuCode='iPhone_x_001')
    # pdtSkuMachineCodeOption(productId='41567',skuCode='1111111111')
    # pdtSkuMachineCodeOption(productId='41567',skuCode='iPhone_x_001')
    # pdtSkuMachineCodeOption(productId='41567',skuCode='iPhone_x_002')
    pdtSkuMachineCodeOption(productId='41567',skuCode='iPhone_x_003')

'''
测试
select tp.Fproduct_id as Fproduct_id, tp.Fproduct_name as Fproduct_name, tp.Fos_type as Fos_type,  tp.Fpic_id as Fpic_id, tpc.Fid as Fclass_id, tpc.Fname as Fclass_name, tpb.Fid as Fbrand_id,  tpb.Fname as Fbrand_name, tpsmcm.Fsku_id as Fsku_id  from t_product as tp, t_pdt_brand as tpb, t_pdt_brand_map as tpbm, t_pdt_class as tpc,  t_pdt_class_map as tpcm, t_pdt_sku_machine_code_map as tpsmcm  where tp.Fproduct_id=tpbm.Fproduct_id and tpbm.Fbrand_id=tpb.Fid and tp.Fproduct_id=tpcm.Fproduct_id  and tpcm.Fclass_id=tpc.Fid and tp.Fproduct_id=tpsmcm.Fproduct_id and tp.Fis_two in (0, 2)  and tp.Fis_upper=1 and Frecycle_type=3 and tpsmcm.Fdelete=1  and TRIM(tpsmcm.Fsku_machine_code)=TRIM('iPhone_x_003') and tpsmcm.Fproduct_id = 41567;

select t_a.Fid as Faid, t_a.Fname as Faname, t_q.Fid as Fqid, t_q.Fname as Fqname  from t_eva_item_base as t_a, t_eva_item_base as t_q  where t_a.Fpid=t_q.Fid and t_a.Flevel=3 and t_q.Flevel=2 and t_a.Fid in (1091,1124,18,2236,2241,38,471);
'''