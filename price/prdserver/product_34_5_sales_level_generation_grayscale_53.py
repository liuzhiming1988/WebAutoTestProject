#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 34.2.销售等级的生成 - http://wiki.huishoubao.net/index.php?s=/105&page_id=6051 | sales_level_generation_grayscale ：销售等级生成（53项）
    服务：base_product）
    1. 标准检机况：不需要传channelId  |  2. 大质检机况：需要传channelId（销售价格查询需求中，产品需要的是是2C平台，默认使用 回收宝主站 渠道id

    入参：productId：产品Id （必填） | channelId：渠道Id （必填）；
        aIdList：估价答案项列表（可直接通过 产品服务 - 6.可估价产品产品选项获取（eva_option_get）  取到估价答案项） （必填）；
        cIdList：估价检测细化项列表（必填，可传空） | orderId：订单号（非必填）
        checkAIdList：检测答案项列表,检测,估价答案项只要包含其一就可，即(channelId&&aIdList&&cIdList) or checkAIdList  （非必填）；
        isRecord：是否做记录,1-做记录，0-不做记录，只给估价后台使用，默认记录（非必填）
    出参：productId：产品id | templateId：使用的销售等级模版Id | level：成色等级
        levelName：成色名称 | levelDesc：成色描述 | levelLabel：销售标签
        _retcode：3001：配置问题 根据产品ID获取不到销售等级模版; | 3002：配置问题 该产品已被禁用,无法生成销售等级;
            3003：配置问题 该产品配置的销售等级模版被禁用; | 3004：配置问题 该产品配置的销售等级模版和选项模版的映射被禁用;
            3005：配置问题 产品使用的检测模版未和销售等级模版建立映射; | 3006：配置问题 产品未使用检测模版;
            3008：配置问题 无法生成等级; 1-系统错误和参数错误，0-成功
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def sales_level_generation_grayscale_53(productId, channelId, orderId, aIdList, cIdList ):
    param = {"_head":{"_interface":"sales_level_generation_grayscale","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"","_invokeId":"","_callerServiceId":"112002","_groupNo":"1"},"_param":{"productId":productId,"channelId":channelId,"orderId":orderId, "aIdList":aIdList,"cIdList":cIdList}}

    secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
    callerserviceid = "112002"
    url = "http://prdserver.huishoubao.com/product/sales_level_generation"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    sales_level_generation_grayscale_53(productId="41567", channelId="40000001", orderId='7592570', aIdList=["1078","12","3246","17","20","2171","23","223","38","1091","55","5535","59","63","65","71","6931","73","77","83","1083"], cIdList=[])

    ''' ①正常的回收单，不保价，可以不传orderId； ②B端帮卖单，不保价，可以不传orderId'''
    # sales_level_generation(productId="30748", channelId="40000001", aIdList=["63","77","73","71","83","20"], cIdList=[])    # 2C

    ''' B端帮卖测试  2020.03.06    
    SELECT * FROM t_bangmai_bottom_channel_map WHERE  Fchannel_id= 10000253; 中 Fsale_type：是否是定价平台：1是  '''
    # sales_level_generation(productId="30748", channelId="10000253", aIdList=["63","77","73","71","83","20"], cIdList=[]) # # 2C（B端寄卖平台渠道）帮卖业务渠道，Fsale_type=1
    # sales_level_generation(productId="30748", channelId="10000164", aIdList=["63","77","73","71","83","20"], cIdList=[])    # 2B（回收宝APP测试）非帮卖业务渠道（属正常流程）

''' 
正常的
SELECT * FROM t_bangmai_bottom_channel_map WHERE  Fchannel_id= 40000001 ;
select Fproduct_id, Ftemplate_id, Fvalid, Fuser_name from t_sales_level_template_product  where Fproduct_id='30748';
select Fitem_template_id from t_eva_platform_product where Fvalid=1 and Fproduct_id='30748' and Fplatform_type='1';
select tpc.Fid Fclass_id, tpc.Fname Fclass_name, tslt.Fid Ftemplate_id, tslt.Fname Ftemplate_name, tslt.Fremarks Fremarks, tslt.Fvalid Fvalid, tslmo.Foption_group Foption_group, tslmo.Fvalid Fm_valid, teot.Fid Fo_id, teot.Ftemplate_name Fo_name, teot.Fvalid Fo_valid, teot.Fproduct_item Fproduct_item from t_pdt_class tpc, t_sales_level_template tslt, t_sales_level_map_option tslmo, t_eva_option_template teot where tpc.Fid=tslt.Fclass_id and tslt.Fid=tslmo.Ftemplate_id and tslmo.Foption_template_id=teot.Fid  and tslmo.Ftemplate_id='12' and tslmo.Foption_template_id='127';
select Ftemplate_id, Flevel, Flevel_name, Flevel_desc, Flevel_label, Fbangmai_desc, Fbangmai_visible, Fbangmai_label, Fvalid from t_sales_level_template_level  where Ftemplate_id='12' and Flevel='260';

B端帮卖
SELECT * FROM t_bangmai_bottom_channel_map WHERE  Fchannel_id= 10000253;
BottomChannelMap Rule: channel[10000253] SaleType[1]
select Fproduct_id, Ftemplate_id, Fvalid, Fuser_name from t_sales_level_template_product  where Fproduct_id='30748';
定价渠道，强制转换成2C平台
select Fitem_template_id from t_eva_platform_product where Fvalid=1 and Fproduct_id='30748' and Fplatform_type='1';
select tpc.Fid Fclass_id, tpc.Fname Fclass_name, tslt.Fid Ftemplate_id, tslt.Fname Ftemplate_name, tslt.Fremarks Fremarks, tslt.Fvalid Fvalid, tslmo.Foption_group Foption_group, tslmo.Fvalid Fm_valid, teot.Fid Fo_id, teot.Ftemplate_name Fo_name, teot.Fvalid Fo_valid, teot.Fproduct_item Fproduct_item from t_pdt_class tpc, t_sales_level_template tslt, t_sales_level_map_option tslmo, t_eva_option_template teot where tpc.Fid=tslt.Fclass_id and tslt.Fid=tslmo.Ftemplate_id and tslmo.Foption_template_id=teot.Fid  and tslmo.Ftemplate_id='12' and tslmo.Foption_template_id='127';
select Ftemplate_id, Flevel, Flevel_name, Flevel_desc, Flevel_label, Fbangmai_desc, Fbangmai_visible, Fbangmai_label, Fvalid from t_sales_level_template_level  where Ftemplate_id='12' and Flevel='260';
'''
