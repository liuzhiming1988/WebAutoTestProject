#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 40.闲鱼帮买用户估价接口 - http://wiki.huishoubao.com/index.php?s=/105&page_id=6811
    1. 对应服务：server-bangmai_pro_eva（服务器应用名：server-bangmai_pro_eva）

    入参：pid：必填，pid,不为空 | channelId：必填，渠道id,不为空 | productId：必填，产品id，要查询产品选项的产品ID | select：必填，用户选择的估价选项
        qIdL：必填，问题项id | aId：必填，答案项id | userId：非必填，用户id
    出参：evaluateId：估价唯一id | hsbPrice	：回收价价格，单位:分 | highestPrice：帮买最高价，单位:分 | dropInPrice：预计降价幅度，单位:分
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def xy_evaluate(channelId, pid, productId, select):
    param = {"_head":{"_callerServiceId":"110001","_groupNo":"1","_interface":"xy_evaluate","_invokeId":"11111","_msgType":"request","_remark":"","_timestamps":"1602671865","_version":"0.01"},"_param":{ "channelId":channelId, "pid":pid,"productId":productId, "select":select }}
    secret_key = "c36691ced620bf82ad3fc4642f8a6427"
    callerserviceid = "110001"
    url = "http://bmserver.huishoubao.com/bangmai/xy_evaluate"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # xy_evaluate(channelId='10000207', pid='1533', productId='41567', select=[{"aId":"34","qId":"32"},{"aId":"1891","qId":"918"},{"aId":"246","qId":"999999"}])
    # xy_evaluate(channelId='10000207', pid='1533', productId='30833', select=[])
    # xy_evaluate(channelId='10000207', pid='1533', productId='30833', select=[{"aId":"34","qId":"32"},{"aId":"1891","qId":"918"}])
    # xy_evaluate(channelId='10000207', pid='1533', productId='30833', select=[{"aId":"34","qId":"32"},{"aId":"1891","qId":"918"},{"aId":"246","qId":"999999"}])
    # xy_evaluate(channelId='10000207', pid='1533', productId='41567', select=[{'qId': '32', 'aId': '38'}, {'qId': '918', 'aId': '1083'}, {'qId': '16', 'aId': '18'}, {'qId': '999999', 'aId': '251'}])
    # xy_evaluate(channelId='10000164', pid='1405', productId='41567', select=[{'qId': '32', 'aId': '38'}, {'qId': '918', 'aId': '1083'}, {'qId': '16', 'aId': '18'}, {'qId': '999999', 'aId': '251'}])
    # xy_evaluate(channelId='10000164', pid='1405', productId='63328', select=[{'qId': '32', 'aId': '1853'}, {'qId': '16', 'aId': '17'}, {'qId': '918', 'aId': '1083'}, {'qId': '999999', 'aId': '247'}])
    # xy_evaluate(channelId='10000164', pid='', productId='30747', select=[{"qId":"918","aId":"1695"},{"qId":"16","aId":"17"},{"qId":"11","aId":"1124"},{"qId":"32","aId":"37"},{"qId":"39","aId":"1091"},{"qId":"999999","aId":"1"}])
    xy_evaluate(channelId='10000207', pid='1533', productId='63328', select=[{"aId":"17","qId":"16"},{"aId":"38","qId":"32"},{"aId":"5567","qId":"918"},{"aId":"232","qId":"999999"}])

'''
流程
第一步：先从 F:\git\python\hsb_project\evaadmin_huishoubao_com_cn\e2_new_product_library\m4_2C_eva\h3_1layer_ev2_conf_035.py  接口获取到产品所使用的的“选项模板”
第二步：成色模板表，Foption_id 为第一步接口返回的选项模板ID，查找并选取到对应的 Funion_id 
SELECT * FROM t_eva_quality_template WHERE Foption_id = '204';  -- 不同成色ID对应不同的 Funion_id
第三步：

curl -d '{"head":{"interface":"evaluate","msgtype":"request","remark":"","version":"0.01"},"params":{"channel_id":"10000207","cookies":"server-xy_bangma_evaluate","ip":"127.0.0.1","pid":"1533","productid":"30833","select":["34","1891","83","78","5530","71","62","23","65","2171","5535","3246","223","6931","59","55","7641","53","21","42","12"],"userid":"0"}}' http://evaserver.huishoubao.com/rpc/evaluate
    {"body":{"data":{"evaluateid":"20111320","quotation":"48700"},"ret":"0","retcode":"0","retinfo":"成功"},"head":{"interface":"evaluate","msgtype":"response","remark":"","version":"0.01"}}
    
    select Fstandard_price, Fbasic_price, Frick_guarantee, Fneed_evaluate, Fproduct_id, Fitem_param_id, Fvalid, Fmax_price, Fsku_map, Fitem_template_id from t_eva_standard_product where Fproduct_id=30833 and Fdelete_flag = 1;
    select Fevaluate_item, Fversion, Fitem_group, Fitem_add_sub, Falgorithm_order, Fall_combination_price from t_eva_item_params  where Fid = 13487 and Fdelete_flag = 1;
    
    select Fstandard_price, Fbasic_price, Frick_guarantee, Fprice_control, Fneed_evaluate, Fproduct_id, Fitem_param_id, Fos_type, Fvalid, Fuse_standard_eva, Fmax_price, Fsku_map, Fitem_template_id from t_eva_platform_product where Fproduct_id=30833 and Fplatform_type=1 and Fdelete_flag = 1;
    select Fevaluate_item, Fversion, Fitem_group, Fitem_add_sub, Falgorithm_order, Fall_combination_price from t_eva_item_params  where Fid = 2260 and Fdelete_flag = 1;
    
SELECT * FROM t_bangmai_product WHERE  Fproduct_id= 30833;
SELECT * FROM t_eva_price_display WHERE  Fdisplay_id= 248;
Display Rule: Type[1] Up[13] Down[11]

outPacket=[{"_data":{"_data":{"dropInPrice":"700","evaluateId":"20111320","highestPrice":"54300","hsbPrice":"48700"},"_errCode":"0","_errStr":"成功","_ret":"0"},"_head":{"_callerServiceId":"110001","_groupNo":"1","_interface":"xy_evaluate","_invokeId":"11111","_msgType":"response","_remark":"","_timestamps":"1604475345","_version":"0.01"}}
'''