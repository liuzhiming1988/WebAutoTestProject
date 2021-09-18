#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 20.根据机器品牌码和spu机器码获取产品信息 - http://wiki.huishoubao.com/index.php?s=/105&page_id=2555
    入参：brandCode：品牌机器码，例如:”HUAWEI”  |  spuCode：spu机型码，例如:”HWI-TL00"
    1. 对应服务：server-base_product（base_product）  |  2. 对应URL：http://prdserver.huishoubao.com
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def spu_code_handler(brandCode, spuCode):
    param = {"_head":{"_interface":"spu_code_handler","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"1592207582","_invokeId":"111","_callerServiceId":"112002","_groupNo":"1"},"_param":{"cmd":"search_product_info","pageIndex":"0","pageSize":"10","brandCode":brandCode,"spuCode":spuCode}}

    secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
    callerserviceid = "112002"
    url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # spu_code_handler(brandCode='',spuCode='')
    # spu_code_handler(brandCode='APPLE',spuCode='')
    # spu_code_handler(brandCode='',spuCode='vivoiqoo3')
    # spu_code_handler(brandCode='',spuCode='1111111111111')
    # spu_code_handler(brandCode='APPLE',spuCode='vivoiqoo3')

    ''' 不可估价的情况下，查不到信息'''
    # spu_code_handler(brandCode='APPLE',spuCode='iPhone11,6')
    # 3130 vivo Y67
    # spu_code_handler(brandCode='VIVO',spuCode='Y67A')
    # spu_code_handler(brandCode='',spuCode='Y67')
    # spu_code_handler(brandCode='',spuCode='vivo Y67')
    # 46517 vivo X21
    # spu_code_handler(brandCode='VIVO',spuCode='vivo X21')
    # spu_code_handler(brandCode='VIVO',spuCode='vivo vivo X21UD A')

    # spu_code_handler(brandCode='',spuCode='V1916A')
    # spu_code_handler(brandCode='',spuCode='V1950A')
    # spu_code_handler(brandCode='',spuCode='PD1728')
    # spu_code_handler(brandCode='',spuCode='y67')
    # spu_code_handler(brandCode='',spuCode='X50')
    # spu_code_handler(brandCode='',spuCode='X27')
    # spu_code_handler(brandCode='',spuCode='vivoiqoo3')

    # spu_code_handler(brandCode='',spuCode='honor荣耀 50')
    spu_code_handler(brandCode='HONOR',spuCode='honor荣耀50')
    # spu_code_handler(brandCode='',spuCode='honor荣耀 50 Pro')
    # spu_code_handler(brandCode='Huawei',spuCode='honor荣耀50pro')


# select tpb.Fid as Fbrand_id, tpb.Fname as Fbrand_name, tpc.Fid as Fclass_id, tpc.Fname as Fclass_name, tp.Fproduct_name as Fproduct_name, tp.Fproduct_id as Fproduct_id, tp.Fpic_id as Fpic_id from t_pdt_spu_machine_code_map tpsmcm, t_product tp, t_pdt_class tpc, t_pdt_brand tpb where tpsmcm.Fproduct_id=tp.Fproduct_id and tp.Fclass_id=tpc.Fid and tp.Fbrand_id=tpb.Fid and tpsmcm.Fvalid=1 and tpb.Fvalid=1 and tp.Fis_upper=1 and tp.Fis_two in (0, 2) and tpb.Fbrand_machine_code like '%"APPLE"%' and tpsmcm.Fspu_nums like '%"iPhone11,6"%' limit 0,10

'''
机型：vivo Y67 
brandCode='VIVO'
spuCode='Y67A'      
Y67A | vivo Y67L | vivo Y67A | vivo Y67    任取其一均可

机型：vivo X21
brandCode='VIVO'
spuCode='vivo X21'
vivo X21UD | vivo vivo X21UD A | vivo vivo X21UD | vivo X21UD A | vivo X21A | vivo X21 | X21A    任取其一均可
'''