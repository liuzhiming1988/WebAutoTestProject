#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


'''  估价服务 - 20.回收指导价接口 - http://wiki.huishoubao.net/index.php?s=/138&page_id=10266
     1.需求：【ID1044022】【检测估价】商品检测估价后，新增回收指导价
     https://www.tapd.cn/21967291/prong/stories/view/1121967291001044022?url_cache_key=34414d2b5948d273656a8f0923febb4f&action_entry_type=stories

    2、入参：select：用户选项，json数组的字符串格式 17项 | pid/channelid：pid或渠道id，可都不传或传递其中一个
    productid：产品ID | orderid：用户订单ID | isOverInsurance：是否强制过保 0:否 1:强制过保 默认为0
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

class Eva_Recycle_Guide_Price:
    def eva_option_get(self, channel_id, product_id, pid):
        ''' http://wiki.huishoubao.com/web/#/105?page_id=1595 '''
        ''' platform_type：使用在不需要 pid 和 channle_id 的场景下，优先使用channel_id 或 pid，可不传'''
        param = {"_head": {"_interface": "eva_option_get", "_msgType": "request", "_remark": "hello", "_version": "0.01","_timestamps": "123", "_invokeId": "111", "_callerServiceId": "112002", "_groupNo": "1"},"_param": {"channel_id": channel_id, "product_id": product_id, "pid": pid, "platform_type": ""}}
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

    def eva_recycle_guide_price(self, pid, channelid, productid, orderid, isOverInsurance):
        select = self.eva_option_get(pid=pid, channel_id=channelid, product_id=productid)
        param = {"head":{"interface":"eva_recycle_guide_price","msgtype":"request","remark":"","version":"0.01"},"params":{"ip":"127.0.0.1","cookies":"1111","userid":"0","pid":pid, "channelid":channelid, "productid":productid,"orderid":orderid, "isOverInsurance":isOverInsurance, "select":select}}
        url = "http://evaserver.huishoubao.com/rpc/evaluate"
        headers = {"Content-Type":"application/json;charset=UTF-8"}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())

        print(select)
        hsb_response_print(respone=respone)

if __name__ == '__main__':
    eva_20 = Eva_Recycle_Guide_Price()
    # channelid='10000190'	渠道名称：闲鱼（外部合作）
    # eva_20.eva_recycle_guide_price(pid='1405', channelid='10000190', productid='23009', orderid='7600995', isOverInsurance='1')
    # eva_20.eva_recycle_guide_price(pid='', channelid='40000001', productid='41567', orderid='7632212', isOverInsurance='')
    # eva_20.eva_recycle_guide_price(pid='1001', channelid='40000001', productid='41567', orderid='7632212', isOverInsurance='0')
    # eva_20.eva_recycle_guide_price(pid='1001', channelid='40000001', productid='41567', orderid='7632212', isOverInsurance='1')
    # eva_20.eva_recycle_guide_price(pid='1001', channelid='40000001', productid='41567', orderid='7632212', isOverInsurance='2')
    # eva_20.eva_recycle_guide_price(pid='', channelid='40000001', productid='41567', orderid='7632212', isOverInsurance='0')
    # eva_20.eva_recycle_guide_price(pid='1001', channelid='40000001', productid='63399', orderid='7632212', isOverInsurance='0')
    # eva_20.eva_recycle_guide_price(pid='1001', channelid='40000001', productid='63399', orderid='7632212', isOverInsurance='1')
    eva_20.eva_recycle_guide_price(pid='1001', channelid='40000001', productid='54791', orderid='7634132', isOverInsurance='1') # 2021.06.23
