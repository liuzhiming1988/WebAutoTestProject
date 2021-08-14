#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : encrypt.py
@Author  : liuzhiming
@Time    : 2021/8/14 15:41
"""

import hashlib
import json
import requests


def get_crypto_Key(ServerId):
    """
    回收宝基础服务加密key集合
    :param ServerId:
    :return:
    """
    key_dict = {
        '212006': 'dk26kmdasnph0voz69fj0jpv7t3ixev8',
        '212007': '34a4bda272f7facbda86d7e789c774ee',
        '216009': '7edcd52b48e6f709539cff9c726ca96e',
        '212013': '665CA5E5BB3CBDF76ADA25240F05AE54',
        '112006': 'gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU',
        '260000': 'dk26kmdasnph0voz69fj0jpv7t3ixev8',
        '210007': '0liqvtHrIWLsqKqyDUK2jUt4AzdG4uo6',
        '110025': '5157c30f296407311b0a0b0194803340',  # bangmai_pro_eva.xml 闲鱼帮卖前端
        '217014': 'wSB8UMQ3prFJb4fb9E28UdqVL8rSaoAp'    # 订单服务自动巡检专用
    }
    return key_dict.get(ServerId)


def calc_md5(string_to_hash):
    """
    计算传入内容的md5
    :param string_to_hash:  传入内容
    :return:                传入内容的md5
    """
    return hashlib.md5(string_to_hash.encode('utf-8')).hexdigest()


def get_sign_body(body, secret_key):
    """
    回收宝自有sign规则，将所有的参数名进行排序，然后按照参数名+参数值进行拼接，最后拼接上key值，再进行sha1加密（utf-8编码），再hexdigest加密
    :param body: 传入一个字典，不包含签名
    :param secret_key: 密钥
    :return: 加入签名后的字典
    """
    sign_str = ""
    # 将传入的字典进行排序并拼接
    for i in sorted(body):
        sign_str += i + body[i]
    # 拼接上key
    sign_str += secret_key
    # 进行加密
    s = hashlib.sha1()
    s.update(sign_str.encode("utf-8"))
    body["sign"] = s.hexdigest()
    return body


def hsb_public_service_encryption(json_payload, headers):
    """
    回收宝公共服务加密
    :param json_payload:
    :param headers:
    :return:
    """
    server_id = headers['HSB-OPENAPI-CALLERSERVICEID']
    secret_key = get_crypto_Key(server_id)
    str_json = str(json.dumps(json_payload))
    src = '_'.join([str_json, secret_key])
    headers['HSB-OPENAPI-SIGNATURE'] = calc_md5(src)
    return headers


def xian_yu_rc4_encryption(json_payload):
    """
    闲鱼平台rc4加密
    :param json_payload:
    :return:
    """
    url = 'http://dev8123.huishoubao.com/getrc4'
    res = requests.post(url, data=json.dumps(json_payload))
    return res.content.decode()
