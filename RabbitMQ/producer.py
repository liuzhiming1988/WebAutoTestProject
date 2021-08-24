#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : producer.py
@Author  : liuzhiming
@Time    : 2021/8/20 15:19
"""

from RabbitMQ.test_mq import *

queue_n = "test_ming"
message_str1 = "mq test-001: today is a good day!!!%%%"
message_str2 = "mq test-002: I will back!!!======"

# 工作队列模式
# work_mq = WorkQueuesMQ()
# work_mq.producer_mq("TestMQ_C", message_str2, 10)

# 发布/订阅模式生产者
# publish_mq = PublishMQ()
# publish_mq.producer_mq("test_exchange", message_str, 15)

# 路由模式
# route_mq = RouteMQ()
# route_mq.producer_mq("routeTestExchange", "route001", message_str1, 10)
# route_mq.producer_mq("routeTestExchange", "route002", message_str2, 20)

# # topic模式
topic_mq = TopicMQ()
topic_mq.producer_mq(exchange_name="topic_test", route_key="person.p", queue_name="topic_testing", message=message_str1, num=10)

