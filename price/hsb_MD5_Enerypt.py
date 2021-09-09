#!/usr/bin/env python
# -*- coding:utf-8 -*-

# @Author:MikingZhang


import hashlib,requests

# 定义md5加密函数
def Md5Enerypt(Lstr):
    '''MD5加密方法封装'''
    m = hashlib.md5()
    m.update(Lstr.encode("utf-8"))
    # print(m.hexdigest())
    return m.hexdigest()

# Md5Enerypt(Lstr='{"_head": {"_interface": "product_lib_and_option_to_evaluate", "_msgType": "request", "_remark": "","_version": "0.01", "_timestamps": "123456", "_invokeId": "123456", "_callerServiceId": "112006", "_groupNo": "1"},"_param": {"orderId": "10192534", "productId": "23007", "skuList": [], "optionList": ["23"], "isOverInsurance":"0","userId": "1311"}}_gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU')