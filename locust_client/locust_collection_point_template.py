#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : locust_collection_point_template.py
@Author  : liuzhiming
@Time    : 2021/10/14 16:06
"""
# 参考资料：https://www.jianshu.com/p/3a7ab6903e48
# https://zhuanlan.zhihu.com/p/143892229

from locust import HttpUser, TaskSet, task, between, events
from gevent._semaphore import Semaphore
import hashlib, requests, json, os, random
import hashlib, requests
from locust import SequentialTaskSet


# 定义md5加密函数
def Md5Enerypt(Lstr):
    '''MD5加密方法封装'''
    m = hashlib.md5()
    m.update(Lstr.encode("utf-8"))
    # print(m.hexdigest())
    return m.hexdigest()


def hsb_eva_ipProxy_test():
    '''1. vpc测试-环境'''
    hsb_eva_ipProxy = {'http': '193.112.170.216'}
    # print('\033[31m您调用的是『价格FT-vpc测试环境』，HOSTS指向IP为：『{0}』\033[0m'.format(hsb_eva_ipProxy['http']))
    return hsb_eva_ipProxy


all_locusts_spawned = Semaphore()
all_locusts_spawned.acquire()


def on_hatch_complete(**kwargs):
    """
    Select_task类的钩子方法
    :param kwargs:
    :return:
    """
    all_locusts_spawned.release()


events.spawning_complete.add_listener(on_hatch_complete)

n = 0  # 标识虚拟用户


class UserBehavior(TaskSet):

    def login(self):
        global n
        n += 1
        print("第{}个虚拟用户开始启动，并登录".format(n))

    def logout(self):
        print("退出登录")

    def on_start(self):
        """
        初始化函数，初始化每个虚拟用户时需要做的操作
        :return:
        """
        self.login()

        all_locusts_spawned.wait()

    @task(2)
    def test1(self):
        param = {"_head": {"_interface": "eva_option_get", "_msgType": "request", "_remark": "eva_product_v3",
                           "_version": "0.01", "_timestamps": "123", "_invokeId": "eva_product_v3",
                           "_callerServiceId": "112002", "_groupNo": "1"},
                 "_param": {"channel_id": "10000060", "product_id": "41567", "pid": "1260"}}
        url = "http://prdserver.huishoubao.com/eva_product_v3/eva_option_get"
        md5value = json.dumps(param) + "_" + "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),
                   "HSB-OPENAPI-CALLERSERVICEID": "112002"}
        with self.client.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test(),
                              catch_response=True) as response:
            print("【价格3.0】获取估价选项")

    @task(5)
    def test2(self):
        param = {"_head": {"_interface": "eva_option_get", "_msgType": "request", "_remark": "eva_product_v3",
                           "_version": "0.01", "_timestamps": "123", "_invokeId": "eva_product_v3",
                           "_callerServiceId": "112002", "_groupNo": "1"},
                 "_param": {"channel_id": "10000060", "product_id": "41567", "pid": "1260"}}
        url = "http://prdserver.huishoubao.com/eva_product_v3/eva_option_get"
        md5value = json.dumps(param) + "_" + "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),
                   "HSB-OPENAPI-CALLERSERVICEID": "112002"}
        with self.client.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test(),
                              catch_response=True) as response:
            print("【价格3.0】获取估价选项")

    @task(6)
    def test3(self):
        param = {"_head": {"_interface": "eva_option_get", "_msgType": "request", "_remark": "eva_product_v3",
                           "_version": "0.01", "_timestamps": "123", "_invokeId": "eva_product_v3",
                           "_callerServiceId": "112002", "_groupNo": "1"},
                 "_param": {"channel_id": "10000060", "product_id": "41567", "pid": "1260"}}
        url = "http://prdserver.huishoubao.com/eva_product_v3/eva_option_get"
        md5value = json.dumps(param) + "_" + "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),
                   "HSB-OPENAPI-CALLERSERVICEID": "112002"}
        # locust能收集到性能指标，需要用self.client.post()方法发起请求
        with self.client.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test(),
                              catch_response=True) as response:
            print("【价格3.0】获取估价选项")

    def on_stop(self):
        """tearDown函数，虚拟用户在退出时，需要执行的操作"""
        self.logout()


class WebsiteUser(HttpUser):
    host = "http://127.0.0.1"
    tasks = [UserBehavior]

    wait_time = between(1, 2)  # 用于确定模拟用户在执行任务之间将等待多长时间;单位秒


if __name__ == '__main__':
    # 加上--web-host 参数，防止IP地址访问不了https://blog.csdn.net/lluozh2015/article/details/105586525/
    os.system("locust -f locust_collection_point_template.py --web-host=0.0.0.0")

    # 设置固定的运行时长
    # locust -f locust_collection_point_template.py --headless -u 1000 -r 100 --run-time 1h30m --csv=example --stop-timeout 99
    """
    常用：
    --headless      无web界面运行脚本
    -u 1000 -r 100      共有1000个用户，每秒启动100个
    --run-time 1h30m       共运行1小时30分
    --csv=example       脚本目录下，生成含数据的csv文件
    
    很少用：
    --expect-workers        分布式无web界面的运行要在配置文件指定该参数
    --stop-timeout 99       到指定时间后，再停99秒结束运行
    
    """
