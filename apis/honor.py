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
from utils.logger import Logger

class HonorTestApi:
    """
    荣耀保值换新API
    """

    def __init__(self):
        self.KEY = "wwqCxg4e3OUzILDzdD957zuVH5iHRt4W"
        self.SERVICE_ID = "110001"
        self.OS = requests.session()
        self.DOMAIN = "http://ordserver.huishoubao.com"
        self.logger = Logger().logger


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
            # res = json.loads(res)
        except Exception as e:
            res = e
        return res

    def buyHonorMaintainValueService(self):
        """
        用户购买荣耀保值服务接口
        :return:
        """
        # body = {
        #     "createTime": "",
        #     "maintainValueServiceList": [
        #         {
        #             "maintainValueServiceOrderId":,
        #             "orderType":,
        #             "imei":,
        #             "serialnum":,
        #             "productName":,
        #             "productSku":,
        #             "salesPrice":,
        #             "maintainValueServiceName":,
        #             "maintainValueServiceSkuCode":,
        #             "maintainValueServicePrice":,
        #             "maintainValueServiceCount":,
        #             "maintainValueServiceEffectTime":,
        #             "maintainValueServiceExpireTime":,
        #             "maintainValueRatio":,
        #             "orderFinishTime":,
        #             "orderRefundTime":,
        #             "orderRefundNo":,
        #
        # }
        #     ]
        # }



    def GetHonorOrderList(self):
        url = "http://ordserver.huishoubao.com/order_center/old4new/getHonorOrderList"
        param = {
            "_head": {
                "_callerServiceId": "110001",
                "_groupNo": "1",
                "_interface": "/order_center/old4new/getHonorOrderList",
                "_invokeId": "7940480c99334bff09dae5d16b133559",
                "_msgType": "request",
                "_remark": "",
                "_timestamps": "1623830616",
                "_version": "0.01"
            },
            "_param": {
                "pageIndex": "0",
                "pageSize": "10",
                "userId": "609419571"
            }
        }
        param = json.dumps(param)
        m = hashlib.md5()
        m.update((param+self.KEY).encode("utf-8"))
        print(len(m.hexdigest()))
        headers = {"Content-Type": "application/json;charset=UTF-8",
                   "HSB-OPENAPI-SIGNATURE": m.hexdigest(),
                   "HSB-OPENAPI-CALLERSERVICEID": "110001"}
        res = requests.post(url, data=param, headers=headers)
        res.encoding = res.apparent_encoding
        print(json.dumps(res.json(),indent=4,ensure_ascii=False))


if __name__ == '__main__':
    honor = HonorTestApi()
    import time
    print(str(int(time.time()*1000)))
    # honor.GetHonorOrderList()
    # url = "http://ordserver.huishoubao.com/order_center/old4new/placeOrder"
    # honor._post(url, place_01)



