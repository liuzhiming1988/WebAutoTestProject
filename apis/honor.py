#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : honor.py
@Author  : liuzhiming
@Time    : 2021/8/3 11:36
"""
import requests
import json
import hashlib
from utils.logger import Logger, LoggerV2


class HonorTestApi:
    """
    荣耀保值换新API
    """

    def __init__(self):
        self.KEY = "wwqCxg4e3OUzILDzdD957zuVH5iHRt4W"
        self.SERVICE_ID = "110001"
        self.OS = requests.session()
        self.DOMAIN = "http://ordserver.huishoubao.com"
        self.logger = LoggerV2()

    @staticmethod
    def get_md5(str):
        """
        接收一个字符串，返回md5值
        :param str:
        :return:
        """
        sign = hashlib.md5()
        sign.update(str.encode("UTF-8"))
        return sign.hexdigest()

    def get_headers(self, param):
        data = json.dumps(param)
        data = data + "_" + self.KEY
        headers = {"Content-Type": "application/json;charset=UTF-8",
                   "HSB-OPENAPI-SIGNATURE": self.get_md5(data),
                   "HSB-OPENAPI-CALLERSERVICEID": self.SERVICE_ID}
        return headers

    def _post(self, url, param):
        headers = self.get_headers(param)
        data = json.dumps(param)
        if "http://" in url:
            pass
        else:
            url = self.DOMAIN + url
        try:
            self.logger.debug("【Start Send Request url】:\n{}".format(url))
            self.logger.debug("【Request Headers】：\n{}".format(headers))
            self.logger.debug("【Request Body】:\n{}".format(json.dumps(param,indent=5,ensure_ascii=False)))
            res = self.OS.post(url, data=data, headers=headers)
            res.encoding = res.apparent_encoding
            res = json.dumps(res.json(), indent=4, ensure_ascii=False)
            self.logger.debug("【{}】Response Body:\n{}".format(url, res))
            self.logger.debug("【End The Request】：{}".format(url))
            # res = json.loads(res)   # 开启此行代码后，前端不能格式化显示json
        except Exception as e:
            res = e
        return res


if __name__ == '__main__':
    honor = HonorTestApi()
    import time
    print(str(int(time.time()*1000)))
    # honor.GetHonorOrderList()
    # url = "http://ordserver.huishoubao.com/order_center/old4new/placeOrder"
    # honor._post(url, place_01)



