#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 6.可估价产品产品选项获取  - http://wiki.huishoubao.com/index.php?s=/105&page_id=1595
    1.对应服务：server-base_product（base_product）

    第一步：拿用户估价选项（举例：B端帮卖估价 41567， 可以去2C估价里找41567，找到其选项作为传参【正好可以用此接口）

    B端帮卖，前端，机型估价选项获取（17项）  ①可以传渠道id：10000254（2C）、②可以传平台 1

    入参：channel_id：渠道id，渠道id，各个产品在不同渠道有不同的价格，可传””但必须传递
        platform_type：使用在不需要 pid 和 channle_id 的场景下 优先使用 channel_id 或 pid 可不传 | product_id：产品id，要查询产品选项的产品ID
    出参：need_eva：1为需要估价 0为无需估价
        itemList：查询成功的产品配置数组
            conftype：类型id，1是包括SKU类，2是单选类，3是功能性类 | id：问题项id 或 答案项id
            name：选项名称 | parent_item：父节点，对于的上一级的节点，一般之答案项对于的问题项的节点id，它是一个问题项节点值；
            seq_num：顺序号 （小的在前，大的在后） | show_level：显示层级，1级为问题级，2级位答案级
            question：答案项列表
                id：问题项id 或 答案项id | name：选项名称
                parent_item：父节点，对于的上一级的节点，一般之答案项对于的问题项的节点id，它是一个问题项节点值；
                priority：同问题项下答案的优先级,值越小,优先级越高,由平台产品或渠道的配置系数而来
                seq_num：顺序号 （小的在前，大的在后） | show_level：显示层级，1级为问题级，2级位答案级 | weight：同问题项下答案的权重,值越大,优先级越高,由选项库而来
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def eva_option_get(channel_id, product_id, pid, platform_type):
    param = { "_head":{ "_interface":"eva_option_get", "_msgType":"request", "_remark":"hello", "_version":"0.01", "_timestamps":"123", "_invokeId":"111", "_callerServiceId":"112002", "_groupNo":"1" },"_param":{ "channel_id":channel_id, "product_id":product_id, "pid":pid,"platform_type":platform_type}}

    secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
    callerserviceid = "112002"
    url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    respone.encoding = respone.apparent_encoding  # 编码设置
    respone_dict = json.loads(respone.text)  # 转成字典
    # print(respone_dict)
    options_list = respone_dict['_body']['_data']['itemList']

    str_options_list = ''
    str_options_desc = ''
    for info in options_list:
        answerList = info['question']
        index = random.randint(0, len(answerList) - 1)
        str_options_list += '"' + answerList[index]['id'] + '",'
        str_options_desc += '"' + info['name'] + ":" + answerList[index]['name'] + '",'
    str_options_list = str_options_list[:-1]

    print('接口响应『json』格式数据为：\n', json.dumps(respone_dict, ensure_ascii=False) + '\n')
    print('大质检【用户】估价【sku】+【机况】答案项ID（随机取）：\n', '{' + str_options_list + '}' + '\n')
    print('以上【sku】+以上【机况】选项名称+答案项名称：\n', '{' + str_options_desc[:-1] + '}' + '\n')
    print('接口响应时长：{0} 秒'.format(respone.elapsed.total_seconds()))

if __name__ == '__main__':
    ''' channel_id="" 和 platform_type='1' 传一个即可 '''
    # eva_option_get(channel_id="", product_id="63398", pid="", platform_type='1')           # 20200228   63398   华为 Mate 30   √
    # eva_option_get(channel_id="", product_id="63398", pid="", platform_type='2')           # 20200228   63398   华为 Mate 30   √
    # eva_option_get(channel_id="10000254", product_id="63330", pid="", platform_type='')    # 20200228   63330   iPhone 11    √
    # eva_option_get(channel_id="", product_id="63330", pid="", platform_type='')            # 20200228   63330   iPhone 11    √
    # eva_option_get(channel_id="10000254", product_id="63399", pid="", platform_type='')    # 20200228   63399   华为 Mate 30 Pro  √
    # eva_option_get(channel_id="10000254", product_id="30831", pid="", platform_type='')    # 20200306   30831   iPhone 7
    # eva_option_get(channel_id="", product_id="38200", pid="", platform_type='1')           # 20200306   38200   iPhone 8
    # eva_option_get(channel_id="", product_id="2068", pid="", platform_type='1')            #
    # eva_option_get(channel_id="10000164", product_id="63330", pid="", platform_type='')    #
    # eva_option_get(channel_id="10000164", product_id="64169", pid="1405", platform_type='')    #
    # eva_option_get(channel_id="10000190", product_id="64169", pid="1405", platform_type='')    #
    eva_option_get(channel_id="10000060", product_id="41567", pid="1196", platform_type='')
    # for i in range(10):
        # eva_option_get(channel_id="10000135", product_id="30752", pid="1365", platform_type='')    #

    # eva_option_get(channel_id="", product_id="64247", pid="", platform_type='1')    # 错误数据机型，华为 P40 Pro+（5G） | "id":"32"
    # eva_option_get(channel_id="", product_id="64001", pid="", platform_type='1')    # 无错误数据机型，华为 P40 Pro（5G） | "id":"32"

''' 20200813 合作-阿里，同一个大类下，多个问题项的顺序：按seq_num的顺序号，小的在前，大的在后； 同一个问题项下，答案项的顺序同理
    1. SKU，只能单个机型的调，在2C平台调价页面，拖动问题项上下顺序，拖动问题项下答案项的左右顺序；
    2. 机况，可以在调价页面，拖动问题项上下顺序，拖动问题项下答案项的左右顺序； 也可以在选项模板设置好后，重新分配给机型（也是默认的顺序）'''
# eva_option_get(channel_id="", product_id="23009", pid="", platform_type='1')           # 20200227   41567   iPhone X     √


# select Fproduct_item, Falias_id_comb, Fshow_item, Fvalid, Fdelete_flag, Fneed_eval
# uate, Fitem_param_id, Fsku_map, Fitem_template_id from t_eva_standard_product  where Fproduct_id = 59939;
# select Fevaluate_item from t_eva_item_params  where Fid=56068;
# select Fproduct_item, Fshow_item, Falias_id_comb, Fuse_standard_eva, Fvalid, Fprice_control, Fdelete_flag, Fneed_evaluate, Fitem_param_id, Fsku_map, Fitem_template_id from t_eva_platform_product  where Fproduct_id = 59939 and Fplatform_type = 1;
# select Fevaluate_item from t_eva_item_params  where Fid=56091;

''' {"_body": {"_data": {"itemList": [{"conftype": "2", "desc": "", "id": "22", "name": "开机", "parent_item": "0", "question": [{"desc": "", "id": "23", "name": "正常开机", "parent_item": "22", "priority": "1", "seq_num": "0", "show_level": "2", "skuMap": [], "weight": "20"}, {"desc": "", "id": "24", "name": "不能正常开机", "parent_item": "22", "priority": "2", "seq_num": "1", "show_level": "2", "skuMap": [], "weight": "10"}], "seq_num": "1", "show_level": "1"}], "itemid": "23009", "need_eva": "1", "time": "1597304437"}, "_ret": "0", "_retcode": "0", "_retinfo": "成功"}, "_head": {"_callerServiceId": "112002", "_groupNo": "1", "_interface": "eva_option_get", "_invokeId": "111", "_msgType": "response", "_remark": "", "_timestamps": "1597304437", "_version": "0.01"}}
'''