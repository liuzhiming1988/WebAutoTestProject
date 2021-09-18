#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 50.通过渠道id获取产品商品库sku信息和大质检机况信息(回收宝专业版使用) - http://wiki.huishoubao.com/web/#/105?page_id=13239
    1. 对应服务：server-evaluate_detect（服务器应用名：server-evaluate_detect）
    2. 对应URL http://codserver.huishoubao.com

    入参：productId：必填，产品id | channelId：必填，渠道id，各个产品在不同渠道有不同的价格，可传””，但必须传递
        pid：必填，pid | platformType：非必填，使用在不需要pid和channle_id的场景下，优先使用channel_id或pid，可不传 | ip：非必填，用户公网访问IP
    出参：itemid：产品id | need_eva：1-为需要估价，0-为无需估价 | itemList：查询成功的产品配置数组 | conftype：类型id，1-是包括SKU类，2-是单选类，3-是功能性类
        desc：描述，辅助名称进行解释的陈述话语 | alias_id：别名id | alias_name：别名名称 | id：问题项id或答案项id | name：选项名称
        parent_item：父节点，对于的上一级的节点，一般之答案项对于的问题项的节点id，它是一个问题项节点值；
        question：答案项列表 | seq_num：顺序号（小的在前，大的在后） | show：针对功能性(conftype=3)选项 表示前端页面是否显示该答案项，1-显示；0或不存在不显示
        show_level：显示层级，1-级为问题级，2-级位答案级 | picture：图片列表 | picturename：图片名称
        priority：同问题项下答案的优先级，值越小，优先级越高，由平台产品或渠道的配置系数而来 | weight：同问题项下答案的权重，值越大，优先级越高，由选项库而来
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def get_sku_option_item_by_channel_id(productId, platformType, channelId, pid):
    param = {"_head":{"_interface":"get_sku_option_item_by_channel_id","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"123456","_invokeId":"123456","_callerServiceId":"112006","_groupNo":"1"},"_param":{"productId":productId,"platformType":platformType,"channelId":channelId,"pid":pid,"ip":"127.0.0.1"}}

    secret_key = "gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU"
    callerserviceid = "112006"
    url = "http://codserver.huishoubao.com/detect/get_sku_option_item_by_channel_id"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    respone.encoding = respone.apparent_encoding  # 编码设置
    print(respone.text)
    respone_dict = json.loads(respone.text)  # 转成字典
    options_list = respone_dict['_data']['_data']['itemList']

    str_sku_list = ''
    str_sku_desc = ''
    str_options_list = ''
    str_options_desc = ''
    for info in options_list:
        conftypeList = info['conftype']
        if conftypeList == "1":
            answerList = info['question']
            index = random.randint(0, len(answerList) - 1)
            str_sku_list += '"' + answerList[index]['id'] + '",'
            str_sku_desc += '"' + info['name'] + ":" + answerList[index]['name'] + '",'
        else:
            answerList = info['question']
            index = random.randint(0, len(answerList) - 1)
            str_options_list += '"' + answerList[index]['id'] + '",'
            str_options_desc += '"' + info['name'] + ":" + answerList[index]['name'] + '",'
    str_sku_list = str_sku_list[:-1]
    str_options_list = str_options_list[:-1]

    print('接口响应『json』格式数据为：\n', json.dumps(respone_dict, ensure_ascii=False) + '\n')
    print('商品库sku案项ID（随机取）：\n', '{' + str_sku_list + '}' + '\n')
    print('以上SKU_ID对应的选项+答案项名称：\n', '{' + str_sku_desc[:-1] + '}' + '\n')
    print('大质检机况案项ID（随机取）：\n', '{' + str_options_list + '}' + '\n')
    print('以上机况ID对应的选项+答案项名称：\n', '{' + str_options_desc[:-1] + '}' + '\n')
    print('接口响应时长：{0} 秒'.format(respone.elapsed.total_seconds()))

if __name__ == '__main__':
    '''正常'''
    # get_sku_option_item_by_channel_id(productId='41567',platformType='',channelId='40000001',pid='1001')
    # get_sku_option_item_by_channel_id(productId='63446',platformType='',channelId='40000001',pid='1001')

    '''"_errStr":"pid或channel_id或platformType必须传其中一个，不可都为空"'''
    # get_sku_option_item_by_channel_id(productId='41567',platformType='',channelId='',pid='')
    # get_sku_option_item_by_channel_id(productId='',platformType='',channelId='',pid='')

    '''只传platformType='1'平台类型场景，正常'''
    # get_sku_option_item_by_channel_id(productId='41567',platformType='1',channelId='',pid='')

    '''HGET Eva_PId_Cache 1001 | HGET Eva_Prd_Option 40000001_41567'''
    # get_sku_option_item_by_channel_id(productId='41567',platformType='',channelId='',pid='1001')

    '''HGET Eva_PId_Cache 1365 | HGET Eva_Prd_Option 10000135_41567'''
    # get_sku_option_item_by_channel_id(productId='41567',platformType='',channelId='',pid='1365')

    '''1363：闲鱼信用速卖，优先取渠道'''
    get_sku_option_item_by_channel_id(productId='41567',platformType='',channelId='40000001',pid='1365') #优先取渠道
    # get_sku_option_item_by_channel_id(productId='41567',platformType='10',channelId='40000001',pid='1001') #优先取渠道


'''
curl -H 'HSB-OPENAPI-SIGNATURE:a688c54f31864c0e9964975e29922e84' -H 'HSB-OPENAPI-CALLERSERVICEID:216008' -d '{"_head":{"_callerServiceId":"216008","_groupNo":"1","_interface":"pdt_sku_query","_invokeId":"18218120c6ec08721b7efef201dff38c","_msgType":"request","_remark":"","_timestamps":"1605238804","_version":"0.01"},"_param":{"info":{"combination":"0","productId":"41567"},"subInterface":"sku_option_combination_get"}}' http://prdserver.huishoubao.com/rpc/new_product_lib

select Fid, Fname, Flevel, Fpid, Fplatform_type_property, Fvalid, Fweight from t_eva_item_base  where Fid in(12,13,14,15,1124,6047,6116,7630,130,471,17,18,2236,36,38,42,1091,1083,1773,2241,2242);

curl -H 'HSB-OPENAPI-SIGNATURE:29ec18bfd91cd545fb75603022aa4726' -H 'HSB-OPENAPI-CALLERSERVICEID:216008' -d '{"_head":{"_callerServiceId":"216008","_groupNo":"1","_interface":"eva_option_get","_invokeId":"050a66d672c37c85189e7c28e10e2fa9","_msgType":"request","_remark":"","_timestamps":"1605238805","_version":"0.01"},"_param":{"channel_id":"","ip":"127.0.0.1","pid":"","platform_type":"1","product_id":"41567","user_name":"server-evaluate_detect"}}' http://prdserver.huishoubao.com/rpc/new_product_lib
'''