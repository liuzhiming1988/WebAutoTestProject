#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : consumer001.py
@Author  : liuzhiming
@Time    : 2021/8/20 14:23
"""

from RabbitMQ.test_mq import *

# 工作队列模式
# work_mq = WorkQueuesMQ()
# work_mq.consumer_mq("TestMQ_C")

# 发布/订阅者模式，消费者实例
# publish_mq = PublishMQ()
# publish_mq.consumer_mq("test_exchange")


# 路由模式
# route_mq1 = RouteMQ()
# route_mq1.consumer_mq("routeTestExchange", "route001")

# topic模式
topic_mq = TopicMQ()
topic_mq.consumer_mq(exchange_name="topic_test", queue_name="", route_key="person.*")   # .*表示匹配后边一个单词
