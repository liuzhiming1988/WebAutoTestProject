#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : public_service_post.py
@Author  : liuzhiming
@Time    : 2021/9/13 16:51
"""
import hashlib
import json
import requests
import time

def calc_md5(string_to_hash):
    """
    计算传入内容的md5
    :param string_to_hash:  传入内容
    :return:                传入内容的md5
    """
    return hashlib.md5(string_to_hash.encode('utf-8')).hexdigest()


def get_crypto_Key(ServerId):
    """
    回收宝基础服务加密key集合
    :param ServerId:
    :return:
    """
    key_dict = {
        '212006': 'dk26kmdasnph0voz69fj0jpv7t3ixev8',  # 价格-prdserver.huishoubao.com
        '212007': '34a4bda272f7facbda86d7e789c774ee',
        '216009': '7edcd52b48e6f709539cff9c726ca96e',
        '212013': '665CA5E5BB3CBDF76ADA25240F05AE54',
        '112006': 'gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU',  # 价格-codserver.huishoubao.com
        '260000': 'dk26kmdasnph0voz69fj0jpv7t3ixev8',
        '210007': '0liqvtHrIWLsqKqyDUK2jUt4AzdG4uo6',
        '212093': 'f01c4962f2ed26b1a72f9029110563ea',  # 价格-闲鱼帮买基础服务-bmserver.huishoubao.com
        '217014': 'wSB8UMQ3prFJb4fb9E28UdqVL8rSaoAp',  # 公共-订单服务自动巡检专用
        '116005': '090a2a8379414357eb6c808717249992',  # 公共-渠道商户
        '214001': '76716d9dfe864872f6ad1f5c6efc5447',  # 公共-新商户 new-merchant-api.hsb.com
        '218003': '72d158c2c50788cc77c77ace3acc2b2d',  # CSL-价格
        '218009': 'eyt70zXUT0RN8T5JmvdCeQmWg2w8gSbo',  # CSL-价格
        '118002': 'fJmORuihWr4nrroHwms5togmkYqNP9pW',  # CSL-价格
        '115001': '0dd892967501866a74b48a6dc7536c87',  # CSL-价格
        '110025': 'ef99b0142994acf5ef63bada662de822',  # 价格-回收宝专业版接入层
        '216008': 'f5dca47cdabddec161b3150107b96a87',  # basepriceserver.huishoubao.com
        '116006': 'R2gFCRbILiNhwv3YbtaGceYJlPS5Ku02',   # bpeserver.huishoubao.com
        '110001': 'wwqCxg4e3OUzILDzdD957zuVH5iHRt4W'     # 荣耀保值换新服务
    }
    return key_dict.get(ServerId)


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


