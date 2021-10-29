#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : ssh_client.py
@Author  : liuzhiming
@Time    : 2021/10/9 17:18
"""

import paramiko


class SSHConfig:
    HOST = "10.0.11.14"
    PORT = 22
    USERNAME = "ming"
    PASSWORD = "123456"


class LinuxClient(object):

    def __init__(self, host=SSHConfig.HOST, port=SSHConfig.PORT, username=SSHConfig.USERNAME, password=SSHConfig.PASSWORD):

        # 创建一个ssh的客户端
        self.ssh = paramiko.SSHClient()
        # 创建一个ssh的白名单
        white_host = paramiko.AutoAddPolicy()
        # 加载创建的白名单
        self.ssh.set_missing_host_key_policy(white_host)
        # 连接服务器
        self.ssh.connect(
            hostname=host,
            port=port,
            username=username,
            password=password
        )
        self.shell = self.ssh.invoke_shell()
        self.shell.settimeout(1)

    def exec_command(self, command):
        """发送单条命令"""
        stdin, stdout, stderr = self.ssh.exec_command(command)
        print(stdout.read().decode())
        self.ssh.close()   # 关闭连接


if __name__ == '__main__':
    # ssh_c = LinuxClient()
    # ssh_c.exec_command("ls")
    # ssh_c.exec_command("cat /home/ming/data/locust_test/test.log")
    # ssh_c.exec_command("ls")
    jump_server = LinuxClient(host="jumpserver.huishoubao.com", port=2222, username="liuzhiming@huishoubao.com.cn", password="123123")
    # jump_server.exec_command("p")
