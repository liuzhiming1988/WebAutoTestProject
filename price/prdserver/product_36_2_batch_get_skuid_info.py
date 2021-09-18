#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 36.2.批量skuId查询机型sku组合  -  http://wiki.huishoubao.com/web/#/105?page_id=13242
    1.对应服务：server-base_product（base_product）

    入参：skuidList：skuId
    出参：skuidInfo：skuid信息 | productId：产品id | productName：产品名称 | pic：产品图片 | productValid：产品有效状态（1-有效，0-无效） | classId：类目ID
        className：类目名称 | brandId：品牌ID | brandName：品牌名称 | itemList：sku选项信息 | aInfo：答案项信息 | aId：答案项id
        aName：答案项名称 | qId：问题项id | qName：问题项名称
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def batch_get_skuid_info(skuidList):
    param = {"_head":{"_interface":"batch_get_skuid_info","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"123","_invokeId":"111","_callerServiceId":"112002","_groupNo":"1"},"_param":{"skuidList":skuidList}}
    secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
    callerserviceid = "112002"
    url = "http://prdserver.huishoubao.com/product/batch_get_skuid_info"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    ''' 1. 传参空数组 or 数组里面传空字符串；  返回：{"skuidInfo":{}}  '''
    # batch_get_skuid_info(skuidList=[])
    # batch_get_skuid_info(skuidList=[''])

    ''' 2.1. spu_id 存在，无sku配置（t_pdt_sku_map 表存在记录）；  返回：将spu信息作为结果返回
        2.2. spu_id 存在，无sku配置（t_pdt_sku_map 表不存在记录）；  返回：将spu信息作为结果返回 '''
    # batch_get_skuid_info(skuidList=["41636"])
    # batch_get_skuid_info(skuidList=["64525"])
    # batch_get_skuid_info(skuidList=["63862"]) # 删除spu在t_pdt_sku_map表的记录

    ''' 3. spu_id 存在，无sku配置（t_pdt_sku_map 表不存在记录），传参带"_"；  返回：{"skuidInfo":{}} '''
    # batch_get_skuid_info(skuidList=["63862_"])
    # batch_get_skuid_info(skuidList=["63862-"])
    # batch_get_skuid_info(skuidList=["41567____56998"]) # 会正常返回
    # batch_get_skuid_info(skuidList=["41567--56998"])
    # batch_get_skuid_info(skuidList=["41567_-56998"])
    # batch_get_skuid_info(skuidList=["41567+56998"])

    ''' 4. spu_id 不存在； 返回：{"skuidInfo":{}}'''
    # batch_get_skuid_info(skuidList=["202012191120"])
    # batch_get_skuid_info(skuidList=["a41567"])
    # batch_get_skuid_info(skuidList=["_41567"])

    ''' 5. spu_id 存在，不存在对应的skuid； 原返回：spu信息；  返回：{"skuidInfo":{}} '''
    # batch_get_skuid_info(skuidList=["63862_20201218"])

    ''' 6. 传参：spu和sku信息均不存在；  返回：{"skuidInfo":{}} '''
    # batch_get_skuid_info(skuidList=["20201218_20201218"])

    ''' 7. 传参多个，"41567_56998" - 正确，"63862" - 没有配置sku，"-20201219" - spu不存在；  返回：正确的会返回 '''
    # batch_get_skuid_info(skuidList=["63862","41567_56998","-20201219"])

    ''' 8.1. 正常数据，单个skuid； 返回：正常返回
        8.2. 正常数据，多个skuid； 返回：正常返回 '''
    # batch_get_skuid_info(skuidList=["41567_56998"])
    # batch_get_skuid_info(skuidList=["41567_56998", "41567_54568", "41567_57097", "41567_57096", "64000_221521", "64000_239560"])

    ''' 9.1. SPU被禁用（"productValid":"0"）'''
    # 禁用机型，有配置sku（t_pdt_sku_map 表存在记录）； 返回：{"skuidInfo":{}}
    # batch_get_skuid_info(skuidList=["31238"])

    # 禁用机型，有配置sku，传了sku（t_pdt_sku_map 表存在记录）； 返回：正常返回（跟机型状态无关，但会返回机型的禁用状态 "productValid":"0"）
    # batch_get_skuid_info(skuidList=["31238_305143"])

    # 禁用机型，有配置sku，传了多个sku（t_pdt_sku_map 表存在记录）； 返回：正常返回（跟机型状态无关，但会返回机型的禁用状态 "productValid":"0"）
    # batch_get_skuid_info(skuidList=["31238_305143","31238_64632"])

    # 禁用机型，无配置sku（t_pdt_sku_map 表不存在记录）；  返回：正常返回（跟机型状态无关，但会返回机型的禁用状态 "productValid":"0"）
    # batch_get_skuid_info(skuidList=["41636"])

    ''' 10.1. spu启用，skuid禁用；  返回：{"skuidInfo":{}}
        10.2. ①spu启用，skuid禁用；②spu启用，skuid启用 '''
    # spu启用，skuid禁用
    # batch_get_skuid_info(skuidList=["64000_239554", "64000_239559", "64000_221512"])

    # ①spu启用，skuid禁用；②spu启用，skuid启用
    # batch_get_skuid_info(skuidList=["64000_239554", "64000_239558"])

    # ①spu启用，skuid禁用；②spu禁用，skuid启用； 返回：正常返回（跟机型状态无关，但会返回机型的禁用状态 "productValid":"0"）
    # batch_get_skuid_info(skuidList=["64000_239554", "31238_305143"])

    ''' 11. 混合场景
        1：空； |  2：仅spu，启用（map表有记录）【返回】； |  3:仅spu，启用（map表无记录）【返回】； |  4：仅spuid，禁用【返回】；
        5：spu启用，spu和sku相同； |  6：spu启用，仅带_，不带具体sku  |  7：spu启用，sku启用【返回】； |  8：spu启用，sku禁用；
        9：spu禁用，sku启用【返回】； |  10：spu禁用，sku禁用
        11：不存在的spu； |  12：不存在的spu和sku  '''
    batch_get_skuid_info(skuidList=["",  "64525",  "63862",  "42066",
                                    "54791_54791",  "38201_",  "41567_56998",  "38200_54205",
                                    "31238_305143",  "31238_305144",
                                    "-20201219","20201219","-20201219_20201219","20201219_20201219"])

'''
测试
SELECT tp.Fproduct_id, tp.Fproduct_name, tp.Fproduct_desc, tp.Fpic_id, tp.Fis_upper, tp.Fmodel, tp.Fkey_word, tp.Fos_type, tp.Fclass_id, tp.Fbrand_id, tpc.Fname AS Fclass_name, tpb.Fname AS Fbrand_name FROM t_product tp LEFT JOIN t_pdt_class tpc ON tpc.Fid = tp.Fclass_id LEFT JOIN t_pdt_brand tpb ON tpb.Fid = tp.Fbrand_id WHERE tp.Fproduct_id IN (63862);
select Fproduct_id, Fvalid_sku_id, Finvalid_sku_id, Fsku_group, Fversion from t_pdt_sku_map  where Fproduct_id in(63862);

SELECT tp.Fproduct_id, tp.Fproduct_name, tp.Fproduct_desc, tp.Fpic_id, tp.Fis_upper, tp.Fmodel, tp.Fkey_word, tp.Fos_type, tp.Fclass_id, tp.Fbrand_id, tpc.Fname AS Fclass_name, tpb.Fname AS Fbrand_name FROM t_product tp LEFT JOIN t_pdt_class tpc ON tpc.Fid = tp.Fclass_id LEFT JOIN t_pdt_brand tpb ON tpb.Fid = tp.Fbrand_id WHERE tp.Fproduct_id IN (41567);
select Fproduct_id, Fvalid_sku_id, Finvalid_sku_id, Fsku_group, Fversion from t_pdt_sku_map  where Fproduct_id in(41567);
select Fid, Faid_list from t_pdt_sku  where Fid in (56998);
select t_a.Fid as Faid, t_a.Fname as Faname, t_q.Fid as Fqid, t_q.Fname as Fqname  from t_eva_item_base as t_a, t_eva_item_base as t_q  where t_a.Fpid=t_q.Fid and t_a.Flevel=3 and t_q.Flevel=2 and t_a.Fid in (1083,1091,1124,130,17,2236,36);
'''