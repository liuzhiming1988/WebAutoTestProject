#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang

'''
估价服务 - 估价配置订阅 - 6.价格异常上报 - 价格不合理上报reportInfo内容 - http://wiki.huishoubao.com/web/#/138?page_id=15372
    userId：商家ID  |  productId：产品id  |  productName：产品名称  |  reportId：上报类型ID，1-定价价格不合理，2-缺少定价价格
    reportInfo：上报信息
        skuItems：sku信息（有sku必填）  |  skuItems[0].id：id  |  skuItems[0].name：name   -----无sku机型，整个skuItems可不传
        optionItems	array[object]：机况信息  |  optionItems[0].id：id  | optionItems[0].name：name
        saleLevelId：销售等级ID（有等级时需要传参）  |  saleLevelName：销售等级名称（有等级时需要传参）
        basePriceLevelId：定价等级ID（有等级时需要传参）  |  basePriceLevelName：定价等级名称（有等级时需要传参）
        priceRecordId：价格记录ID
        reportInfo.referSalePrice：销售参考价 （单位：分）
        reportInfo.maxPrice：最高价（单位：分）
        reportInfo.expectPrice：期望价（单位：分）
        reportInfo.desc	string：备注信息（长度小于128字符）
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

    # reportId：上报类型ID，1-定价价格不合理（机型有sku，有定价等级，有价格2.0销售等级）
    # message = json.dumps({"userId":"061104","productId":"41567","productName":"iPhone X","reportId":"1","reportInfo":{"priceRecordId":"9210643019","saleLevelId":"260","saleLevelName":"S","basePriceLevelId":"600","basePriceLevelName":"S","referSalePrice":"292500","maxPrice":"189900","expectPrice":"219900","desc":"【测试环境测试】兄弟，价格太低了，20210611"}})

    # reportId：上报类型ID，1-定价价格不合理（机型无sku，有定价等级，有价格2.0销售等级）
    message = json.dumps({"userId":"061807","productId":"64000","productName":"华为 P40（5G）","reportId":"1","reportInfo":{"priceRecordId":"9210682918","saleLevelId":"260","saleLevelName":"S","basePriceLevelId":"600","basePriceLevelName":"S","referSalePrice":"202500","maxPrice":"229900","expectPrice":"222500","desc":"测试测试测试061807"}})

    # reportId：上报类型ID，1-定价价格不合理（机型无sku，有定价等级，无价格2.0销售等级）
    # message = json.dumps({"userId":"0605003","productId":"1","productName":"iPhone 3GS","reportId":"1","reportInfo":{"optionItems":[{"id":"7532","name":"完好"},{"id":"7559","name":"正常"},{"id":"7575","name":"无法连接电脑"},{"id":"9016","name":"iCloud无法注销"},{"id":"9019","name":"正常开机"},{"id":"9027","name":"全新（未拆封/未激活）"},{"id":"9117","name":"已激活，可还原"}],"saleLevelId": "","saleLevelName": "","basePriceLevelId":"600","basePriceLevelName":"S","priceRecordId":"9210697710","referSalePrice":"168900","maxPrice":"189900","expectPrice":"209900","desc":"【TEST】无sku机型，机况未匹配上销售等级"}})

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
    钉钉通知内容，机况信息，只给到答案项层级就行，关系不大，运营主要关心缺陷项
返回：
    mapUserReport is , userId:052503, reportId:1, productId:54790
    checkFrquency error: user: 052503, productId: 41567 has already reported today
    不触发钉钉通知

入DB：【测试主库 - data_warehouse - t_unusual_price_report】
    `Fid`：'id',
    `Fuser_id`：'商家ID',
    `Fproduct_id`：'产品ID',
    `Fproduct_name`：'产品名称',
    `Freport_id`：'报告类型 1 价格不合理 2 缺少价格',
    `Freport_info`：'上报信息',
    `Freport_time`：'上报时间',

【常见问题分析】
1. SKU 或者 机况的名称未展示，确认 MongoDB 库 t_answer_item表 和 t_question_item表 均能查看对应的数据（有从线上同步）
'''


