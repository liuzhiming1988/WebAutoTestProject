#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : test_mq.py
@Author  : liuzhiming
@Time    : 2021/8/18 11:36
"""

import pika
from RabbitMQ.mq_config import TestMQConfig
import sys
import time


class MQSimple:
    """简单模式
    """

    def __init__(self):
        # 远程rabbitMQ服务的配置信息
        self.username = TestMQConfig.USERNAME
        self.pwd = TestMQConfig.PASSWORD
        self.ip_addr = TestMQConfig.IP_ADDR
        self.port_num = TestMQConfig.PORT_NUM
        # 消息队列服务的连接和队列的创建
        self.auth = pika.PlainCredentials(self.username, self.pwd)
        self.conn = pika.BlockingConnection(
            pika.ConnectionParameters(self.ip_addr, self.port_num, "/", self.auth))
        self.channel = self.conn.channel()

    def producer_mq(self, queue_name, message, num=1):

        # 创建一个名为balance的队列，对queue进行durable持久化设为True(持久化第一步)
        self.channel.queue_declare(queue=queue_name, durable=True)

        for i in range(num):
            # n RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
            self.channel.basic_publish(
                    exchange="",
                    routing_key=queue_name,  # 写明将消息发送给队列
                    body=message+str(i),  # 要发送的消息
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

        with pika.BlockingConnection(pika.ConnectionParameters(self.ip_addr,self.port_num, "/", self.auth)) as conn:
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
                        body=message+str(i),  # 要发送的消息
                        properties=pika.BasicProperties(delivery_mode=2)  # 设置消息持久化(持久化第二步)，将要发送的消息的属性标记为2，表示该消息要持久化
                    )
                # 向消息队列发送一条消息
                time.sleep(0.5)
                print(" {} Sent '{}'".format(i, message))


    @staticmethod
    def callback(ch, method, properties, body):
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(" [{}] Received {}".format(time_str, body))
        time.sleep(2)   # 模拟真实处理方法耗时
        # 回调结束发送确认信号(确保消费者意外结束而导致消息丢失)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def consumer_mq(self, queue_name):

        with pika.BlockingConnection(pika.ConnectionParameters(self.ip_addr,self.port_num, "/", self.auth)) as conn:
            channel = conn.channel()
            channel.basic_consume(queue=queue_name,
                                  # auto_ack=True,  # 自动向服务器发送确认信号
                                  on_message_callback= self.callback
                            )
            channel.basic_qos(prefetch_count=1)     # 只有在消费者发送确认，确认它的上一个任务已经完成，它才会收到下一个
            channel.start_consuming()    # 启动消费


class PublishMQ:
    """
    发布、订阅模式
    """

    def __init__(self):
        # 远程rabbitMQ服务的配置信息
        self.username = TestMQConfig.USERNAME
        self.pwd = TestMQConfig.PASSWORD
        self.ip_addr = TestMQConfig.IP_ADDR
        self.port_num = TestMQConfig.PORT_NUM
        # 定义授权信息
        self.auth = pika.PlainCredentials(self.username, self.pwd)

    def producer_mq(self, exchange_name, message, num=1):
        with pika.BlockingConnection(pika.ConnectionParameters(self.ip_addr, self.port_num, "/", self.auth)) as conn:
            channel = conn.channel()
            channel.exchange_declare(exchange=exchange_name, exchange_type="fanout")    # 创建exchange，类型为fanout

            for i in range(num):
                """
                n RabbitMQ a message can never be sent directly to the queue, 
                it always needs to go through an exchange.
                """
                channel.basic_publish(
                    exchange=exchange_name,
                    routing_key="",  # 写明将消息发送给队列
                    body=message  # 要发送的消息
                )
                # 向消息队列发送一条消息
                time.sleep(0.5)
                print(" {} Sent '{}'".format(i, message))

    @staticmethod
    def callback(ch, method, properties, body):
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(" [{}] Received {}".format(time_str, body))
        time.sleep(2)  # 模拟真实处理方法耗时
        # 回调结束发送确认信号(确保消费者意外结束而导致消息丢失)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def consumer_mq(self, exchange_name):
        with pika.BlockingConnection(pika.ConnectionParameters(self.ip_addr, self.port_num, "/", self.auth)) as conn:
            # 创建一个队列，对queue进行durable持久化设为True(持久化第一步)
            channel = conn.channel()
            channel.exchange_declare(exchange=exchange_name, exchange_type="fanout")  # 创建exchange，类型为fanout
            result = channel.queue_declare(queue="", exclusive=True)
            queue_name = result.method.queue

            channel.queue_bind(exchange=exchange_name, queue=queue_name)

            channel.basic_consume(queue=queue_name,
                                  # auto_ack=True,  # 自动向服务器发送确认信号
                                  on_message_callback=self.callback
                                  )
            channel.basic_qos(prefetch_count=1)  # 只有在消费者发送确认，确认它的上一个任务已经完成，它才会收到下一个
            channel.start_consuming()  # 启动消费


class RouteMQ:
    """
    路由模式
    """
    def __init__(self):
        # 远程rabbitMQ服务的配置信息
        self.username = TestMQConfig.USERNAME
        self.pwd = TestMQConfig.PASSWORD
        self.ip_addr = TestMQConfig.IP_ADDR
        self.port_num = TestMQConfig.PORT_NUM
        # 定义授权信息
        self.auth = pika.PlainCredentials(self.username, self.pwd)

    def producer_mq(self, exchange_name, route_key, message, num):
        with pika.BlockingConnection(pika.ConnectionParameters(self.ip_addr, self.port_num, "/", self.auth)) as conn:
            channel = conn.channel()
            channel.exchange_declare(exchange=exchange_name, exchange_type="direct", durable=True)    # 创建exchange，类型为direct

            for i in range(num):
                """
                n RabbitMQ a message can never be sent directly to the queue, 
                it always needs to go through an exchange.
                """
                channel.basic_publish(
                    exchange=exchange_name,
                    routing_key=route_key,  # 写明将消息发送给队列
                    body=message+str(i)  # 要发送的消息
                )
                # 向消息队列发送一条消息
                time.sleep(0.5)
                print(" {} Sent '{}'".format(i, message+str(i)))

    @staticmethod
    def callback(ch, method, properties, body):
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(" [{}] Received {}".format(time_str, body))
        time.sleep(2)  # 模拟真实处理方法耗时
        # 回调结束发送确认信号(确保消费者意外结束而导致消息丢失)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def consumer_mq(self, exchange_name, route_key):
        with pika.BlockingConnection(pika.ConnectionParameters(self.ip_addr, self.port_num, "/", self.auth)) as conn:
            channel = conn.channel()
            channel.exchange_declare(exchange=exchange_name, exchange_type="direct")  # 创建exchange，类型为direct
            result = channel.queue_declare(queue="", exclusive=True)
            queue_name = result.method.queue

            channel.queue_bind(exchange=exchange_name,
                               queue=queue_name,
                               routing_key=route_key)

            channel.basic_consume(queue=queue_name,
                                  # auto_ack=True,  # 自动向服务器发送确认信号
                                  on_message_callback=self.callback
                                  )
            channel.basic_qos(prefetch_count=1)  # 只有在消费者发送确认，确认它的上一个任务已经完成，它才会收到下一个
            channel.start_consuming()  # 启动消费


class TopicMQ:
    """
    主题模式
    """
    def __init__(self):
        # 远程rabbitMQ服务的配置信息
        self.username = TestMQConfig.USERNAME
        self.pwd = TestMQConfig.PASSWORD
        self.ip_addr = TestMQConfig.IP_ADDR
        self.port_num = TestMQConfig.PORT_NUM
        # 定义授权信息
        self.auth = pika.PlainCredentials(self.username, self.pwd)

    def producer_mq(self, exchange_name, route_key, queue_name, message, num):
        with pika.BlockingConnection(pika.ConnectionParameters(self.ip_addr, self.port_num, "/", self.auth)) as conn:
            channel = conn.channel()
            channel.exchange_declare(exchange=exchange_name, exchange_type="topic", durable=True)    # 创建exchange，类型为topic
            # channel.queue_declare(queue="", exclusive=True, durable=True)    # 自动生成唯一的队列，并在使用完后自动销毁
            channel.queue_declare(queue=queue_name, durable=True)

            for i in range(num):
                """
                n RabbitMQ a message can never be sent directly to the queue, 
                it always needs to go through an exchange.
                """
                channel.basic_publish(
                    exchange=exchange_name,
                    routing_key=route_key,    # 写明将消息发送给队列
                    body=message+str(i),    # 要发送的消息
                    properties=pika.BasicProperties(delivery_mode=2)     # 消息持久化
                )
                # 向消息队列发送一条消息
                time.sleep(0.2)
                print(" {} Sent '{}'".format(i, message+str(i)))

    @staticmethod
    def callback(ch, method, properties, body):
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(" [{}] Received {}".format(time_str, body))
        time.sleep(2)  # 模拟真实处理方法耗时
        # print("【ch】{}".format(ch))
        # print("【method】{}".format(method))
        # print("【properties】{}".format(properties))
        # print("【body】{}".format(body))
        # 回调结束发送确认信号(确保不因为消费者意外结束而导致消息丢失)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def consumer_mq(self, exchange_name, queue_name, route_key):
        with pika.BlockingConnection(pika.ConnectionParameters(self.ip_addr, self.port_num, "/", self.auth)) as conn:
            channel = conn.channel()
            channel.exchange_declare(exchange=exchange_name, exchange_type="topic", durable=True)  # 创建exchange，类型为topic
            # result = channel.queue_declare(queue="", exclusive=True, durable=True)
            # queue_name = result.method.queue     # 自动生成唯一的队列，并在使用完后自动销毁
            channel.queue_declare(queue=queue_name, durable=True)

            channel.queue_bind(exchange=exchange_name,
                               queue=queue_name,
                               routing_key=route_key)

            channel.basic_consume(queue=queue_name,
                                  # auto_ack=True,  # 自动向服务器发送确认信号
                                  on_message_callback=self.callback
                                  )
            channel.basic_qos(prefetch_count=1)  # 只有在消费者发送确认，确认它的上一个任务已经完成，它才会收到下一个
            channel.start_consuming()  # 启动消费


if __name__ == '__main__':

    # queue_n = "test_ming"
    message_str = "test mq==={}"
    # mq = WorkQueuesMQ()
    # # mq.producer_mq(quene, message_str, 20)
    # # time.sleep(5)
    # mq.consumer_mq(quene)

    # 发布/订阅模式生产者
    # publish_mq = PublishMQ()
    # publish_mq.producer_mq("test_exchange", message_str, 15)

    # 路由模式
    route_mq = RouteMQ()
    route_mq.producer_mq("routeTestExchane", "route001", message_str, 88)

    # print(bytes(aa, encoding="utf-8"))  # 字符串转换为字节
    # print(bb.decode())    # 字节转换为str对象

