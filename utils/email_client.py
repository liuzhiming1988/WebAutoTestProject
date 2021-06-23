#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : email_client.py
@Author  : liuzhiming
@Time    : 2021/6/19 下午10:10
"""
import yagmail
from utils.config_read import ConfigRead

# 从配置文件中读取邮件配置信息
conf = ConfigRead()
user = conf.get_value("email", "user")
password = conf.get_value("email", "password")
host = conf.get_value("email", "host")
title = conf.get_value("email", "subject")
content = conf.get_value("email", "content")
address_list = conf.get_value("email", "to").split(";")


def send_mail(attachment=None, text=content, subject=title):
    """

    :param attachment: 附件路径，传列表
    :param text: 邮件正文部分，可以传html
    :param subject: 邮件标题，默认值可在配置文件中修改
    :return:
    """
    email_client = yagmail.SMTP(
        user=user,
        password=password,
        host=host)
    email_client.send(
        address_list,
        subject,
        content,
        attachment)
    email_client.close()


if __name__ == '__main__':

    send_mail(attachment=["/Users/liuzhiming/Documents/test_ocr.png"], text="测试：Test on macOS", subject="测试：From macOS email_client")

