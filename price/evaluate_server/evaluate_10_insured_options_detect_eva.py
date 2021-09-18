#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 估价服务 - 10.获取保价产品选项接口 -  http://wiki.huishoubao.net/index.php?s=/138&page_id=2220
    接口内部先计算是否保价，再根据计算结果，拉取相应的产品数据（保价拉保价版本数据、不保价拉取最新版本数据）
	1.对应服务 rpc_evaluate_server（服务器应用名：rpc_evaluate_server）

    入参：user_name：否，调用方名称 | productId：是，修改产品后的产品id 优先使用这个 未传递则使用DB中的
        isOverInsurance：否，是否强制过保，0-否，1-强制过保，默认为0 | channelId：否，渠道ID
    出参：channelID	是，渠道Id | insured：是，0-过保，1-保价 | new_product：是，改变产品Id标记 0未修改 1修改 | orderid：是，订单Id
        pid：是，Pid | platformID：是，估价平台 | productId：是，产品Id | options：是，选项信息 | itemList：是，选项列表
        conftype：是，选项类型 | desc：是，选项描述 | id：是，选项ID | name：是，选项名称 | parent_item：是，选项父Id
        priority：是，答案项优先级 值越小 优先级越大 | weight：是，答案项权重,值越大,权重越大 | question：是，问题项列表
        show：是，表示前端页面是否显示该答案项 ，1显示；0或不存在不显示 | show_level：是，显示层级，1级为问题级，2级位答案级
        seq_num：是，顺序号 | itemid：是，产品Id
'''

import requests, json, os, random
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def insured_options(order_id, productId, isOverInsurance):
    param = {"head":{"interface":"insured_options","msgtype":"request","remark":"","version":"0.01"},"params":{"order_id":order_id, "productId":productId, "isOverInsurance":isOverInsurance, "user_name":"zhangjinfa@huishoubao.com.cn"}}

    headers = {"Content-Type":"application/json;charset=UTF-8"}
    url = "http://evaserver.huishoubao.com/rpc/insured"
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    respone.encoding = respone.apparent_encoding  # 编码设置
    respone_dict = json.loads(respone.text)  # 转成字典
    # print(respone_dict)
    options_list = respone_dict['body']['data']['options']['itemList']

    str_options_list = ''
    str_options_desc = ''
    for info in options_list:
        answerList = info['question']
        index = random.randint(0, len(answerList) - 1)
        str_options_list += '"' + answerList[index]['id'] + '",'
        str_options_desc += '"' + info['name'] + ":" + answerList[index]['name'] + '",'
    str_options_list = str_options_list[:-1]

    print('接口响应『json』格式数据为：\n', json.dumps(respone_dict, ensure_ascii=False) + '\n')
    print('大质检【检测】估价【sku】+【机况】答案项ID（随机取）：\n', '{' + str_options_list + '}' + '\n')
    print('以上【sku】+以上【机况】选项名称+答案项名称：\n', '{' + str_options_desc[:-1] + '}' + '\n')
    print('接口响应时长：{0} 秒'.format(respone.elapsed.total_seconds()))

if __name__ == '__main__':
    ''' 传 isOverInsurance=1，order_id为无效订单  pass  '''

    ''' 传 isOverInsurance，为空，正常默认为0  pass'''
    # insured_options(order_id="7598533", productId='54791',isOverInsurance='')
    # insured_options(order_id="7598533", productId='54791',isOverInsurance='') # 保价时间配置13天，发货-下单=10天，在保

    ''' 传 isOverInsurance=2，不符合条件，还是按默认0获取 pass'''
    # insured_options(order_id="7598533", productId='54791',isOverInsurance='2')

    ''' 传 isOverInsurance=1，返回现网产品选项 pass'''
    # insured_options(order_id="7598533", productId='54791',isOverInsurance='1')

    ''' 传 isOverInsurance=1，order_id为无效订单，"_retinfo":"获取订单的基本信息失败 pass"'''
    # insured_options(order_id="202010210001", productId='54791',isOverInsurance='1')
    # insured_options(order_id="7598533", productId='202010210001',isOverInsurance='1')
    # insured_options(order_id="", productId='54791',isOverInsurance='1')
    # insured_options(order_id="7598533", productId='',isOverInsurance='1')
    # insured_options(order_id="", productId='',isOverInsurance='1')
    insured_options(order_id="7610474", productId='23010',isOverInsurance='')

    ''' 传 isOverInsurance=1，productId与用户机型不一致 由iPhone XR 变成 iPhone XS  pass'''
    # insured_options(order_id="7598533", productId='54790',isOverInsurance='0')
    # insured_options(order_id="7598533", productId='54790',isOverInsurance='0') # 保价时间配置13天，发货-下单=10天，在保
    # insured_options(order_id="7598533", productId='54790',isOverInsurance='1')

    ''' order_id为B端帮卖批量单，iPhone XS 返回现网产品选项 pass'''
    # 估价记录ID evaluateId=0  不再单独调查询估价记录接口   直接查询并返回检测机型现网选项 pass
    # insured_options(order_id="7598522", productId='54790',isOverInsurance='0') # 帮卖单无保价逻辑，统一取现网选项
    # insured_options(order_id="7598522", productId='54790',isOverInsurance='1')

    # insured_options(order_id="7598522", productId='54790',isOverInsurance='0')  # 保价时间配置大于7天

    ''' order_id为B端帮卖批量单，productId不传，取订单里面的机型ID，也是固定写死的7017，在价格侧又是个不可估价机型，则固定取30827产品的估价选项 '''
    # insured_options(order_id="7598522", productId='', isOverInsurance='0') # 检测自定义机型 非笔记本 选项拉取使用2C平台 30827产品估价选项
    # insured_options(order_id="7598522", productId='', isOverInsurance='1') # 检测自定义机型 非笔记本 选项拉取使用2C平台 30827产品估价选项

    ''' order_id为B端帮卖普通单 '''
    # insured_options(order_id="7598535", productId='', isOverInsurance='0')  # 不传机型ID，取订单中的机型ID，无保价逻辑，统一取现网选项，
    # insured_options(order_id="7598535", productId='', isOverInsurance='1')
    # insured_options(order_id="7598535", productId='38201', isOverInsurance='0') # 检测传机型与用户下单机型一致
    # insured_options(order_id="7598535", productId='54790', isOverInsurance='0') # 检测传机型与用户下单机型不一致

    ''' 有错误的数据'''
    # insured_options(order_id="7604917", productId='64247', isOverInsurance='0') # 订单在保，不强制过保
    # insured_options(order_id="7604939", productId='64247', isOverInsurance='0') # 订单在保，不强制过保

    # insured_options(order_id="7604918", productId='64247', isOverInsurance='0') # 错误数据机型，订单在保，历史版本数据“存储容量”数据存在多个。"id":"32"
    # insured_options(order_id="7604918", productId='64247', isOverInsurance='1') # 错误数据机型，订单在保，历史版本数据“存储容量”数据存在多个。"id":"32"

    '''无错误的数据'''
    # insured_options(order_id="7604922", productId='64001', isOverInsurance='0') # 订单在保  "id":"32"

    # insured_options(order_id="7605782", productId='23010', isOverInsurance='1') # 订单在保  "id":"32"


'''
1. 订单在保，不强制过保
select Fevaluate_item, Fstandard_price, Fmin_price, Fproduct_id, Fproduct_item, Fshow_item, Fsku_map from t_eva_pditems_history  where Fplatform_type = 1 and Fproduct_id = 54791 and Fversion = 489;
2. 订单在保，强制保价
curl -H 'HSB-OPENAPI-SIGNATURE:b7fb2dff6b1dc0e219e421fd5a6fffa2' -H 'HSB-OPENAPI-CALLERSERVICEID:212006' -d '{"_head":{"_callerServiceId":"212006","_groupNo":"1","_interface":"product_id_info_get","_invokeId":"d17d288a2a22f7568abdcd786496acf9","_msgType":"request","_remark":"","_timestamps":"1603263466","_version":"0.01"},"_param":{"evaFlag":"1","fchannel_id":"40000001","fproduct_id":"54791"}}' http://prdserver.huishoubao.com/rpc/new_product_lib
select Fstandard_price, Fproduct_item, Fshow_item, Fbasic_price, Frick_guarantee, Fprice_control, Fneed_evaluate, Fproduct_id, Fitem_param_id, Fos_type, Fvalid, Fuse_standard_eva, Fitem_template_id, Fsku_map from t_eva_platform_product where Fproduct_id = 54791 and Fplatform_type = 1 and Fdelete_flag = 1
'''