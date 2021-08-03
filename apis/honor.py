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

buy_01 = {
     "_head": {
          "_callerServiceId": "110001",
          "_groupNo": "1",
          "_interface": "/order_center/old4new/buyHonorMaintainValueService",
          "_invokeId": "7940480c99334bff09dae5d16b133559",
          "_msgType": "request",
          "_remark": "",
          "_timestamps": "1623830612",
          "_version": "0.01"
     },
     "_param": {
          "createTime": "1111111111120",
          "maintainValueServiceList": [
               {
                    "maintainValueServiceOrderId": "honor00013",
                    "orderType": "2",
                    "serialnum": "123",
                    "productName": "honor p50",
                    "productSku": "honor p50 pro",
                    "salesPrice": "560000",
                    "maintainValueServiceName": "p50 old4new",
                    "maintainValueServicePrice": "9900",
                    "maintainValueServiceCount": "2",
                    "maintainValueServiceEffectTime": "2021-07-29 12:00:15+0800",
                    "maintainValueServiceExpireTime": "2022-07-29 12:00:15",
                    "maintainValueRatio": "70",
                    "maintainValueServiceSkuCode": "p60 sku",
                    "orderFinishTime": "2021-07-29 12:01:19",
                    "orderRefundTime": "2021-07-29 12:02:19",
                    "orderRefundNo": "honor10001"
               },
               {
                    "maintainValueServiceOrderId": "honor00014",
                    "orderType": "1",
                    "serialnum": "123",
                    "productName": "honor p50",
                    "productSku": "honor p50 pro",
                    "salesPrice": "560000",
                    "maintainValueServiceName": "p50 old4new",
                    "maintainValueServicePrice": "9900",
                    "maintainValueServiceCount": "2",
                    "maintainValueServiceEffectTime": "2021-07-29 12:20:15",
                    "maintainValueServiceExpireTime": "2022-07-29 12:30:15",
                    "maintainValueRatio": "70",
                    "maintainValueServiceSkuCode": "p60 sku",
                    "orderFinishTime": "2021-07-29 12:01:19",
                    "orderRefundTime": "2021-07-29 12:02:19",
                    "orderRefundNo": "honor10002"
               }
          ]
     }
}

place_01 = {
     "_head": {
          "_callerServiceId": "110001",
          "_groupNo": "1",
          "_interface": "/order_center/old4new/placeOrder",
          "_invokeId": "7940480c99334bff09dae5d16b133559",
          "_msgType": "request",
          "_remark": "",
          "_timestamps": "1623830622",
          "_version": "0.01"
     },
     "_param": {
          "externalOrderNo": "2108030032",
          "channelInfo": {
               "pid": "1001",
               "channelId": "40000001"
          },
          "fourTupleInfo": {
               "businessAttribute": "14",
               "deliveryMode": "3",
               "paymentMode": "4",
               "businessType": "15",
               "arrivalType": "2",
               "accessBusiness": "1",
               "recycleType": "2",
               "maintainValueType": "0",
               "orderCode": "honor00016"
          },
          "oldGoodsInfo": {
               "productId": "64537",
               "serialNum": "SD159647852369",
               "imei": "3333333333"
          },
          "newGoodsInfo": {
               "productId": "64537",
               "productName": "新机001",
               "productPrice": "666600",
               "productImage": "123.jpg"
          },
          "userInfo": {
               "userId": "609419571",
               "userName": "ZS",
               "userPhone": "13588888888",
               "userOpenId": "ljkjvoisdfjlsj"
          },
          "priceInfo": {
               "isMatchMaintainValue": "1",
               "maintainValueAmount": "100000",
               "maintainValueServiceFee": "19900",
               "userEvaluatePrice": "500000",
               "newSalesPrice": "650000",
               "evaRecordId": "210722088"
          },
          "logisticInfo": {
               "provice": "广东省",
               "city": "深圳市",
               "area": "南山区",
               "address": "威新软件园"
          }
     }
}

submitHonorNewMachinOrder_01 = {
     "_head": {
          "_interface": "submitHonorNewMachinOrder",
          "_msgType": "request",
          "_remark": "",
          "_version": "0.01",
          "_timestamps": "1627902755",
          "_invokeId": "beb1496652ef7e39d3c9ee0af3ed4d63",
          "_callerServiceId": "110001",
          "_groupNo": "1"
     },
     "_param": {
          "basicInfo": {
               "orderId": "honor00001",
               "recycleOrderId": "7635031",
               "recycleType": "1"
          },
          "oldGoodsInfo": {
               "serialNum": "13000005800-1",
               "skuCode": "0086011001290100201",
               "skuName": ""
          },
          "newGoodsInfo": [
               {
                    "qty": "1",
                    "skuCode": "0086011001290100201",
                    "skuName": "荣耀50 1亿像素超清影像 （初雪水晶）"
               },
               {
                    "qty": "1",
                    "skuCode": "00860116090000301",
                    "skuName": "荣耀商城保值换新服务"
               },
               {
                    "qty": "1",
                    "skuCode": "00860116090000302",
                    "skuName": "延保商品"
               },
               {
                    "qty": "1",
                    "skuCode": "301006C",
                    "skuName": "phone"
               },
               {
                    "qty": "1",
                    "skuCode": "1001010007701001",
                    "skuName": "赠品1"
               }
          ],
          "logisticsInfo": {
               "logisticsCompany": "顺丰快递",
               "trackingNo": "SVP1300000580001"
          },
          "priceInfo": {
               "recycleAmount": "600",
               "recycleRemain": "0.00"
          },
          "userVisitInfo": {
               "province": "江苏",
               "city": "南京",
               "area": "雨花台区",
               "street": "street",
               "address": "软件大道101号润和",
               "userName": "叶女士2",
               "phone": "17715298882"
          }
     }
}

getHonorOrderList_01 = {
     "_head": {
          "_callerServiceId": "110001",
          "_groupNo": "1",
          "_interface": "/order_center/old4new/getHonorOrderList",
          "_invokeId": "7940480c99334bff09dae5d16b133559",
          "_msgType": "request",
          "_remark": "",
          "_timestamps": "1623830612",
          "_version": "0.01"
     },
     "_param": {
          "pageIndex": "0",
          "pageSize": "10",
          "userId": "609419571"
     }
}

getHonorMaintainValueService_01 = {
     "_head": {
          "_callerServiceId": "110001",
          "_groupNo": "1",
          "_interface": "/order_center/old4new/getHonorMaintainValueService",
          "_invokeId": "7940480c99334bff09dae5d16b133559",
          "_msgType": "request",
          "_remark": "",
          "_timestamps": "1623830612",
          "_version": "0.01"
     },
     "_param": {
          "userId": "609419571",
          "honorOrderId": "honor00010"
     }
}

getHonorOrderInfo_01 = {
     "_head": {
          "_callerServiceId": "110001",
          "_groupNo": "1",
          "_interface": "/order_center/old4new/getHonorOrderInfo",
          "_invokeId": "7940480c99334bff09dae5d16b133559",
          "_msgType": "request",
          "_remark": "",
          "_timestamps": "1623830612",
          "_version": "0.01"
     },
     "_param": {
          "recycleOrderId": "7635031"
     }
}



class HonorTestApi:

    def __init__(self):
        self.KEY = "wwqCxg4e3OUzILDzdD957zuVH5iHRt4W"
        self.SERVICE_ID = "110001"
        self.OS = requests.session()

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
        try:
            res = self.OS.post(url, data=data, headers=headers)
            res.encoding = res.apparent_encoding
            res = json.dumps(res.json(), indent=4, ensure_ascii=False)
            print(res)
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
    # honor.GetHonorOrderList()
    url = "http://ordserver.huishoubao.com/order_center/old4new/placeOrder"
    honor._post(url, place_01)



