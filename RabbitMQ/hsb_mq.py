#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : hsb_mq.py
@Author  : liuzhiming
@Time    : 2021/10/20 9:28
"""
import pika
from RabbitMQ.mq_config import TestMQConfig
import sys
import time
import json


class WorkQueuesMQ:
    """
    工作队列模式
    """

    def __init__(self):
        # 远程rabbitMQ服务的配置信息
        self.username = TestMQConfig.USERNAME
        self.pwd = TestMQConfig.PASSWORD
        self.ip_addr = TestMQConfig.IP_ADDR
        self.port_num = TestMQConfig.PORT_NUM
        # 定义授权信息
        self.auth = pika.PlainCredentials(self.username, self.pwd)

    def producer_mq(self, queue_name, message, num=1):
        with pika.BlockingConnection(pika.ConnectionParameters(self.ip_addr, self.port_num, "/", self.auth)) as conn:
            # 创建一个队列，对queue进行durable持久化设为True(持久化第一步)
            channel = conn.channel()
            channel.queue_declare(queue=queue_name, durable=True)

            for i in range(num):
                """
                n RabbitMQ a message can never be sent directly to the queue, 
                it always needs to go through an exchange.
                """
                channel.basic_publish(
                    exchange="",
                    routing_key=queue_name,  # 写明将消息发送给队列
                    body=message,  # 要发送的消息
                    properties=pika.BasicProperties(delivery_mode=2)  # 设置消息持久化(持久化第二步)，将要发送的消息的属性标记为2，表示该消息要持久化
                )
                # 向消息队列发送一条消息
                time.sleep(0.5)
                print(" {} Sent '{}'".format(i, message))


if __name__ == '__main__':
    quene = "EvaToolsCmdProQueue123"
    message_del_redis_key = {"cmd": "DelEvaRedis", "params": []}

    message_add_channel = {"cmd": "CheckEvaV3Channel",
                           "params": {
                                           "cmd": "add",
                                           "channelId": "1196"
                                       }
                           }

    message_del_channel = {
        "cmd": "CheckEvaV3Channel",
        "params": {
            "cmd": "del",
            "channelId": "1196"
        }
    }
    # 价格3.0切换渠道管理http://wiki.huishoubao.com/web/#/347?page_id=15636

    mq = WorkQueuesMQ()
    mq.producer_mq(queue_name=quene, message=json.dumps(message_del_channel))
