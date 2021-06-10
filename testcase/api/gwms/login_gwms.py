#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : login_gwms.py
@Author  : liuzhiming
@Time    : 2021/6/9 18:49
"""

import requests
import json
import re
from urllib import parse


class LoginGwms:

    def __init__(self):
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}

    def login(self):
        url = "http://119.23.17.189:8090/gwms_test/main.jsf"
        res = requests.get(url).text
        # print(res)
        machine_id = res.split(':"0","machineID":"')[1].split('","startDate"')[0]
        view_state = res.split('id="javax.faces.ViewState" value="')[1].split('" autocomplete="off"')[0]

        # print(machine_id)
        # print(view_state)

        url_login = "http://119.23.17.189:8090/gwms_test/main.jsf"
        form_data = {
            "form1": "form1",
            "form1: nv_userid": "030",
            "form1: passWord": "030",
            "form1: selectid": "1",
            "form1: available_flag": "",
            "form1: msg": "系统授权通过,有效期更新至:2099-09-26,效期还剩余:28607天",
            "form1: resultMsg":"",
            "form1: machineID":machine_id,
            "javax.faces.ViewState": view_state,
            "form1: loginBtn.x": "85",
            "form1: loginBtn.y": "15"
        }
        data = parse.urlencode(form_data)
        # print(form_data)
        res_login = requests.post(url_login, data=data, headers=self.headers).text
        print(res_login)




if __name__ == '__main__':
    LoginGwms().login()