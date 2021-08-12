#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : conftest.py
@Author  : liuzhiming
@Time    : 2021/6/1 17:43
"""

import pytest
from utils.common import *
import requests
import time
from utils.common import *
import random
from urllib3 import encode_multipart_formdata
from utils.pmysql import Pmysql
import pytest
import time
import json
from apis.hsb_app_api import HsbAppApi

phone = "18676702152"
sms_code = "666666"

own = HsbAppApi()
own.login(phone, sms_code)
res = own.temp


@pytest.fixture(scope="module", autouse=True)
def get_token():
    loginToken = res["token"]
    return loginToken


@pytest.fixture(scope="module", autouse=True)
def get_uid():
    uid = res["eid"]
    return uid







