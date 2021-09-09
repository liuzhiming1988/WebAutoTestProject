#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang

'''
估价服务 - 估价配置订阅 - 6.价格异常上报 - 价格不合理上报reportInfo内容 - http://wiki.huishoubao.com/web/#/138?page_id=15372
    userId：商家ID  |  productId：产品id  |  productName：产品名称  |  reportId：上报类型ID，1-定价价格不合理，2-缺少定价价格
'''

import pika
import json

''' 生产者（producter）：队列消息的产生者，负责生产消息，并将消息传入队列'''

def producter_main():
    # 1. mq用户名和密码
    credentials = pika.PlainCredentials('hjx', '123456')

    # 2. 虚拟队列需要指定参数 virtual_host，如果是默认的可以不填。
    ''' pika.BlockingConnection 连接MQ'''
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='111.230.107.156', port=5672, virtual_host='eva_vhost', credentials=credentials))
    # 3. 创建频道
    channel=connection.channel()

    # 4. 声明或创建消息队列，消息将在这个队列传递，如不存在，则创建
    '''
    背景：MQ默认建立的是临时 queue、exchange，如果不声明持久化，一旦 RabbitMQ 挂掉，queue、exchange 将会全部丢失
         所以我们一般在创建 queue或者exchange 的时候会声明 持久化。
    4.1. queue 声明持久化;  声明消息队列，消息将在这个队列传递，如不存在，则创建
         durable = True 代表消息队列持久化存储，False 非持久化存储
    备注：durable=True 队列持久化的值需要一致（生产者 和 消费者当中队列的durable的参数尽量保持一致）
    4.2. exchange 声明持久化； 声明exchange，由exchange指定消息在哪个队列传递，如不存在，则创建
         durable=True 代表 exchange持久化存储，False非持久化存储。
    注意：如果已存在一个非持久化的 queue 或 exchange ，执行上述代码会报错，因为当前状态不能更改 queue 或 exchange 存储属性，需要删除重建
         如果 queue 和 exchange 中一个声明了持久化，另一个没有声明持久化，则不允许绑定
    '''
    result = channel.queue_declare(queue='unusual_price_report_queue', durable=True)

    # 发布与订阅借助交换机（exchange），模式1：fanout，传递到 exchange 的消息将会发送到所有与其绑定的 queue 上
    # result = channel.exchange_declare(exchange='eva_2_bijia_compare_price_17', durable=True, exchange_type='fanout')

    # 消息发送至 exchange，exchange 根据 路由键（routing_key）转发到相对应的 queue 上
    # result = channel.exchange_declare(exchange='eva_2_bijia_compare_price_17', durable=True, exchange_type='direct')

    # reportId：上报类型ID，2 - 缺少定价价格
    message = json.dumps({"userId":"052504","productId":"54789","productName":"iPhone XS Max","reportId":"2"})

    # 5. 向队列插入数值 routing_key 是队列（queue）名
    ''' 5.1. 消息持久化； 向队列插入数值，routing_key是队列名。
        delivery_mode=2 声明消息在队列中持久化，delivery_mod=1 消息非持久化 '''
    channel.basic_publish(exchange='', routing_key='unusual_price_report_queue', body=message, properties=pika.BasicProperties(delivery_mode=2))
    print(message)

    # 6. 关闭连接
    connection.close()

if __name__ == '__main__':
    # for i in range(20):
    #     producter_main()
    producter_main()

'''
MQ  |  virtual_host='eva_vhost'   |  queue='unusual_price_report_queue'
【钉钉通知 限频】【EvaluateToolsGo】
需求：限制用户操作提醒的频次，同个用户、每天（自然日）、同个机型只能提醒一次，再次点击时toast提示“已发送提醒”，不再记录，也不再钉钉通知
返回： 
    mapUserReport is , userId:052504, reportId:2, productId:41567
    checkFrquency error: user: 052504, productId: 41567 has already reported today
    不触发钉钉通知
    
入DB：【测试主库 - data_warehouse - t_unusual_price_report】
    `Fid`：'id',
    `Fuser_id`：'商家ID',
    `Fproduct_id`：'产品ID',
    `Fproduct_name`：'产品名称',
    `Freport_id`：'报告类型 1 价格不合理 2 缺少价格',
    `Freport_info`：'上报信息',
    `Freport_time`：'上报时间',
'''