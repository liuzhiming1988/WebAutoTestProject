#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : test_mq.py
@Author  : liuzhiming
@Time    : 2021/8/18 11:36
"""

import pika
import sys
import time


class DebugMQ:

    def __init__(self):
        # 远程rabbitMQ服务的配置信息
        self.username = "hjx"
        self.pwd = "123456"
        self.ip_addr = "111.230.107.156"
        self.port_num = 5672
        # 消息队列服务的连接和队列的创建
        self.auth = pika.PlainCredentials(self.username, self.pwd)
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(self.ip_addr, self.port_num, "/", self.auth))
        self.channel = self.conn.channel()

    def producer_mq(self, quene_name, message, num):

        # 创建一个名为balance的队列，对queue进行durable持久化设为True(持久化第一步)
        self.channel.queue_declare(queue=quene_name, durable=True)

        for i in range(num):
            # n RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
            self.channel.basic_publish(
                    exchange="",
                    routing_key=quene_name,  # 写明将消息发送给队列
                    body=message,  # 要发送的消息
                    properties=pika.BasicProperties(delivery_mode=2)  # 设置消息持久化(持久化第二步)，将要发送的消息的属性标记为2，表示该消息要持久化
                )
            # 向消息队列发送一条消息
            time.sleep(0.5)
            print(" {} Sent '{}'".format(i, message))

        # self.conn.close()   # 关闭消息队列服务的连接

    @staticmethod
    def callback(ch, method, properties, body):
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(" [{}] Received {}".format(time_str, body))
        time.sleep(0.2)

    def consumer_mq(self, quene_name):

        self.channel.basic_consume(queue=quene_name, on_message_callback= self.callback, auto_ack=True)
        self.channel.start_consuming()    # 启动消费
        # self.conn.close()


if __name__ == '__main__':
    # quene = "test_ming"
    # message_str = b"for test xianyu by zhiming==="
    # mq = DebugMQ()
    # # mq.producer_mq(quene, message_str, 20)
    # # time.sleep(5)
    # mq.consumer_mq(quene)
    # mq.conn.close()
    bb = b'{\r\n        "type":"2",//1\xe8\xa1\xa8\xe7\xa4\xba\xe5\x95\x86\xe5\x93\x81\xe4\xba\x8b\xe4\xbb\xb6\xef\xbc\x8c2\xe8\xa1\xa8\xe7\xa4\xba\xe4\xb8\xbb\xe8\xae\xa2\xe5\x8d\x95\xe4\xba\x8b\xe4\xbb\xb6\xef\xbc\x8c3\xe8\xa1\xa8\xe7\xa4\xba\xe8\xae\xa2\xe5\x8d\x95\xe9\x80\x80\xe8\xb4\xa7\xe9\x80\x80\xe6\xac\xbe\xe4\xba\x8b\xe4\xbb\xb6\r\n        "originalMessage":"{\\"item_id\\":1,\\"biz_order_id\\":12378923,\\"order_status\\":1}",//"type":"2"\xe6\x97\xb6 \xe7\xbb\x93\xe6\x9e\x84\xe4\xbd\x93\xef\xbc\x9border_status\xe4\xb8\xba1\xef\xbc\x9a\xe8\xae\xa2\xe5\x8d\x95\xe5\xb7\xb2\xe5\x88\x9b\xe5\xbb\xba\xe3\x80\x812\xef\xbc\x9a\xe8\xae\xa2\xe5\x8d\x95\xe5\xb7\xb2\xe4\xbb\x98\xe6\xac\xbe\xe3\x80\x813\xef\xbc\x9a\xe5\xb7\xb2\xe5\x8f\x91\xe8\xb4\xa7\xe3\x80\x814\xef\xbc\x9a\xe4\xba\xa4\xe6\x98\x93\xe6\x88\x90\xe5\x8a\x9f\xe3\x80\x815\xef\xbc\x9a\xe5\xb7\xb2\xe9\x80\x80\xe6\xac\xbe\xe3\x80\x816\xef\xbc\x9a\xe4\xba\xa4\xe6\x98\x93\xe5\x85\xb3\xe9\x97\xad\r\n    }'
    aa = "fldadfhla发"

    print(bytes(aa, encoding="utf-8"))  # 字符串转换为字节
    print(bb.decode())    # 字节转换为str对象

