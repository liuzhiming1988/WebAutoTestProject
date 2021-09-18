#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 估价服务 - 1.用户估价接口  -  evaluate  (大质检）- http://wiki.huishoubao.net/index.php?s=/138&page_id=2211
	1.对应服务 rpc_evaluate_server（服务器应用名：rpc_evaluate_server）

    入参：pid：回收宝对外入口ip；   channel_id：渠道id（渠道ID赋值：代表使用2B估价模型），（有pid时可为空）
        productid：估价产品id；   userid：登录用户id（未登录用户可为空）；    select：用户选择的估价选项；   isBottomPrice：是否获取保底价,1是,默认为否
    出参：quotation：估算价格，单位分；  evaluateid：估价唯一id（id 会超过int(11)，请不要用int保存）（可通过：12 获取估价记录信息接口，获取信息）
        bottomPrice：保底价/起拍价,单位为分,isBottomPrice不为1时,返回空, isBottomPrice为1时 存在
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print
from price.dingdingTalk_push_demo import dingdingTalk_push_run

class EvaluateUserEva:
    def eva_option_get(self, channel_id, product_id, pid, platform_type):
        ''' http://wiki.huishoubao.com/web/#/105?page_id=1595 '''
        ''' platform_type：使用在不需要 pid 和 channle_id 的场景下，优先使用channel_id 或 pid，可不传'''
        param = {"_head": {"_interface": "eva_option_get", "_msgType": "request", "_remark": "hello", "_version": "0.01","_timestamps": "123", "_invokeId": "111", "_callerServiceId": "112002", "_groupNo": "1"},"_param": {"channel_id": channel_id, "product_id": product_id, "pid": pid, "platform_type": platform_type}}
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

    def evaluate(self, channel_id, product_id, pid, platform_type):
        param = {"head":{"interface":"evaluate","msgtype":"request","remark":"","version":"0.01"},"params":{"cookies":"1111","ip":"127.0.0.1", "pid":pid, "channel_id":channel_id, "productid":product_id, "select":self.eva_option_get(channel_id=channel_id, product_id=product_id, pid=pid, platform_type=platform_type), "userid":"1311"}}
        url = "http://evaserver.huishoubao.com/rpc/evaluate"
        headers = {"Content-Type":"application/json"}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        hsb_response_print(respone=respone)

if __name__ == '__main__':
    evaluate_user_eva = EvaluateUserEva()
    # evaluate_user_eva.evaluate(channel_id='40000001', product_id='41567', pid='', platform_type='') # iPhone x
    # evaluate_user_eva.evaluate(channel_id='40000001', product_id='63398', pid='', platform_type='') # 华为 Mate 30

    # 2020.03.13 优化先计算差值再计算等级算法  机型名称：iPhone 6   机型ID：30748
    # select=["2171","44","53","56","58","63","34","65","15","23","69","20","3246","3244","17","1083","223","77","82"]
    # evaluate_user_eva.evaluate(channel_id='40000001', product_id='30748', pid='', platform_type='') # iPhone 6

    # evaluate_user_eva.evaluate(channel_id='40000001', product_id='4006', pid='1001', platform_type='') # 华为 G350

    # for i in range(10):
    evaluate_user_eva.evaluate(channel_id='40000001', product_id='66045', pid='1001', platform_type='') # 有错误数据的机型
    # evaluate_user_eva.evaluate(channel_id='40000001', product_id='64001', pid='1001', platform_type='') # 无错误数据的机型
    # evaluate_user_eva.evaluate(channel_id='10000255', product_id='64247', pid='', platform_type='10')  # 有错误数据的机型
    # evaluate_user_eva.evaluate(channel_id='10000255', product_id='64001', pid='', platform_type='10')  # 无错误数据的机型

'''
indata={"head": {"interface": "evaluate", "msgtype": "request", "remark": "", "version": "0.01"}, "params": {"cookies": "1111", "ip": "127.0.0.1", "pid": "1001", "channel_id": "40000001", "productid": "4006", "select": ["23"], "userid": "1311"}}

hset Eva_PId_Cache 1001 {"channelFlag":"1","channelId":"40000001","platformId":"1","platformName":"2C","tagId":"1","time":"1602746712"}
Platform Eva Version: 90 standardPrice:700

整机项: 700*100/100 = 700
系数特殊规则:700 = 700
选项分组命中等级:100 lType:1 lValue:101 uType:1 uValue:101
选项分组下限百分比:(700*101)/100=707
选项分组上限百分比:(700*101)/100=707
选项分组取下限:707
先计算选项分组再计算差值算法 差值:(707+700*0/100+0)*100/100 = 707

outdata={"body":{"data":{"evaluateid":"20104299","quotation":"700"},"ret":"0","retcode":"0","retinfo":"成功"},"head":{"interface":"evaluate","msgtype":"response","remark":"","version":"0.01"}}
'''