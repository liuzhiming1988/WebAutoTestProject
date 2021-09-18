#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 7.获取产品列表（包括不可估价）-  http://wiki.huishoubao.com/index.php?s=/105&page_id=1596  |  base_product
    入参：fkeyword：关键字（可传递空值） |  fclassid：类目id（可传递空值），多个类目用#号分割，1#2#3  |  fbrandid：2.0品牌id （可传递空值）
        fbrandidV1：1.0品牌id （可传递空值，当fbrandid空值，fbrandidV1有值时，才有效）
        fpageindex：起始页面（从0开始） | fpagesize：页面最大数量（最大限额：500）
        frecycle_type_id：回收类型id（空值返回所有类型数据）1-公益回收，2-山寨机，3-正常回收
        fvalid：产品状态（1-上架； 2-下架，空值返回两个状态数据，（数据是产品库的上下架，不是估价的上下架）
        orderList：排序规则，1-classAsc按类目升序，2-classDesc按类目降序，3-productAsc按产品Id升序，4-productDesc按产品ID降序  |  ip：用户公网访问IP
    出参：fproduct_desc：产品描述  |  fbrand_id：品牌id  |  fbrand_name：品牌名称  |  fclass_id：类目id  |  fclass_name：类目名称
        fkey_word：关键词  |  fos_type_id：系统id  |  fos_type_name：系统名称  |  fproduct_id：产品id  |  fproduct_logo：图片名称
        fproduct_name：产品名称  |  frecycle_type_id：回收类型id  |  frecycle_type_name：回收类型
        fvalid：是否有效（1-有效，2-无效 ，产品库上下架）  |  fmax_price：最高价（分）（当无最高价时，为0） |  sum_num：搜索数量

    逻辑：elasticsearch：（先） ——>  MySql（后） |  elasticsearch：能查询，查询有结果，直接返回  |  elasticsearc：查询无结果，再从MySql查询，将查询结果返回

    select * from t_product as tp  left join t_pdt_class as tpc on tpc.Fid = tp.Fclass_id
        left join t_pdt_brand as tpb on tpb.Fid = tp.Fbrand_id  left join t_eva_os_type as teot on tp.Fos_type = teot.Fos_id
        left join t_eva_recycle_type as tert on tp.Frecycle_type = tert.Frecycle_id  where (tp.Fis_two=0 OR tp.Fis_two=2) and tp.Fbrand_id = 2
    and tp.Fis_upper = 1 and tp.Frecycle_type = 3 and tp.Fclass_id IN (1,2)  order by tp.Fproduct_id desc limit 0,50
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def product_con_get(fkeyword,fbrandid,fclassid,fvalid,fpageindex,fpagesize,frecycle_type_id,orderList):
    param = {"_head":{"_interface":"product_con_get","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"123","_invokeId":"111","_callerServiceId":"112002","_groupNo":"1"},"_param":{"fkeyword":fkeyword,"fbrandid":fbrandid,"fbrandidV1":"","fclassid":fclassid,"fvalid":fvalid,"fpageindex":fpageindex,"fpagesize":fpagesize,"frecycle_type_id":frecycle_type_id,"orderList":orderList,"ip":"127.0.0.1"}}

    secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
    callerserviceid = "112002"
    url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # product_con_get(fkeyword='',fbrandid='2',fclassid='1#2',fvalid='1',fpageindex='0',fpagesize='10',frecycle_type_id='3',orderList='4')
    # product_con_get(fkeyword='苹果',fbrandid='2',fclassid='1#2',fvalid='1',fpageindex='0',fpagesize='10',frecycle_type_id='3',orderList='4')
    # product_con_get(fkeyword='',fbrandid='',fclassid='1#2#10',fvalid='1',fpageindex='0',fpagesize='10',frecycle_type_id='1',orderList='4')
    # product_con_get(fkeyword='',fbrandid='',fclassid='1#2#10',fvalid='1',fpageindex='0',fpagesize='10',frecycle_type_id='2',orderList='4')
    product_con_get(fkeyword='华为',fbrandid='',fclassid='1#2#10',fvalid='1',fpageindex='0',fpagesize='10',frecycle_type_id='3',orderList='4')

'''
【原SQL】
select tp.Fproduct_id, tp.Fproduct_name, tp.Fproduct_desc, tp.Fpic_id, tp.Fkey_word, tp.Frecycle_type, tp.Fos_type, tpc.Fid as Fclass_id, tpc.Fname as Fclass_name, tpb.Fid as Fbrand_id, tpb.Fname as Fbrand_name, tp.Fis_upper, tert.Frecycle_type as Frecycle_name, teot.Fos_name from t_product as tp  left join t_pdt_class as tpc on tpc.Fid = tp.Fclass_id  left join t_pdt_brand as tpb on tpb.Fid = tp.Fbrand_id  left join t_eva_os_type as teot on tp.Fos_type = teot.Fos_id  left join t_eva_recycle_type as tert on tp.Frecycle_type = tert.Frecycle_id where (tp.Fis_two=0 OR tp.Fis_two=2) and tp.Fbrand_id = 2 and tp.Fis_upper = 1 and tp.Frecycle_type = 3 and tp.Fclass_id IN (1,2)  order by tp.Fproduct_id desc limit 0,10;

【发版后】
select SQL_CALC_FOUND_ROWS tp.Fproduct_id, tp.Fproduct_name, tp.Fproduct_desc, tp.Fpic_id, tp.Fkey_word, tp.Frecycle_type, tp.Fos_type, tpc.Fid as Fclass_id, tpc.Fname as Fclass_name, tpb.Fid as Fbrand_id, tpb.Fname as Fbrand_name, tp.Fis_upper, tert.Frecycle_type as Frecycle_name, teot.Fos_name from t_product as tp  left join t_pdt_class as tpc on tpc.Fid = tp.Fclass_id  left join t_pdt_brand as tpb on tpb.Fid = tp.Fbrand_id  left join t_eva_os_type as teot on tp.Fos_type = teot.Fos_id  left join t_eva_recycle_type as tert on tp.Frecycle_type = tert.Frecycle_id where (tp.Fis_two=0 OR tp.Fis_two=2) and tp.Fbrand_id = 2 and tp.Fis_upper = 1 and tp.Frecycle_type = 3 and tp.Fclass_id IN (1,2)  order by tp.Fproduct_id desc limit 0,10;
SELECT FOUND_ROWS()

【SQL_CALC_FOUND_ROWS 简述】
在很多分页的程序中都这样写:
    # 查出符合条件的记录总数   SELECT COUNT(*) from [table] WHERE  ......;
    # 查询当页要显示的数据    SELECT * FROM [table]  WHERE ...... limit M,N;
但是从Mysql4.0.0开始，我们可以选择使用另外一个方式：
    SELECT SQL_CALC_FOUND_ROWS * FROM [table] WHERE ......  limit M, N;
    SELECT FOUND_ROWS();
    # SQL_CALC_FOUND_ROWS 告诉MySQL将sql所处理的行数记录下来
    # FOUND_ROWS() 则取到了这个纪录
虽然也是两个语句，但是只执行了一次主查询，所以效率比原来要高很多。

【ES】
20210202-160813-211|REPORT|140530852890880||1|1612253293|EvaSBaseProductSys|test-price-server-01|PriceElasticSearch|EVA_ES_HOST:9200|search|0|93.311
20210202-160813-211|INFO|140530852890880||8575|127.0.0.1|base_product|../../../implements/elasticsearch/elasticsearch_wrapper.cpp|search|754|Url:EVA_ES_HOST:9200/eva_product/_doc/_search Request:{"_source":["Fproduct_id","Fproduct_name","Fbrand_id","Fbrand_name","Fclass_id","Fclass_name","Fpic_id","Frecycle_type","Frecycle_name","Fkey_word","Fpic_id","Fis_upper","Fos_type","Fos_name","Fproduct_desc"],"from":0,"query":{"bool":{"must":[{"match":{"Fis_upper":"1"}},{"match":{"Fbrand_id":"2"}},{"match":{"Frecycle_type":"3"}},{"terms":{"Fclass_id":["1","2"]}}]}},"size":10,"sort":[{"Fproduct_id":{"order":"desc"}}],"track_total_hits":true} RetCode:0
20210202-160813-212|DEBUG|140530852890880||8575|127.0.0.1|base_product|src/logicmodel/product_con_get_infologic.cpp|getProductWithEs|438|search success
20210202-160813-212|DEBUG|140530852890880||8575|127.0.0.1|base_product|src/logicmodel/product_con_get_infologic.cpp|getProductWithEs|447|jResult is array
20210202-160813-212|DEBUG|140530852890880||8575|127.0.0.1|base_product|src/logicmodel/product_con_get_infologic.cpp|getProductWithEs|457|jResulLen > 0
'''