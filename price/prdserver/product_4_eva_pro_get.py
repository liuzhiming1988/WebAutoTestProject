#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 4-获取产品列表（可估价，不包括下架产品） -  http://wiki.huishoubao.com/index.php?s=/105&page_id=1593
    1-产品中心服务：product_center
    2-对应服务：server-base_product（base_product）
    3-对应URL http://prdserver.huishoubao.com

    迭代场景：【频率限制】1.通用接口频率限制 2.获取产品接口（两个）接入通用限频
    select a.Fp_id, b.Ftag_id, b.Fchannel_id, c.Fchannel_name, c.Fchannel_flag from t_maptag a
		left join t_tag b on b.Ftag_id = a.Ftag_id  
		left join t_channel c on c.Fchannel_id = b.Fchannel_id  
	 where a.Fp_id = 1001 limit 1;

	recycletype：根据回收类型查询,3:正常回收 2:山寨机 1:公益回收,可为空值,表示不根据该字段值过滤
    excludeClassId：排除的类目 1手机 2笔记本 3平板 传多个时可用#分割，如:2#3
    brandid：品牌id； classid：类目id
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print
from price.dingdingTalk_push_demo import dingdingTalk_push_run

def eva_pro_get(pageindex, pagesize, channel_id, pid, keyword, brandid, classid, recycletype):
    param = { "_head":{ "_interface":"eva_pro_get", "_msgType":"request", "_remark":"hello", "_version":"0.01", "_timestamps":"123", "_invokeId":"111", "_callerServiceId":"112002", "_groupNo":"1" }, "_param":{ "pageindex":pageindex, "pagesize":pagesize, "channel_id":channel_id, "pid":pid, "keyword":keyword, "brandid":brandid, "brandidV1":"", "classid":classid, "orderField":"1", "orderType":"1", "recycletype":recycletype, "os":"","ip":"127.0.0.1"}}

    secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
    callerserviceid = "112002"
    url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # eva_pro_get(pageindex='1', pagesize='15', channel_id='', keyword='', pid='', brandid='', classid='', recycletype='')
    # eva_pro_get(pageindex='0', pagesize='60', channel_id='10000837', keyword='iphone 12', pid='', brandid='', classid='1', recycletype='3')
    # eva_pro_get(pageindex='1', pagesize='15', channel_id='', keyword='iPhone', pid='1001', brandid='', classid='', recycletype='')
    # eva_pro_get(pageindex='1', pagesize='15', channel_id='', keyword='华为', pid='1001', brandid='', classid='', recycletype='')
    # eva_pro_get(pageindex='2', pagesize='30', channel_id='', keyword='oppo', pid='1001', brandid='', classid='', recycletype='')
    # eva_pro_get(pageindex='0', pagesize='20', channel_id='10000254', keyword='', pid='', brandid='1', classid='1', recycletype='3')
    # eva_pro_get(pageindex='0', pagesize='20', channel_id='10000254', keyword='', pid='', brandid='2', classid='1', recycletype='3')
    # eva_pro_get(pageindex='0', pagesize='20', channel_id='10000164', keyword='', pid='1405', brandid='1', classid='1', recycletype='3')
    eva_pro_get(pageindex='0', pagesize='20', channel_id='', keyword='65980', pid='1001', brandid='', classid='1', recycletype='3')

{ "_head":{ "_interface":"eva_pro_get", "_msgType":"request", "_remark":"hello", "_version":"0.01", "_timestamps":"123", "_invokeId":"111", "_callerServiceId":"110003", "_groupNo":"1" }, "_param":{ "pageindex":"0", "pagesize":"20", "channel_id":"10000254", "pid":"", "keyword":"", "brandid":"1", "brandidV1":"", "classid":"1", "recycletype":"3", "os":"","ip":"127.0.0.1"}}