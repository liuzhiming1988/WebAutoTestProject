#!/usr/bin/env python
# -*- coding:utf-8 -*-

# @Author:MikingZhang


import hashlib
import requests
import json


# 定义md5加密函数
def Md5Enerypt(Lstr):
    '''MD5加密方法封装'''
    m = hashlib.md5()
    m.update(Lstr.encode("utf-8"))
    # print(m.hexdigest())
    return m.hexdigest()


# 定义md5加密函数
def md5_encrypt(str_):
    """MD5加密方法封装"""
    m = hashlib.md5()
    m.update(str_.encode("utf-8"))
    return m.hexdigest()


def get_secret_key(key_):
    """
    根据callerserviced，返回对应的密钥
    :param key_:
    :return:
    """
    key_dict = {
        "112002": "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9",   # EvaluateProductV3
        "216053": "1FN3xvtbO9NG80QmRf3E6HReN0PHQCLF",    # EvaluatePriceV3
        "216002": "rAfnRwyWfh2N9vXVgWwdpJxaXgOCd8af",    # EvaluateDetectV3  EvaluateCheckV3
        "212011": "UhQ4jfyKxrGb1QBhFAzaspRPBwB1x4eJ",   # BaseProductV3
        "212019": "af6c253503a530d9d3fd021c15bd14c3",   # EvaluateCheckV3
        "216041": "4sf0W2F6ix1SXaqVQ34j2tnvwSI9oa4R",   # BasePriceEvaluate
        "110001": "c36691ced620bf82ad3fc4642f8a6427",
        "116006": "R2gFCRbILiNhwv3YbtaGceYJlPS5Ku02",
        "112006": "gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU",
        "110025": "5157c30f296407311b0a0b0194803340",
        "212013": "CtN4bZr7qYyxygRyP5T0VWMEvWhpH0uf",
        "816006": "9aee61caf448b65fdf84c0e7d77c7348",   # EvaluatePrice
        # "816006": "R2gFCRbILiNhwv3YbtaGceYJlPS5Ku02",   # EvaluateProduct
        "216009": "5WiSSySG2uadSrvcLIFtrzlwenN7M1cb"        # 用于查询订单信息
    }
    return key_dict[key_]


def get_price_headers(param):
    """
    接收接口参数，加密后返回headers
    :param param: 接口参数
    :return:
    """
    CALLERSERVICEID = param["_head"]["_callerServiceId"]
    if not CALLERSERVICEID:
        return "_callerServiceId不能为空，请检查！"
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "HSB-OPENAPI-SIGNATURE": md5_encrypt(json.dumps(param)+"_"+get_secret_key(CALLERSERVICEID)),
        "HSB-OPENAPI-CALLERSERVICEID": CALLERSERVICEID
    }
    return headers


def res_print(res, print_type="1"):
    """
    格式化打印输出响应结果
    :param res: 响应结果，原数据
    :param print_type: 1为text，其它为json
    :return:
    """
    res.encoding = res.apparent_encoding   # 编码设置
    if print_type == "1":
        print("==========>接口响应数据为：\n{}".format(res.text))
    else:
        print("==========>接口响应『json』格式数据为：\n{}".format(json.dumps(res.json(), indent=4, ensure_ascii=False)))

    print("\n==========>接口响应时长：{} 秒\n".format(res.elapsed.total_seconds()))
    print('\033[32m=\033[0m' * 180)









