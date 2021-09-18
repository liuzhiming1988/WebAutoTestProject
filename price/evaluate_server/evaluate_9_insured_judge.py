#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 估价服务  -  9.保价判断接口  -  http://wiki.huishoubao.net/index.php?s=/138&page_id=2219

    入参：order_id：是，订单Id | productId：是，修改产品后的产品id 优先使用这个 未传递则使用DB中的 | checkItem：否，检测选项（大质检） | user_name：否，调用方名称
    出参：order_id：是，订单Id | insured：是，保价标记，1-保价，0-不保价 | new_product：是，产品Id修改 1修改了 0未修改
        isItemConsistent：否，有checkItem入参时，返回，0：检测选项和估价记录用户选项不一致， 1：检测选项和估计记录用户选项一致
        isItemTemplateConsistent：否，有checkItem入参时返回，0：估价选项模板与现网选项模板不一致， 1：估计记录选项模板与现网模板一致

	1.对应服务 rpc_evaluate_server（服务器应用名：rpc_evaluate_server）
'''

import requests, json, os
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def insured_judge(order_id,productId,checkItem):
    param = {"head":{"interface":"insured_judge","msgtype":"request","remark":"","version":"0.01"},"params":{"order_id":order_id, "productId":productId, "checkItem":checkItem, "user_name":"zhangjinfa@huishoubao.com.cn"}}
    url = "http://evaserver.huishoubao.com/rpc/insured"
    headers = {"Content-Type":"application/json;charset=UTF-8"}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    ''' 不传productId，不传checkItem  pass'''
    # insured_judge(order_id="7598533",productId='',checkItem='')

    ''' 无效订单ID，"retinfo":"初始化订单数据失败"'''
    insured_judge(order_id="20201021001",productId='',checkItem='')
    # insured_judge(order_id="", productId='',checkItem='') # 订单ID为空，"retinfo":"请求参数子接口ID为空"

    ''' 传机型ID'''
    # insured_judge(order_id='7598533', productId='54791',checkItem='') # 传参机型与用户下单机型一致 "insured":"1"
    # insured_judge(order_id='7598533', productId='54790',checkItem='') # 传参机型与用户下单机型不一致 "insured":"0"

    ''' 【估计记录选项模板与现网模板一致】 传机型ID（一致），传checkItem'''
    # insured_judge(order_id='7598533', productId='54791', checkItem='') # 传空
    # insured_judge(order_id='7598533', productId='54791', checkItem=["12","18","38","41","5410","83","78","73","71","62","20","23","55","59","65","223","1078","3246","2171","5535","6931","7641"]) # 检测选项和估价记录用户选项一致，估计记录选项模板与现网模板一致
    # insured_judge(order_id='7598533', productId='54791', checkItem=["24","55","59","62","65","40","68","5530","78","37","82","224","1083","1078","20","3245","2171","17","5535","6930","7642","12"]) # 检测选项和估价记录用户选项不一致，估计记录选项模板与现网模板一致
    # insured_judge(order_id='7598533', productId='54791', checkItem=["24","55","59","62","65","40","68","5530","78","37","82","224"]) # 检测选项和估价记录用户选项不一致（不是当前产品的选项，或者缺失，或者增多），估计记录选项模板与现网模板一致

    ''' 【估计记录选项模板与现网模板不一致】 传机型ID（一致），传checkItem'''
    # 更改前 "itemTemplateId":"102"   更改后 "itemTemplateId":"215"    strRecordItemTemplateId:102 strCurrItemTemplateId:215
    # insured_judge(order_id='7598541', productId='23009', checkItem=["23"]) # "insured":"1","isItemConsistent":"1","isItemTemplateConsistent":"0"
    # insured_judge(order_id='7598541', productId='23009', checkItem='') # "insured":"1"
    # insured_judge(order_id='7598541', productId='23009', checkItem=[]) # "insured":"1"
    # insured_judge(order_id='7598541', productId='23009', checkItem=["24"]) # "insured":"1","isItemConsistent":"0","isItemTemplateConsistent":"0"

    ''' 【估计记录选项模板与现网模板一致】 传机型ID（不一致）（"insured":"0"），传checkItem'''
    # insured_judge(order_id='7598533', productId='54790', checkItem=["62","20","23","55","59","65","223","1078","3246","12","18","38","41","5410","83","78","73","71","2171","5535","6931","7641"]) # 检测选项和估价记录用户选项一致（强行一致的选项），估计记录选项模板与现网模板一致
    # insured_judge(order_id='7598533', productId='54790', checkItem=["23","59","62","56","65","71","42","73","3243","1853","14","7641","6930","82","21","5534","224","18","1083","1077","2171","3245"]) # 检测选项和估价记录用户选项不一致，估计记录选项模板与现网模板一致

    ''' 【估计记录选项模板与现网模板不一致】 传机型ID（不一致），传checkItem'''
    # 原机型 23009 传参机型 23007   strRecordItemTemplateId:102 strCurrItemTemplateId:215
    # insured_judge(order_id='7598541', productId='23007', checkItem=["23"]) # "insured":"0","isItemConsistent":"1","isItemTemplateConsistent":"0"

    # insured_judge(order_id='7605471', productId='64495', checkItem=["13","7823","3247","18","2491","83","63","73","1853","3243","23","59","55","65","7641","6931","21","5535","223","1078","3246","2171"]) # "insured":"0","isItemConsistent":"1","isItemTemplateConsistent":"0"


'''
1. 传机型ID，传checkItem 
select Fstandard_price, Fproduct_item, Fshow_item, Fbasic_price, Frick_guarantee, Fprice_control, Fneed_evaluate, Fproduct_id, Fitem_param_id, Fos_type, Fvalid, Fuse_standard_eva, Fitem_template_id, Fsku_map from t_eva_platform_product where Fproduct_id=54791 and Fplatform_type=1 and Fdelete_flag = 1;
估价2.0平台产品表  返回 `Fitem_param_id` = '选项参数组合ID，关联表：t_eva_item_params的Fid字段'  36196

select Fevaluate_item from t_eva_item_params  where Fid = 36196;
估价2.0产品选项参数表  返回  `Fevaluate_item` = '产品估价选项，配比权重，存json格式'

strUserItem:12,18,20,23,38,41,55,59,62,65,71,73,78,83,223,1078,2171,3246,5410,5535,6931,7641,
strCheckItem:12,18,20,23,38,41,55,59,62,65,71,73,78,83,223,1078,2171,3246,5410,5535,6931,7641,
strRecordItemTemplateId:204 strCurrItemTemplateId:204

outdata={"body":{"data":{"additionVersion":"0","channelID":"40000001","insured":"1","isItemConsistent":"1","isItemTemplateConsistent":"1","new_product":"0","operatorVersion":"0","orderTime":"2020-10-11 14:37:14","order_id":"7598533","pid":"1001","platformID":"1","platformVersion":"489","productId":"54791","propertyFlag":"0","tagId":"1","unifiedVersion":"65"},"ret":"0","retcode":"0","retinfo":"成功"},"head":{"interface":"insured_judge","msgtype":"response","remark":"","version":"0.01"}}
'''