#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 估价服务 - 2-检测估价接口  -  http://wiki.huishoubao.net/index.php?s=/138&page_id=2212
	1.对应服务 rpc_evaluate_server（服务器应用名：rpc_evaluate_server）

    入参：orderid：订单ID（必填） | productId：否，修改产品后的产品id 优先使用这个 未传递则使用DB中的（非必选）
        select：用户选择的估价选项（必填） |  isOverInsurance：是否强制过保，0-否，1-强制过保，默认为0（非必填） | userid：检测员登录ID（必填）
    出参：quotation：估算价格，单位分 |  evaluateid：估价唯一id; | evaversion：检测员使用的产品估价版本号 | evaluateType：估价类型，1-现网估价，2-历史估价
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

class Eva_Luateengineer:
    def eva_option_get(self, channel_id, product_id, pid, platform_type):
        ''' http://wiki.huishoubao.com/web/#/105?page_id=1595 '''
        ''' platform_type：使用在不需要 pid 和 channle_id 的场景下，优先使用channel_id 或 pid，可不传'''
        param = {"_head": {"_interface": "eva_option_get", "_msgType": "request", "_remark": "hello", "_version": "0.01","_timestamps": "123", "_invokeId": "111", "_callerServiceId": "112002", "_groupNo": "1"},"_param": {"channel_id": channel_id, "product_id": product_id, "pid": pid, "platform_type": platform_type }}

        secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
        callerserviceid = "112002"
        url = "http://prdserver.huishoubao.com/rpc/new_product_lib"
        md5value = json.dumps(param) + "_" + secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID": callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典
        options_list = respone_dict['_body']['_data']['itemList']

        str_options_list = []
        str_options_list_show = ''
        str_options_desc_show = ''
        for info in options_list:
            answerList = info['question']
            index = random.randint(0, len(answerList) - 1)
            str_options_list.append(answerList[index]['id'])
        # 以下只为打印输出随机取的估价选项数据
            str_options_list_show += '"' + answerList[index]['id'] + '",'
            str_options_desc_show += '"' + info['name'] + ":" + answerList[index]['name'] + '",'
        str_options_list_show = str_options_list_show[:-1]

        print('估价答案项ID传参数据为（随机取）：\n', '{' + str_options_list_show + '}' + '\n')
        print('以上估价答案项ID对应的选项+答案项名称：\n', '{' + str_options_desc_show[:-1] + '}' + '\n')

        return str_options_list

    # isOverInsurance：是否强制过保 0:否 1:强制过保,默认为0（非必填）   0312检测估价强制过保需求增加
    def evaluateengineer(self, orderid, isOverInsurance, channel_id, product_id, pid, platform_type):
        # select = self.eva_option_get(channel_id=channel_id, product_id=product_id, pid=pid, platform_type=platform_type)
        select = ["12","3246","20","2171","23","223","35","40","53","55","5535","59","63","65","71","6702","6931","9","73","77","7641"]
        param = {"head":{"interface":"evaluateengineer","msgtype":"request","remark":"","version":"0.01"},"params":{"cookies":"server-evaluate_detect","ip":"127.0.0.1","orderid":orderid, "productId":product_id, "select":select,  "isOverInsurance":isOverInsurance, "userid":"1311"}}
        headers = {"Content-Type":"application/json;charset=UTF-8"}
        url = "http://evaserver.huishoubao.com/rpc/evaluate"  # 大质检 /rpc/evaluate
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        hsb_response_print(respone=respone)

if __name__ == '__main__':
    eva_luateengineer = Eva_Luateengineer()
    # select = ["23","55","58","62","66","1340","3247","5530","3242","36","83","223","5410","1077","20","3245","2170","18","5535","6930","7642","13"]
    # eva_luateengineer.evaluateengineer(orderid='7598979', product_id='54791', isOverInsurance='1', channel_id='40000001', pid='', platform_type='')

    # select = ["82","62","66","71","58","5530","78","56","15","1091","7641","6931","36","5535","24","224","1633","20","1078","2171","18","3246"]
    # eva_luateengineer.evaluateengineer(orderid='7598979', product_id='41567', isOverInsurance='0', channel_id='40000001', pid='', platform_type='')
    # eva_luateengineer.evaluateengineer(orderid='7600137', product_id='54790', isOverInsurance='1', channel_id='40000001', pid='', platform_type='')

    # 20201208 检测工程师估价接口屏蔽掉模板判断的逻辑（选项模板ID变化）
    # eva_luateengineer.evaluateengineer(orderid='7601021',product_id='23009',isOverInsurance='0',channel_id='40000001',pid='',platform_type='')
    # eva_luateengineer.evaluateengineer(orderid='7601021',product_id='23009',isOverInsurance='1',channel_id='40000001',pid='',platform_type='')
    # 20201208 检测工程师估价接口屏蔽掉模板判断的逻辑（选项模板ID不变）
    # eva_luateengineer.evaluateengineer(orderid='7601021',product_id='23009',isOverInsurance='0',channel_id='40000001',pid='',platform_type='')
    # eva_luateengineer.evaluateengineer(orderid='7601021',product_id='23009',isOverInsurance='1',channel_id='40000001',pid='',platform_type='')

    # select = ["14","42","38","1634","17","83","63","71","73","77","65","59","55","7641","6931","5535","23","223","20","1078","2171","3246"]
    # eva_luateengineer.evaluateengineer(orderid='7601020',product_id='41567',isOverInsurance='',channel_id='40000001',pid='',platform_type='')
    # eva_luateengineer.evaluateengineer(orderid='7601020',product_id='41567',isOverInsurance='1',channel_id='40000001',pid='',platform_type='')

    # 2020.03.12 检测估价强制过保需求
    # ①isOverInsurance传空， "quotation":"17100"    ②修改基准价 系数 等级上下限后 "quotation":"17100"
    # select=["23","58","55","61","1091","65","68","38","2171","3246","15","74","21","77","1078","18","1083","82","224"]
    # eva_luateengineer.evaluateengineer(orderid='7600124', product_id='63446', isOverInsurance='', channel_id='40000001', pid='', platform_type='')

    # 2020.03.12 检测估价强制过保需求
    # ①isOverInsurance传空， "quotation":"17100"    ②修改基准价 系数 等级上下限后 "quotation":"17100"
    # select=["23","58","55","61","1091","65","68","38","2171","3246","15","74","21","77","1078","18","1083","82","224"]
    # eva_luateengineer.evaluateengineer(orderid='7600124', product_id='63446', isOverInsurance='0', channel_id='40000001', pid='', platform_type='')

    # 2020.03.12 检测估价强制过保需求
    # ①isOverInsurance传值非0非1， "quotation":"17100"   ②修改基准价 系数 等级上下限后 "quotation":"17100"
    # select=["23","58","55","61","1091","65","68","38","2171","3246","15","74","21","77","1078","18","1083","82","224"]
    # eva_luateengineer.evaluateengineer(orderid='7600124', product_id='63446', isOverInsurance='2', channel_id='40000001', pid='', platform_type='')

    # 2020.03.12 检测估价强制过保需求
    # ①isOverInsurance传值1，强制过保， "quotation":"17100"   ②修改基准价 系数 等级上下限后 "quotation":"49900"
    # select=["23","58","55","61","1091","65","68","38","2171","3246","15","74","21","77","1078","18","1083","82","224"]
    # eva_luateengineer.evaluateengineer(orderid='7600124', product_id='63446', isOverInsurance='1', channel_id='40000001', pid='', platform_type='')


    # 2020.03.13  优化先计算差值再计算等级算法  机型名称：iPhone 6   机型ID：30748
    # select=["2171","44","53","56","58","63","34","65","15","23","69","20","3246","3244","17","1083","223","77","82"]
    # eva_luateengineer.evaluateengineer(orderid='7598732', product_id='54791', isOverInsurance='1', channel_id='40000001', pid='', platform_type='')



    ''' 2020.10.15  大质检-检测工程师估价，①会先调用保价判断接口，如果保价中，则取历史版本估价；如果不保价，则取现网版本估现网价'''

    # eva_luateengineer.evaluateengineer(orderid='7598459', product_id='4006', isOverInsurance='', channel_id='40000001', pid='', platform_type='')
    # eva_luateengineer.evaluateengineer(orderid='7607559', product_id='30749', isOverInsurance='0', channel_id='10000343', pid='', platform_type='')

    eva_luateengineer.evaluateengineer(orderid='7629774', product_id='23036', isOverInsurance='0', channel_id='', pid='', platform_type='')

    # for i in range(10):
    #     eva_luateengineer.evaluateengineer(orderid='7604918', product_id='64247', isOverInsurance='0', channel_id='40000001', pid='', platform_type='')
    #     eva_luateengineer.evaluateengineer(orderid='7604918', product_id='64247', isOverInsurance='1', channel_id='40000001', pid='', platform_type='')
    #     eva_luateengineer.evaluateengineer(orderid='7604917', product_id='64247', isOverInsurance='1', channel_id='40000001', pid='', platform_type='')
    #     eva_luateengineer.evaluateengineer(orderid='7604939', product_id='64247', isOverInsurance='0', channel_id='40000001', pid='', platform_type='')
    #     eva_luateengineer.evaluateengineer(orderid='7604922', product_id='64001', isOverInsurance='0', channel_id='40000001', pid='', platform_type='')

'''
【20201208 rpc_evaluate_server】
indata={"head": {"interface": "evaluateengineer", "msgtype": "request", "remark": "", "version": "0.01"}, "params": {"cookies": "server-evaluate_detect", "ip": "127.0.0.1", "orderid": "7598979", "productId": "41567", "select": ["82", "61", "65", "68", "59", "73", "79", "56", "13", "1091", "7641", "6931", "36", "5534", "24", "223", "1633", "21", "1077", "2171", "17", "3246"], "isOverInsurance": "0", "userid": "1311"}}

curl -d '{"head":{"interface":"insured_judge","msgtype":"request","remark":"","version":"0.01"},"params":{"checkItem":["82","61","65","68","59","73","79","56","13","1091","7641","6931","36","5534","24","223","1633","21","1077","2171","17","3246"],"order_id":"7598979","productId":"41567","user_name":"evaluate_server"}}' http://evaserver.huishoubao.com/rpc/insured
    
Reply:{"body":{"data":{"additionVersion":"0","channelID":"40000001","insured":"0","isItemConsistent":"0","isItemTemplateConsistent":"1","new_product":"1","operatorVersion":"0","orderTime":"2020-10-31 09:32:11","order_id":"7598979","pid":"1001","platformID":"1","platformVersion":"507","productId":"41567","propertyFlag":"0","tagId":"1","unifiedVersion":"67"},"ret":"0","retcode":"0","retinfo":"成功"},"head":{"interface":"insured_judge","msgtype":"response","remark":"","version":"0.01"}}

orderId: 7598979 order can't insured,  evaluate type is current
user's product id=41567

select Fplatform_type from t_eva_channel_platform_map  where Fvalid=1 and Fdelete_flag=0 and Fchannel_id=10000164
select Fchannel_id, Faddition, Fversion, Fvalid, Fdelete_flag, Foperator_name, Faddition_range from t_eva_channel_addition  where Fchannel_id = 10000164 and Fdelete_flag=1
select Fevaluate_item, Fstandard_price, Fmin_price, Fitem_group, Fitem_add_sub, Falgorithm_order, Fall_combination_price from t_eva_standard_pditems_history  where Fproduct_id = 4006 and Fversion = 13;
select Fevaluate_item, Fstandard_price, Fmin_price, Fitem_group, Fitem_add_sub, Falgorithm_order, Fall_combination_price from t_eva_pditems_history  where Fplatform_type = 1 and Fproduct_id = 4006 and Fversion = 89;

Platform Eva Version: 906 standardPrice:278000
整机项: 278000*100/100 *82/100 *100/100 *100/100 *100/100 *79/100 *100/100 *100/100 *100/100 *100/100 *100/100 *100/100 *100/100 *100/100 = 180088
非整机项:(180088*30/100=54026*100/100 *100/100 = 54026) + (180088*30/100=54026*100/100 = 54026) + (180088*40/100=72035*100/100 *100/100 *100/100 *100/100 *100/100 = 72035) = 180087
系数特殊规则:180087 = 180087
SKU价格:278000*82/100 *100/100 *79/100 *100/100 *100/100 = 180088
选项分组命中等级:10 lType:1 lValue:3 uType:1 uValue:3
选项分组下限百分比:(180088*3)/100=5402
选项分组上限百分比:(180088*3)/100=5402
选项分组取上限:5402
先计算选项分组再计算差值算法 差值:(5402+278000*0/100+0)*100/100 = 5402

outdata={"body":{"data":{"evaluateType":"1","evaluateid":"201210768","evaversion":"","quotation":"5500"},"ret":"0","retcode":"0","retinfo":"成功"},"head":{"interface":"evaluateengineer","msgtype":"response","remark":"","version":"0.01"}}

给机型调价，再调一次
因为订单仍处在 保价期 内，所以还是取的历史版本去估的价格

【20201208 rpc_insured_server】
indata={"head":{"interface":"insured_judge","msgtype":"request","remark":"","version":"0.01"},"params":{"checkItem":["82","61","65","68","59","73","79","56","13","1091","7641","6931","36","5534","24","223","1633","21","1077","2171","17","3246"],"order_id":"7598979","productId":"41567","user_name":"evaluate_server"}}

curl -H 'HSB-OPENAPI-SIGNATURE:82ab1defd400a9f44e0766b603c0053d' -H 'HSB-OPENAPI-CALLERSERVICEID:216009' -d '{"_head":{"_callerServiceId":"216009","_groupNo":"1","_interface":"getOrderInfo","_invokeId":"dc7361244aabbf97903d9429f7a0451a","_msgType":"request","_remark":"","_timestamps":"1607396485","_version":"0.01"},"_param":{"containInfo":["good","basic","evaluation"],"orderId":"7598979"}}' http://ordserver.huishoubao.com/order_center/getOrderInfo

curl -H 'HSB-OPENAPI-SIGNATURE:2aa39237b5de623487939c494af2d844' -H 'HSB-OPENAPI-CALLERSERVICEID:216009' -d '{"_head":{"_callerServiceId":"216009","_groupNo":"1","_interface":"get_eva_record","_invokeId":"775d86fd917dc3cac6a993c73facd0e5","_msgType":"request","_remark":"","_timestamps":"1607396485","_version":"0.01"},"_param":{"evaluateId":"201011781"}}' http://evaserver.huishoubao.com/eva_query/get_eva_record

OrderId: 7598979 GetInTime: 2020-12-08 11:01:25 OrderTime: 2020-10-31 09:32:11
change user new product
user can't insured
user's product id=41567

curl -H 'HSB-OPENAPI-SIGNATURE:bc2971b28f0b09b7bd002ac1b930128e' -H 'HSB-OPENAPI-CALLERSERVICEID:212006' -d '{"_head":{"_callerServiceId":"212006","_groupNo":"1","_interface":"product_id_info_get","_invokeId":"5579108ac76fa828e85e0ac2ce09380a","_msgType":"request","_remark":"","_timestamps":"1607396485","_version":"0.01"},"_param":{"evaFlag":"1","fchannel_id":"40000001","fproduct_id":"41567"}}' http://prdserver.huishoubao.com/rpc/new_product_lib

select Fstandard_price, Fproduct_item, Fshow_item, Fbasic_price, Frick_guarantee, Fprice_control, Fneed_evaluate, Fproduct_id, Fitem_param_id, Fos_type, Fvalid, Fuse_standard_eva, Fitem_template_id, Fsku_map from t_eva_platform_product where Fproduct_id=41567 and Fplatform_type=1 and Fdelete_flag = 1 limit 1;
select Fevaluate_item from t_eva_item_params  where Fid=11126;
strUserItem:12,17,21,24,36,41,55,59,62,65,71,77,82,224,1078,1083,2171,3245,5530,5534,6931,7642,
strCheckItem:13,17,21,24,36,56,59,61,65,68,73,79,82,223,1077,1091,1633,2171,3246,5534,6931,7641,
strRecordItemTemplateId:204 strCurrItemTemplateId:204

outdata={"body":{"data":{"additionVersion":"0","channelID":"40000001","insured":"0","isItemConsistent":"0","isItemTemplateConsistent":"1","new_product":"1","operatorVersion":"0","orderTime":"2020-10-31 09:32:11","order_id":"7598979","pid":"1001","platformID":"1","platformVersion":"507","productId":"41567","propertyFlag":"0","tagId":"1","unifiedVersion":"67"},"ret":"0","retcode":"0","retinfo":"成功"},"head":{"interface":"insured_judge","msgtype":"response","remark":"","version":"0.01"}}
'''