#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 估价服务-8-根据时间估价接口 - http://wiki.huishoubao.com/index.php?s=/138&page_id=2218
	1.对应服务 rpc_evaluate_server（服务器应用名：rpc_evaluate_server）
	入参：select：用户选项，json数组的字符串格式（必填）  |  time：估价时间（必填）  |  pid/channelid：pid或渠道id，只需传递一个（必填）  |  productid：产品ID（必填）
	    platformSign：估算当时子平台产品价格，不传默认为1，填1或0（非必填）  |  unifiedSign：估算当时统一估价产品价格 不传默认为0 填1或0（非必填）
'''

import requests, json, os, time as t
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def eva_time(select,time,productid,pid):
    param = {"head":{ "interface":"eva_time", "msgtype":"request", "remark":"", "version":"0.01" }, "params":{ "ip":"127.0.0.1", "cookies":"test", "userid":"1", "select":select, "time":time, "productid":productid, "pid":pid}}
    # print(json.dumps(param))
    url = "http://evaserver.huishoubao.com/rpc/evaluate"
    headers = {"Content-Type":"application/json;charset=UTF-8"}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    eva_time(select=["23"], time=t.strftime('%Y-%m-%d %H:%M:%S',t.localtime()), productid='4006', pid='1001')

'''
测试
select Fversion from t_eva_conf_effective_schedule where Fid=(select max(Fid) from t_eva_conf_effective_schedule where Ftype=1 and Fproduct_id=4006 and Fvalid_time<='2020-12-01 15:30:21' and (Finvalid_time >'2020-12-01 15:30:21' or Finvalid_time is NULL))
select Fversion from t_eva_conf_effective_schedule where Fid=(select max(Fid) from t_eva_conf_effective_schedule where Ftype=2 and Fproduct_id=4006 and Fplatform_type=1 and Fvalid_time<='2020-12-01 15:30:21' and (Finvalid_time >'2020-12-01 15:30:21' or Finvalid_time is NULL))
select Fversion from t_eva_conf_effective_schedule where Fid=(select max(Fid) from t_eva_conf_effective_schedule where Ftype=3 and Fproduct_id=4006 and Fchannel_id=40000001 and Fvalid_time<='2020-12-01 15:30:21' and (Finvalid_time >'2020-12-01 15:30:21' or Finvalid_time is NULL))
select Fversion from t_eva_conf_effective_schedule where Fid=(select max(Fid) from t_eva_conf_effective_schedule where Ftype=4 and Fchannel_id=40000001 and Fvalid_time<='2020-12-01 15:30:21' and (Finvalid_time >'2020-12-01 15:30:21' or Finvalid_time is NULL))
select Fevaluate_item, Fstandard_price, Fmin_price, Fitem_group, Fitem_add_sub, Falgorithm_order, Fall_combination_price from t_eva_standard_pditems_history  where Fproduct_id = 4006 and Fversion = 13 limit 1

整机项: 500*100/100 = 500
系数特殊规则:500 = 500
选项分组命中等级:100 lType:1 lValue:100 uType:1 uValue:100
选项分组下限百分比:(500*100)/100=500
选项分组上限百分比:(500*100)/100=500
选项分组在上下限范围内, 无需校正
先计算选项分组再计算差值算法 差值:(500+500*0/100+0)*100/100 = 500

select Fchannel_id, Faddition, Fversion, Fdelete_flag, Foperator_name, Faddition_range from t_eva_channel_addition_record  where Fchannel_id = 40000001 and Fversion=24 and Fdelete_flag=1 limit 1
select Fevaluate_item, Fstandard_price, Fmin_price, Fitem_group, Fitem_add_sub, Falgorithm_order, Fall_combination_price from t_eva_standard_pditems_history  where Fproduct_id = 4006 and Fversion = 1 limit 1
select Fevaluate_item, Fstandard_price, Fmin_price, Fitem_group, Fitem_add_sub, Falgorithm_order, Fall_combination_price from t_eva_pditems_history  where Fplatform_type = 1 and Fproduct_id = 4006 and Fversion = 88 limit 1

整机项: 500*100/100 = 500
系数特殊规则:500 = 500
选项分组命中等级:100 lType:1 lValue:100 uType:1 uValue:100
选项分组下限百分比:(500*100)/100=500
选项分组上限百分比:(500*100)/100=500
选项分组在上下限范围内, 无需校正
先计算选项分组再计算差值算法 差值:(500+500*0/100+0)*100/100 = 500

select Fchannel_id, Faddition, Fversion, Fdelete_flag, Foperator_name, Faddition_range from t_eva_channel_addition_record  where Fchannel_id = 40000001 and Fversion=24 and Fdelete_flag=1 limit 1
'''