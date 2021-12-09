#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : mysql_client.py
@Author  : liuzhiming
@Time    : 2021/10/29 15:37
"""

import pymysql


class MysqlClient:

    def __init__(self, host, port, username, password, database):
        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database,
            charset="utf8")

    def __del__(self):
        self.conn.close()
        print("关闭conn连接")

    def insert(self, sql):
        text = ""
        if "insert" not in sql.lower()[:10]:
            print("只允许传入Insert语句，请检查：\n{}".format(sql))
            return False

        conn = self.conn
        with conn.cursor() as cursor:
            try:
                conn.cursor().execute(sql)
                conn.commit()
                text = "处理成功"
            except pymysql.err.IntegrityError as ec:
                text = "插入失败，返回错误如下：\n{}".format(ec.__str__())  # 打印异常信息
            print(text)
            return text

    def select(self, sql):
        if "select" in sql.lower()[:10]:
            pass
        else:
            print("只允许传入查询语句，请检查：\n{}".format(sql))
            return False

        with self.conn.cursor() as cursor:
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
                print("查询结果如下：\n{}".format(result))
                return result
            except Exception as ec:
                print("查询失败，返回错误如下：\n{}".format(ec.__str__()))  # 打印异常信息
                return False


if __name__ == '__main__':
    vpc_price_mysql_client = MysqlClient(
        host="193.112.170.216",
        port=3306,
        username="eva",
        password="evao123456",
        database="recycle"
    )

    insert_sql = "INSERT INTO `recycle`.`t_eva_pditems_history`(`Fplatform_type`, `Fproduct_id`, `Fstandard_price`, `Fmax_price`, `Fmin_price`, `Falgorithm_id`, `Fevaluate_item`, `Fdelete_flag`, `Fproduct_item`, `Fshow_item`, `Foperator_name`, `Fsku_map`, `Fitem_group`, `Fitem_add_sub`, `Falgorithm_order`, `Fall_combination_price`, `Fcreate_time`, `Fupdate_time`,`Fversion`)  (select Fplatform_type, Fproduct_id, Fstandard_price, Fmax_price, Fmin_price, Falgorithm_id, Fevaluate_item, Fdelete_flag, Fproduct_item, Fshow_item, Foperator_name, Fsku_map, Fitem_group, Fitem_add_sub, Falgorithm_order, Fall_combination_price, Now(), Now(), 931 from t_eva_pditems_history  where Fplatform_type = 1 and Fproduct_id = 30749 ORDER BY Fupdate_time DESC LIMIT 1)"
    vpc_price_mysql_client.insert(insert_sql)
    vpc_price_mysql_client.insert(insert_sql)

    # select_sql = "select * from t_eva_pditems_history  where Fplatform_type = 1 and Fproduct_id = 30749 ORDER BY Fupdate_time DESC LIMIT 5"
    # vpc_price_mysql_client.select(select_sql)
    # vpc_price_mysql_client.select(select_sql)
