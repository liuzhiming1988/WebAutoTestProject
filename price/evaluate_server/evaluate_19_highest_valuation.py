#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


'''  估价服务 - 19.获取估价量最高机型以及最高价  http://wiki.huishoubao.com/index.php?s=/138&page_id=9638
    入参：channelId：估价渠道ID，10000031（只有平台时可为空）  |  platformId：平台ID，1-2C、2-2B、3-微回收
        classId：类目ID：1-手机、2-笔记本、3-平板  |  dateTime：时间	‘2020-01-01'
     1.需求：【ID1039692】【外部需求】以旧换新-估价量最高机型
     https://www.tapd.cn/21967291/prong/stories/view/1121967291001039692?url_cache_key=00c85a05fd645c7cee492555eb9e9861&action_entry_type=stories&left_tree=1
     2.需求阐述：取昨天回收 估价量 第一的机型  返回其最高回收价
    SELECT Fproduct_id, COUNT(A.Fproduct_id) AS Total FROM hsblog.t_eva_interface_record_2020_01 A WHERE A.Finterface = 'evaluate'
		AND A.Fcreate_date = '2020-01-02' AND A.Fproduct_id IN (SELECT B.Fproduct_id FROM recycle.t_pdt_class_map B
	WHERE B.Fvalid = 1 AND B.Fclass_id = 1) GROUP BY A.Fproduct_id ORDER BY Total DESC;

	SELECT Fproduct_id, COUNT(A.Fproduct_id) AS Total FROM hsblog.t_eva_interface_record_2020_01 A WHERE A.Finterface = 'evaluate'
		AND A.Fcreate_date = '2020-01-02' GROUP BY A.Fproduct_id ORDER BY Total DESC;  '''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def highest_valuation(platformId, channelId, classId, dateTime):
    param = {"_head":{"_interface":"highest_valuation","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"1525332832","_invokeId":"1111","_callerServiceId":"212013","_groupNo":"1"},"_param":{"platformId":platformId,"channelId":channelId,"classId":classId,"dateTime":dateTime}}
    secret_key = "CtN4bZr7qYyxygRyP5T0VWMEvWhpH0uf"
    callerserviceid = "212013"
    # eva_query 估价查询服务
    url = "http://evaserver.huishoubao.com/eva_query/highest_valuation"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # highest_valuation(platformId="1", channelId="40000001", classId="1", dateTime="2021-04-01" )   # 正常请求
    # highest_valuation(platformId="1", channelId="", classId="1", dateTime="2021-04-01" ) # "_errStr":"获取最高价失败"
    # highest_valuation(platformId="", channelId="40000001", classId="1", dateTime="2021-04-01" )
    # highest_valuation(platformId="1", channelId="10000164", classId="1", dateTime="2020-04-13" )   # 正常请求
    # highest_valuation(platformId="", channelId="40000001", classId="1", dateTime="2020-01-02" )  # 渠道必传，平台ID可不传（始终是2C）

    # 第二次请求，只修改 classId，日期和渠道没变，返回数据是取的redis缓存里的值
    # highest_valuation(platformId="", channelId="40000001", classId="2", dateTime="2020-01-04" )

    # highest_valuation(platformId="", channelId="40000001", classId="1", dateTime="2020-01-05" )  # 昨日估价量为0

    # 昨日估价量为0，返回"maxPrice":"0" 与返回空是一样的
    highest_valuation(platformId="", channelId="40000001", classId="1", dateTime="2020-02-17" )

'''   {"_data":{"_errCode":"0","_errStr":"SUCCEED","_ret":"0","maxPrice":"425500","productId":"54790","productName":"iPhone XS"},"_head":{"_callerServiceId":"212013","_groupNo":"1","_interface":"highest_valuation","_invokeId":"SALESDETECT152533283241636","_msgType":"response","_remark":"","_timestamps":"1581994152","_version":"0.01"}}  '''

