#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : t_locust_v2_base_price_evaluate.py
@Author  : liuzhiming
@Time    : 2021/10/26 11:43
"""

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test, hsb_eva_ipProxy_k8s_test
from price.hsb_MD5_Enerypt import get_price_headers, res_print
from locust import task, between, TaskSet, FastHttpUser, HttpUser
import requests

"""
locust V2.4.0
接口：http://codserver.huishoubao.com/detect/product_check_item
wiki：http://wiki.huishoubao.com/web/#/105?page_id=3295

接口：http://bpeserver.huishoubao.com/adjustment_price/sale_apply_price
wiki：http://wiki.huishoubao.com/web/#/138?page_id=15625
"""


class SaleApplyPriceCase(TaskSet):

    # 初始化方法，相当于setup
    def on_start(self):
        pass

    """
    
    """
    @task
    def sale_apply_price(self):
        planId = "3"
        productId = "41567"
        evaType = "3"
        skus = ['8012', '130', '17', '2236', '36', '42', '2242']
        options = ['9015', '9019', '9027', '9028', '9035', '9039', '9047', '7481', '9057', '9059', '9062', '9067',
                   '9071', '9074', '7559', '9077', '9079', '7570', '7574', '9082', '9084', '7589', '9090', '9094',
                   '9098', '9102', '9106', '9111', '9117', '9120']
        ip = "10.0.11.88"
        freqLimitType = "0"
        url = "http://bpeserver.huishoubao.com/adjustment_price/sale_apply_price"
        param = {"_head": {"_interface": "sale_apply_price", "_msgType": "request", "_remark": "", "_version": "0.01",
                           "_timestamps": "1525332832", "_invokeId": "lzm_adjustPrice_locust",
                           "_callerServiceId": "116006", "_groupNo": "1"},
                 "_param": {"planId": planId, "productId": productId, "evaType": evaType, "skuItem": skus,
                            "optItem": options, "ip": ip, "userId": "1895", "freqLimitType": freqLimitType}}
        # res = self.client.post(url, json=param, headers=get_price_headers(param), catch_response=True,
        #                        name="get_sale_price", proxies=hsb_eva_ipProxy_k8s_test())
        with self.client.post(url, json=param, headers=get_price_headers(param), proxies=hsb_eva_ipProxy_k8s_test(),
                              name="获取销售价V2.0", catch_response=True) as res:
            # print(res.text)
            if res.status_code == 200 and res.json()["_data"]["_errCode"] == "0":
                print("请求成功")
                res.success()
            else:
                res.failure("sale_apply_price接口失败！")

    # 结束方法，相当于tearDown
    def on_stop(self):
        pass


# 定义一个运行类
class UserRun(HttpUser):
    host = "http://127.0.0.1"
    tasks = [SaleApplyPriceCase]   # 指定任务类名称

    wait_time = between(0, 0)  # 用于确定模拟用户在执行任务之间将等待多长时间;单位秒


if __name__ == '__main__':
    # 执行locust测试
    os.system("locust -f t_locust_v2_base_price_evaluate.py --web-host=127.0.0.1")
