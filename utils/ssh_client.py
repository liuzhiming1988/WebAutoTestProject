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

    def __del__(self):
        self.ssh.close()  # 关闭连接
        print("关闭ssh连接")

    def exec_command(self, command):
        """发送单条命令"""
        stdin, stdout, stderr = self.ssh.exec_command(command)
        print(stdout.read().decode())

    def interactive_shell(self):
        command = input(">>>"+"\n")
        self.shell.send(command)
        while True:
            try:
                recv = self.shell.recv(512).decode()
                if recv:
                    print(recv)
            except:
                command = input(">>>") + "\n"
                self.shell.send(command)


class LinuxFtpClient:

    def __init__(self, host=SSHConfig.HOST, port=SSHConfig.PORT, username=SSHConfig.USERNAME, password=SSHConfig.PASSWORD):
        trans = paramiko.Transport(sock=(host, port))
        trans.connect(username=username, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(trans)

    def __del__(self):
        self.sftp.close()
        print("关闭sftp连接")

    def put(self, local_file, origin_file):
        """
        把本地文件上传到远端路径，如：sftp.put("local.log", "/data/test/ll.log")
        :param local_file:
        :param origin_file:
        :return:
        """
        try:
            self.sftp.put(local_file, origin_file)
        except FileNotFoundError as ec:
            error_str = "文件上传失败：【{}】".format(ec.__str__())
            print(error_str)

    def get(self, origin_file, local_file):
        """
        把远程服务器上的文件拉取到本地
        :param origin_file:
        :param local_file:
        :return:
        """
        try:
            self.sftp.get(origin_file, local_file)
        except FileNotFoundError as ec:
            error_str = "文件拉取失败：【{}】".format(ec.__str__())
            print(error_str)


if __name__ == '__main__':
    ssh_c = LinuxClient()
    # ssh_c.exec_command("ls")
    ssh_c.exec_command("cat /home/ming/data/locust_test/test.log")
    # ssh_c.exec_command("ls")
    # jump_server = LinuxClient(host="jumpserver.huishoubao.com", port=2222, username="liuzhiming@huishoubao.com.cn", password="123123")
    # jump_server.exec_command("p")
    # ssh_c.interactive_shell()
    ftp = LinuxFtpClient()
    ftp.put("redis_client.py", "data/locust_test/test.py")
    ftp.get("data/locust_test/test.py", "d:/testabc.py")

