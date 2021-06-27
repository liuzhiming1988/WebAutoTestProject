#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : pmysql.py
@Author  : liuzhiming
@Time    : 2021/5/26 11:03
"""
# 导入pymysql模块
import pymysql
from config.config_read import ConfigRead


cr = ConfigRead()
host = cr.get_value("mysql", "host")
port = int(cr.get_value("mysql", "port"))
username = cr.get_value("mysql", "username")
passwd = cr.get_value("mysql", "passwd")
database = cr.get_value("mysql", "database")


class Pmysql:

    def __init__(self):
        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password=passwd,
            database=database,
            charset="utf8")
        self.cursor = self.conn.cursor()

    def execute_sql(self, sql, limit=10):
        """

        :param sql: 传入要执行的sql语句,sql后不带入分号
        :param limit: 默认限制最多返回10条记录
        :return:
        """
        result=None
        if ";" in sql:
            sql = sql[:-1]
        else:
            pass

        if "select" in sql.lower():
            if "limit" in sql.lower():
                pass
            else:
                sql += " limit {0}".format(limit)
            self.cursor.execute(sql)

            num = self.cursor.rownumber
            count = self.cursor.rowcount
            result = self.cursor.fetchall()
            # if count > 1:
            #     result = self.cursor.fetchall()
            # else:
            #     result = self.cursor.fetchone()

        else:
            self.cursor.execute(sql)
            self.conn.commit()
            result = "{0} is success".format(sql)
        self.cursor.close()
        self.conn.close()
        return result

    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    msq = Pmysql()
    sql = "SELECT u.Fuser_id FROM t_user u WHERE u.Fphone_num = '13049368516';"

    res = msq.execute_sql(sql, limit=1)
    print(res[0][0])



