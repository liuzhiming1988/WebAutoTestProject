#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 15.根据ID获取估价选项库接口  -  http://wiki.huishoubao.com/web/#/105?page_id=2255

    1-对应服务：server-base_product（base_product）  |  2-对应URL：http://prdserver.huishoubao.com

    入参：id：选项库记录ID（可为空）  |  pid：选项库记录的父级ID（可为空）  |  name：选项库记录的名称（可为空）
        classtype：类目ID（获取选项类，赋值后fpid参数将无效）（可为空）
        pageIndex：分页的页码，从0开始 0,1,2,3,4 （空值：默认0）  |  pageSize：每页的数据量;（空值：默认10）
    出参：id：记录Id  |  name：名称  |  level：记录层级（1：大类；2：问题；3：答案；4：检测细化项）
        pid：记录层级父ID  |  pname：记录层级父名称  |  property：记录每个选项在那个平台显示
        valid：是否有效：1有效；其他无效  |  check：检测细化项（答案项才有）  |  alias：别名（答案项才有
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def get_eva_item_by_id(id,pid,name,classtype):
    param = {"_head":{"_interface":"get_eva_item_by_id","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"1525332832","_invokeId":"SALESDETECT152533283241636","_callerServiceId":"112002","_groupNo":"1"},"_param":{"id":id,"pid":pid,"name":name,"classtype":classtype,"pageIndex":"0","pageSize":"100"}}

    secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
    callerserviceid = "112002"
    url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # get_eva_item_by_id(id='', pid='', name='', classtype='')
    # get_eva_item_by_id(id='', pid='7421', name='', classtype='')
    # get_eva_item_by_id(id='', pid='7421', name='', classtype='2')
    # get_eva_item_by_id(id='', pid='7421', name='', classtype='3')
    # get_eva_item_by_id(id='', pid='3', name='', classtype='1')
    # get_eva_item_by_id(id='', pid='', name='购买渠道', classtype='')
    get_eva_item_by_id(id='', pid='20210326', name='', classtype='')

'''
测试
SELECT t_a.Fid AS Fid, t_a.Fname AS Fname, t_a.Flevel AS Flevel, t_a.Fplatform_type_property AS Fplatform_type_property, t_a.Fvalid AS Fvalid, t_a.Fweight AS Fweight, t_b.Fid AS Fpid, t_b.Fname AS Fpname FROM t_eva_item_base AS t_a LEFT JOIN t_eva_item_base AS t_b ON t_a.Fpid = t_b.Fid where (1=1) AND t_a.Fname like '%购买渠道%' LIMIT 0, 100
'''