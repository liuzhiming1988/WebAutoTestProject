#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : locust_interface_template.py
@Author  : liuzhiming
@Time    : 2021/10/14 11:19
"""

from locust import HttpUser, FastHttpUser, TaskSet, SequentialTaskSet, constant, between, task, events
import os

"""
https://cloud.tencent.com/developer/article/1594240
locust快速入门_春天的BO菜-CSDN博客_locust https://blog.csdn.net/legend818/article/details/117897944
【本例场景说明】
1. 按顺序执行接口
2. 登录一次，获取10次店铺信息
3. 序号标识虚拟用户
"""


@events.test_start.add_listener
def on_test_start(**kwargs):
    print("=====测试最开始提示=====")


@events.test_stop.add_listener
def on_test_top(**kwargs):
    print("======测试结束了的提示===")


virtual_user_num = 0  # 标识虚拟用户序号


# 自定义变量
class CustomVariable:
    headers = {"Content-Type": "application/json; charset=utf-8"}       # 请求头
    protocol = "https://"       # 协议
    domain = "hsbpro.huishoubao.com"        # 域名
    sms_code = "666666"     # 短信验证码


class TaskSetTemplate(SequentialTaskSet):
    """
    TaskSet: 为并行执行类
    SequentialTaskSet: 为串行执行类
    """

    data = {}   # 多个接口之间共享数据（将接口返回的关键字段加入字典中共用）单个虚拟用户之间使用

    def on_start(self):
        """每个虚拟用户在执行任务前会调用"""
        global virtual_user_num
        virtual_user_num += 1
        self.data = {"index": virtual_user_num}  # index 标识虚拟用户的序号
        print("第{}个虚拟用户已启动".format(self.data.get("index", "null")))

    @task(2)
    def login(self):
        headers = {"Content-Type": "application/json; charset=utf-8"}
        url = "https://hsbpro.huishoubao.com/hsbpro"
        param = {"_head": {"_remark": "", "_appVersion": "5.0.0", "_version": "0.01",
                           "_groupNo": "1", "longitude": 113.94299928073816, "latitude": 22.532460629273437,
                           "_interface": "login_captcha", "_timestamps": "1635842033",
                           "_invokeId": "iOS_C854F1C2-5E70-44D3-853C-655BBA17E54E_1635842033",
                           "_msgType": "request", "channelStr": "appstore", "_callerServiceId": "111111"},
                 "_param": {
                     "phone": "18676702152",
                     "captcha": CustomVariable.sms_code,
                     "permissions": "0"
                 }
                 }
        with self.client.post(url, json=param, headers=headers, name="专业版-登录接口", catch_response=True) as res:
            print(res.text)
            if res.status_code == 200 and res.json()["_data"]["_errCode"] == "0":
                print("请求成功")
                self.data = dict(self.data, **res.json()["_data"]["data"])
                res.success()
            else:
                res.failure("登录失败！{}".format(res.json()["_data"]["_errStr"]))

    @task(3)
    def get_merchant_info(self):
        headers = {"Content-Type": "application/json; charset=utf-8"}
        url = "https://hsbpro.huishoubao.com/hsbpro"
        param = {"_head": {"_remark": "", "_appVersion": "5.0.0", "_version": "0.01",
                           "_groupNo": "1", "longitude": 113.94299928073816, "latitude": 22.532460629273437,
                           "_interface": "get_merchant_info", "_timestamps": "1635842033",
                           "_invokeId": "iOS_C854F1C2-5E70-44D3-853C-655BBA17E54E_1635842033",
                           "_msgType": "request", "channelStr": "appstore", "_callerServiceId": "111111"},
                 "_param": {
                     "merchantId": self.data.get("merchant_id", "null"),
                     "permissions": "0",
                     "login_token": self.data.get("login_token", "null"),
                     "queryType": "tagInfo"
                 }
                 }
        with self.client.post(url, json=param, headers=headers, name="专业版-获取店铺信息", catch_response=True) as res:
            print(res.text)
            if res.status_code == 200 and res.json()["_data"]["_errCode"] == "0":
                print("请求成功")
                res.success()
            else:
                print("请求失败")
                res.failure("请求失败！{}".format(res.json()["_data"]["_errStr"]))

    def on_stop(self):
        """每个虚拟用户在执行结束后会调用"""
        print("第{}个虚拟用户已停止".format(self.data.get("index", "null")))


class MyTasks(HttpUser):
    host = "http://127.0.0.1"  # 测试环境的地址（域名、IP+端口）
    tasks = [TaskSetTemplate]  # 指定测试任务类
    wait_time = between(1, 2)  # 用于确定模拟用户在执行任务之间将等待多长时间;单位秒
    # wait_time = constant(3)   # 每次请求等待时间


if __name__ == '__main__':
    # pycharm中执行
    # 加上--web-host 参数，防止IP地址访问不了https://blog.csdn.net/lluozh2015/article/details/105586525/
    os.system("locust -f locust_interface_template.py --web-host=127.0.0.1")

    # 命令行中执行，带web界面
    # locust -f locust_interface_template.py --web-host=0.0.0.0

    # 不带界面执行
    # 设置固定的运行时长
    # locust -f locust_interface_template.py --headless -u 1000 -r 100 --run-time 1h30m --csv=example --stop-timeout 99

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
