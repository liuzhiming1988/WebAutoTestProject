#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : github_file.py
@Author  : liuzhiming
@Time    : 2021/11/5 12:35
"""

import requests
import json
import re
# 用于忽略警告
# import urllib3
# urllib3.disable_warnings()


def get_top_project(name="python", num="20"):
    """获取github上排名靠前的python项目"""
    url = "https://api.github.com/search/repositories?q=language:{}&sort".format(name)
    res = json.loads(requests.get(url).text)
    for item in res["items"][:int(num)]:
        print(item["html_url"])
        # print(json.dumps(item, indent=4))


class GitHubClient:

    def __init__(self):
        # 设置session
        self.s = requests.session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:44.0) Gecko/20100101 Firefox/44.0"
        }
        # self.s.verify = False

    def get_token(self):
        """
        获取页面token
        :return:
        """
        login_url = "https://github.com/login"
        r = self.s.get(login_url, headers=self.headers)
        authenticity_token = re.findall('<input type="hidden" name="authenticity_token" value="(.+?)" />', r.text)
        print("authenticity_token：{}".format(authenticity_token))
        return authenticity_token[0]

    def github_login(self, username, password):
        """
        登录方法，返回登录后的title
        :param username:
        :param password:
        :return:
        """
        session_url = "https://github.com/session"
        body = {
            "authenticity_token": self.get_token(),
            "commit": "Sign in",
            "login": username,
            "password": password,
            "utf8": "✓",
            "webauthn-support": "unknown"
        }
        r = self.s.post(session_url, headers=self.headers, data=body)
        title = re.findall('<title>(.+?)</title>', r.text)
        print("title：%s" % title[0])
        return title[0]

    def is_login_success(self, title):
        """
        判断title，登录成功返回True，失败返回False
        :param title:
        :return:
        """
        if "GitHub" == title:
            return True
        else:
            return False


if __name__ == '__main__':
    # get_top_project()
    github = GitHubClient()
    github.github_login(username="554050110@qq.com", password="m554010")
