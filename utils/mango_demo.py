#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : mango_demo.py
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


class MongoDemo:

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


if __name__ == '__main__':
    mongo = MongoDemo()
    with mongo.get_client_ssh() as client:
        db = client.base_price
        record = db.t_eva_record_2109
        querys = record.find({"Fevaluate_id": 2804978})
        # print(querys)
        for query in querys:
            print(query)
            print(type(query))
            # print(query['Fevaluate_id'])








