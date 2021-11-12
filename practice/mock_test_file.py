#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : mock_test_file.py
@Author  : liuzhiming
@Time    : 2021/11/4 10:14
"""
import mock
import pytest
from practice.mock_request_file import invoke_get_info
from pytest_mock import mocker


# 1. 使用pytest-mock中的mocker
def test_get_info(mocker):
    mocker.patch("practice.mock_request_file.get_info", return_value=200)
    assert invoke_get_info("http://www.baidu.com/") == 200


# 2. 使用mock中patch方法，对目标函数的返回值进行替换，采用了with上下文进行管理
def test_get_info_2():
    with mock.patch("practice.mock_request_file.get_info", side_effetc=[400, 500]) as mock_test:
        assert invoke_get_info("http://www.huishoubao.com.cn") == mock_test.return_value


# 3. 使用的装饰器的方式对mock对象的函数返回值进行替换
@mock.patch("practice.mock_request_file.get_info", return_value=500)
def test_get_info_3(get_info):
    assert invoke_get_info("http://www.jd.com/") == get_info.return_value


if __name__ == '__main__':
    pytest.main()



