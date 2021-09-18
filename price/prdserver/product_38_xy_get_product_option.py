#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 38.闲鱼帮买用户产品估价选项获取 - http://wiki.huishoubao.com/index.php?s=/105&page_id=6804
    1. 对应服务：server-bangmai_pro_eva（服务器应用名：server-bangmai_pro_eva）

    入参：productId：必填，产品id，要查询产品选项的产品ID | channelId：必填，渠道id，不为空
    出参：productId：产品id | list：产品估价选项liebiao | id：问题项id或答案项id | name：选项名称 | question：答案项列表 | desc：答案项描述
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def xy_get_product_option(productId, channelId,Funion_id):
    param = {"_head":{"_interface":"xy_get_product_option","_msgType":"request","_remark":"hello","_version":"0.01","_timestamps":"123","_invokeId":"111","_callerServiceId":"110001","_groupNo":"1"},"_param":{ "productId":productId, "channelId":channelId }}

    secret_key = "c36691ced620bf82ad3fc4642f8a6427"
    callerserviceid = "110001"
    url = "http://bmserver.huishoubao.com/bangmai/xy_get_product_option"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, data=json.dumps(param), headers=headers, proxies=hsb_eva_ipProxy_test())
    respone.encoding = respone.apparent_encoding  # 编码设置
    print(respone.text)
    respone_dict = json.loads(respone.text)  # 转成字典
    skuList = respone_dict['_data']['_data']['list']
    print(json.dumps(skuList))

    str_Qid_List = [] # 用于存放响应数据中的 答案项id
    question_list_p = []  # 用于临时过渡性存放 答案项id（因为响应数据中，最后一个
    str_Aid_List = []  # 用于最终存放 答案项id 数据

    for info in skuList:
        index = random.randint(0, len(info) - 1)
        str_Qid_List.append(info['id'])

        question_list_p.append(info['question'])
    question_list_p.pop(-1)
    print('question_list_p --->',question_list_p)

    for info_Aid in question_list_p:
        index = random.randint(0, len(info_Aid) - 1)
        str_Aid_List.append(info_Aid[index]['id'])

    str_Aid_List.append(Funion_id)
    print(str_Qid_List,str_Aid_List)

    Q_A_list = list(zip(str_Qid_List, str_Aid_List))
    print('Q_A_list --->',Q_A_list)
    Qid_Aid_list = []
    for i in Q_A_list:
        Qid_Aid_dic = dict(qId=i[0], aId=i[1])
        Qid_Aid_list.append(Qid_Aid_dic)
    print(Qid_Aid_list)

if __name__ == '__main__':
    # xy_get_product_option(Funion_id='251', productId='', channelId='')
    # xy_get_product_option(Funion_id='251', productId='41567', channelId='')
    # xy_get_product_option(Funion_id='251', productId='41567', channelId='11111111111111')
    # xy_get_product_option(Funion_id='251', productId='41567', channelId='10000207')
    # xy_get_product_option(Funion_id='240', productId='46517', channelId='10000164')
    # xy_get_product_option(Funion_id='', productId='41567',channelId='10000164')
    xy_get_product_option(Funion_id='12', productId='3121',channelId='10000207')

'''
流程
select Fchannel_flag from t_channel where Fchannel_id= 10000164;
select Fplatform_type from t_eva_channel_platform_map where Fvalid=1 and  Fchannel_id = 10000164;

select Fproduct_item, Falias_id_comb, Fshow_item, Fvalid, Fdelete_flag, Fneed_evaluate, Fitem_param_id, Fsku_map, Fitem_template_id from t_eva_standard_product  where Fproduct_id = 41567;   -- 可以得到 Fitem_template_id 
-- 结合 F:\git\python\hsb_project\product_server\product_40_xy_evaluate.py  一起使用
-- 通过 SELECT * FROM t_eva_quality_template WHERE Foption_id = '204';  -- 不同成色ID对应不同的 Funion_id，得到 Funion_id

select Fevaluate_item from t_eva_item_params  where Fid = 11812;

select Fproduct_item, Fshow_item, Falias_id_comb, Fuse_standard_eva, Fvalid, Fprice_control, Fdelete_flag, Fneed_evaluate, Fitem_param_id, Fsku_map, Fitem_template_id from t_eva_platform_product  where Fproduct_id = 41567 and Fplatform_type = 1;
select Fevaluate_item from t_eva_item_params  where Fid = 11126;

select Fvalid, Fdelete_flag, Fevaluate_item from t_eva_product_operate  where Fproduct_id = 41567 and Fchannel_id = 10000164;

select Fsku_id, Fselect, Fclass_id, t_eva_item_base.Fname as sku_name, t_pdt_class.Fname as clss_name from t_bangmai_sku_rule left join t_eva_item_base on t_bangmai_sku_rule.Fsku_id = t_eva_item_base.Fid left join t_pdt_class on t_pdt_class.Fid = t_bangmai_sku_rule.Fclass_id where 1=1  and t_pdt_class.Fid = 1 and Fselect = 1;

select t_eva_quality_template.Funion_id, Fquality_name, Fquality_desc from t_eva_channel_quality  left join t_eva_quality_template on t_eva_channel_quality.Fquality_id = t_eva_quality_template.Fquality_id and t_eva_channel_quality.Fchannel_id = t_eva_quality_template.Fchannel_id where t_eva_quality_template.Fchannel_id =10000164  and t_eva_quality_template.Foption_id =204  and t_eva_channel_quality.Fvalid =1  and t_eva_quality_template.Fdelete_flag =0;

【问题解析，如果遇到这种错误 realDealModelData|44|图片信息解析错误71】
可以 删除redis
    del Eva_Index_ItemBasePic_Item
    del Eva_ItemBasePic
'''