#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : mongo_client.py
@Author  : liuzhiming
@Time    : 2021/9/22 15:58
"""

import pymongo
from sshtunnel import SSHTunnelForwarder
import json

class TestVpcMongoConfig:

    ssh_host = ("129.204.129.154", 22)
    ssh_username = "zhangjinfa"
    ssh_password = "qJ453CqH8*ew"

    mongodb_host = "10.0.40.51"
    mongodb_port = 27017
    username = "admin"
    password = "test_price"

local_config = {
    "ssh_host": ("129.204.129.154", 22),
    "ssh_username": "zhangjinfa",
    "ssh_password": "",
    "mongodb_host": "10.0.11.14",
    "mongodb_port": 27017,
    "username": "admin",
    "password": "12345678",
}

class MongoSSHClient:

    def __init__(self):
        # 直连MongoDB
        # self.client = pymongo.MongoClient(
        #     host=TestVpcMongoConfig.mongodb_host, port=TestVpcMongoConfig.mongodb_port,
        #     username=TestVpcMongoConfig.username, password=TestVpcMongoConfig.password)
        pass

    def get_client_ssh(self):

        # create ssh channel
        server = SSHTunnelForwarder(
            ssh_address_or_host=TestVpcMongoConfig.ssh_host,
            ssh_username=TestVpcMongoConfig.ssh_username,
            ssh_password=TestVpcMongoConfig.ssh_password,
            remote_bind_address=(TestVpcMongoConfig.mongodb_host,TestVpcMongoConfig.mongodb_port))
        server.daemon_forward_servers = True   # 打开守护进程
        server.start()
        # print(server.local_bind_port)    # ssh连接返回的动态端口
        # create MongoDB client
        mongo_client = pymongo.MongoClient(
            host="127.0.0.1", port=server.local_bind_port,
            username=TestVpcMongoConfig.username, password=TestVpcMongoConfig.password)

        return mongo_client

    @staticmethod
    def get_client():
        """
        direct connction mongoDB
        :return:
        """
        mongo_client = pymongo.MongoClient(
            host=TestVpcMongoConfig.mongodb_host, port=TestVpcMongoConfig.mongodb_port,
            username=TestVpcMongoConfig.username, password=TestVpcMongoConfig.password)
        return mongo_client

    def get_col(self, db_name, col_name):
        """
        get a collection object, and return it
        :param db_name: 数据库名称
        :param col_name: 集合名称
        :return: 集合对象
        """
        db = self.get_client()[db_name]
        col_object = db[col_name]
        return col_object


class MongoClient:

    def __init__(self, db_config=local_config):
        self.client = pymongo.MongoClient(
            host=db_config.get("mongodb_host", "default"),
            port=db_config.get("mongodb_port", 27017),
            username=db_config.get("username", "default"),
            password=db_config.get("password", "default")
        )

    def get_db(self, db_name):
        db = self.client[db_name]
        return db

    def get_collection(self, db_name, set_name):
        db = self.get_db(db_name)
        mongo_set = db[set_name]
        return mongo_set


if __name__ == '__main__':
    # mongo = MongoDemo()
    # with mongo.get_client_ssh() as client:
    #     db = client.base_price
    #     record = db.t_eva_record_2109
    #     querys = record.find_one({"Fevaluate_id": 2804978})
    #     print(querys)
    #     print(type(querys))
        # for query in querys:
        #     print(query)
        #     print(type(query))
        #     print(query['Fevaluate_id'])

    # 本地mongo库
    local_db = MongoClient()
    counters = local_db.get_collection(db_name="base_price", set_name="counters")
    # 统计集合中的记录数
    print(counters.estimated_document_count())

    answer_item = local_db.get_collection(db_name="base_price", set_name="t_answer_item")
    print(answer_item.estimated_document_count())
    results = answer_item.find({"Faname": "黑色"})
    res_list = [result for result in results]
    print(res_list[1].get("Fuser_name", "default"))
    print(type(res_list[1]))


    # 官方推荐使用insert_one()和insert_many()方法将插入单条和多条记录分开
    # collection.insert_one(dict1)
    # collection.insert_many([dict1,dict2])


    # 查询
    # 1.对于多条数据的查询，我们可以使用find()方法
    # collection.find({'Fevaluate_id': '2804978'})
    # 返回的结果是cursor类型，相当于一个生成器，我们需要遍历取到所有结果，每个结果都是dict类型

    # 2.查询单个结果，可以使用find_one()方法
    # collection.find_one({'Fevaluate_id': '2804978'})
    # 返回的结果为dict类型

    # _id属性，是MongoDB在插入的过程中自动添加的，唯一标识一条记录

    """
    符号含义示例
    $lt小于{'age': {'$lt': 20}}
    $gt大于{'age': {'$gt': 20}}
    $lte小于等于{'age': {'$lte': 20}}
    $gte大于等于{'age': {'$gte': 20}}
    $ne不等于{'age': {'$ne': 20}}
    $in在范围内{'age': {'$in': [20, 23]}}
    $nin不在范围内{'age': {'$nin': [20, 23]}}
    """

    # 正则匹配查询，例如查询名字以M开头的学生数据，示例如下：
    # results = collection.find({'name': {'$regex': '^M.*'}})
    # # 在这里使用了$regex来指定正则匹配，^M.*代表以M开头的正则表达式，这样就可以查询所有符合该正则的结果。

    """
    符号含义示例示例含义
    $regex匹配正则{'name': {'$regex': '^M.*'}}name以M开头
    $exists属性是否存在{'name': {'$exists': True}}name属性存在
    $type类型判断{'age': {'$type': 'int'}}age的类型为int
    $mod数字模操作{'age': {'$mod': [5, 0]}}年龄模5余0
    $text文本查询{'$text': {'$search': 'Mike'}}text类型的属性中包含Mike字符串
    $where高级条件查询{'$where': 'obj.fans_count == obj.follows_count'}自身粉丝数等于关注数
    """









