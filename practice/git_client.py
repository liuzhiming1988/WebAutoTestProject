#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : git_client.py
@Author  : liuzhiming
@Time    : 2021/11/12 17:42
"""

import git
from git import Repo

"""
cd path
git add .
git commit -m "remarks"
git push origin master
"""


class GitClient:

    def __init__(self, git_path):
        """

        :param git_path: git项目所在路径
        """
        self.git_path = git_path
        self.repo = Repo(self.git_path)
        self.git = self.repo.git

    def get_current_branch(self):
        current_branch = self.repo.active_branch
        print(current_branch)
        return current_branch

    def get_all_branches(self):
        print([str(b) for b in self.repo.branches])
        return self.repo.branches

    def add_file(self, files=None):
        # if files is None:
        #     self.git.add(".")
        # else:
        #     self.repo.index.add(files)
        self.repo.index.add(files)

    def commit(self, mark):
        self.repo.index.commit(mark)

    def create_tag_push(self, tag_name, remark):
        """创建tag"""
        # 原生命令
        # self.git.tag(tag_name, remark)
        # self.git.push("origin", tag_name)
        # repo方式
        self.repo.create_tag(tag_name, message=remark)
        self.repo.remotes.origin.push(tag_name)

    def push(self, tag_name):
        # self.repo.remote().push()
        self.repo.remotes.origin.push(tag_name)


    def get_status(self):
        """查看status，打印出改动的信息"""
        print(self.git.status())

    def check_is_empty(self):
        """查看版本库是否为空版本库"""
        print(self.repo.bare)
        return self.repo.bare


if __name__ == '__main__':
    git_client = GitClient(git_path="D:\work\WebAutoTestProject")
    # git_client.get_current_branch()
    # git_client.get_all_branches()
    # git_client.get_status()
    # git_client.check_is_empty()
    # git_client.add_file([".\\practice\\git_client.py"])
    # git_client.commit("test gitpython add")
    # git_client.create_tag_push("tag-test-2021111501", "mark words")
    git_client.push("tag-test-2021111501")
