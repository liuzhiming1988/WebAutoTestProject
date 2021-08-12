#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : honor_data.py
@Author  : liuzhiming
@Time    : 2021/8/4 11:38
"""
import time
from utils.IMEI import generate_imei


def times_13():
    times_13 = str(int(time.time()*1000))
    return times_13



# imei = generate_imei()

user_id = "602810010"
phone = "18676702152"
open_id = "MDFAMjEwNzk3NDM1QDFkMjU0NDI1YjcwMTVkMmRhOWY2NjhmNDg0MzY3OTJkQGY2MDAxNjg4MTNmNDI3MzAzMjRlNzNjY2Q2OTQ2MGE5N2NhZjFiaNWIzOGZmMzg5MDMxZDYzNGI2"

# 临时变量
tmp = {}

recycle_order_id = times_13()[3:]

def buyHonorMaintainValueService():
    old_order_id = "888" + times_13()[5:]
    buyHonorMaintainValueService = {
        "_head": {
            "_interface": "buyHonorMaintainValueService",
            "_msgType": "request",
            "_remark": "",
            "_version": "0.01",
            "_timestamps": times_13(),
            "_invokeId": "2625ec9525882fca77984083bdaf59ef",
            "_callerServiceId": "110001",
            "_groupNo": "1"
        },
        "_param": {
            "createTime": times_13(),
            "maintainValueServiceList": [
                {
                    "orderType": "1",
                    "maintainValueServiceOrderId": old_order_id,
                    "productName": "荣耀 50",
                    "productSku": "2601010213601",
                    "salesPrice": "389900",
                    "maintainValueServiceName": "保值换新服务99元ming",
                    "maintainValueServiceSkuCode": "0086013201170000201",
                    "maintainValueServicePrice": "9900",
                    "maintainValueServiceCount": "1",
                    #"imei": "",
                    #"serialnum": "",
                    "maintainValueServiceEffectTime": "2021-07-31 09:22:08+0800",
                    "maintainValueServiceExpireTime": "2022-08-31 10:06:36+0800",
                    "maintainValueRatio": "70",
                    "orderRefundNo": "",
                    "orderFinishTime": "2021-08-10 14:06:38+0800",
                    "orderRefundTime": ""
                }
            ]
        }
    }
    tmp["old_order"] = old_order_id

    return buyHonorMaintainValueService

def placeOrder():
    serialnum = "msn" + times_13()[3:]
    placeOrder = {
        "_head": {
            "_interface": "placeOrder",
            "_msgType": "request",
            "_remark": "",
            "_version": "0.01",
            "_timestamps": times_13(),
            "_invokeId": "0fa04f37a588ce0df348851df2340a48",
            "_callerServiceId": "110001",
            "_groupNo": "1"
        },
        "_param": {
            "externalOrderNo": times_13(),
            "fourTupleInfo": {
                "businessAttribute": "14",
                "deliveryMode": "3",
                "paymentMode": "4",
                "businessType": "15",
                "arrivalType": "2",
                "accessBusiness": "1",
                "recycleType": "2",
                "maintainValueType": "0"
            },
            "channelInfo": {
                "pid": "3483",
                "channelId": "10000876"
            },
            "userInfo": {
                "userId": user_id,
                "userOpenId": "MDFAMjEwNzk3NDM1QDFkMjU0NDI1YjcwMTVkMmRhOWY2NjhmNDg0MzY3OTJkQGY2MDAxNjg4MTNmNDI3MzAzMjRlNzNjY2Q2OTQ2MGE5N2NhZjFiaNWIzOGZmMzg5MDMxZDYzNGI2",
                "userPhone": "18888889999"
            },
            "oldGoodsInfo": {
                "productId": "65980",
                "serialNum": serialnum,
                "imei": ""
            },
            "newGoodsInfo": {
                "productId": "65979",
                "productName": "荣耀 50 pro",
                "productPrice": "5000.00",
                "productImage": "https:\\/\\/picuat.test.hihonor.com\\/pimages\\/omstestpms\\/product\\/SSSSB2CtestGBOM01\\/\\/142_142_532F2778A3709F8D991A0BDFA8BA2279C2EAB9D1AE4EF76Cmp.JPG",
                "skuName": "65979",
                "skuId": "65979"
            },
            "logisticInfo": {
                "province": "广东",
                "city": "深圳",
                "area": "南山区",
                "address": "科苑地铁站ABCming"
            },
            "priceInfo": {
                "isMatchMaintainValue": "1",
                "maintainValueAmount": "279930",
                "maintainValueServiceFee": "0",
                "userEvaluatePrice": "1929.00",
                "newSalesPrice": "5000.00",
                "evaRecordId": "2108123961"
            },
            "customData": {
                "orderName": "钢铁侠",
                "orderPhone": phone,
                "address": "好莱坞8888号ming",
                "longitude": "113.946925",
                "latitude": "22.547326",
                "areaId": "3871"
            },
            "storeInfo":{
                "storeId":"78456",
                "store":"测试小店ming"
            }
        }
    }
    tmp["sn"] = serialnum

    return placeOrder

def submitHonorNewMachinOrder():
    trackingNo = "msf" + times_13()
    new_order_id = "99" + times_13()[5:]
    submitHonorNewMachinOrder = {
        "_head": {
            "_interface": "submitHonorNewMachinOrder",
            "_msgType": "request",
            "_remark": "",
            "_version": "0.01",
            "_timestamps": times_13(),
            "_invokeId": "7b0b9bf78622d651ef9c31fa07af3a73",
            "_callerServiceId": "110001",
            "_groupNo": "1"
        },
        "_param": {
            "basicInfo": {
                # "orderId": "75300003638",
                "orderId": new_order_id,
                "recycleOrderId": "",
                "recycleType": "1"
            },
            "oldGoodsInfo": {
                "serialNum": tmp["sn"],
                "skuCode": "2601010213601"
            },
            "newGoodsInfo": [
                {
                    "skuName": "荣耀 50 pro",
                    "qty": "1",
                    "skuCode": "008601137010000201",
                    "logisticsCompany": "顺丰快递",
                    "trackingNo": trackingNo
                }
            ],
            "priceInfo": {
                "recycleAmount": "2799.30",
                "recycleRemain": "0.00"
            },
            "userVisitInfo": {
                "province": "广东",
                "city": "深圳",
                "area": "南山区",
                "street": "粤海街道",
                "address": "深圳湾科技生态园",
                "userName": "回收宝小豹哥",
                "phone": "13612833088"
            }
        }
    }

    return submitHonorNewMachinOrder


def getHonorOrderList():
    getHonorOrderList = {
         "_head": {
              "_callerServiceId": "110001",
              "_groupNo": "1",
              "_interface": "/order_center/old4new/getHonorOrderList",
              "_invokeId": "7940480c99334bff09dae5d16b133559",
              "_msgType": "request",
              "_remark": "",
              "_timestamps": times_13(),
              "_version": "0.01"
         },
         "_param": {
              "pageIndex": "0",
              "pageSize": "10",
              "userId": user_id
         }
    }
    return getHonorOrderList

def getHonorMaintainValueService():
    getHonorMaintainValueService = {
         "_head": {
              "_callerServiceId": "110001",
              "_groupNo": "1",
              "_interface": "/order_center/old4new/getHonorMaintainValueService",
              "_invokeId": "7940480c99334bff09dae5d16b133559",
              "_msgType": "request",
              "_remark": "",
              "_timestamps": times_13(),
              "_version": "0.01"
         },
         "_param": {
              "userId": user_id,
              "honorOrderId": "75320003880"
         }
    }
    return getHonorMaintainValueService

def getHonorOrderInfo():
    getHonorOrderInfo = {
         "_head": {
              "_callerServiceId": "110001",
              "_groupNo": "1",
              "_interface": "/order_center/old4new/getHonorOrderInfo",
              "_invokeId": "7940480c99334bff09dae5d16b133559",
              "_msgType": "request",
              "_remark": "",
              "_timestamps": times_13(),
              "_version": "0.01"
         },
         "_param": {
              "orderId": "75300003638",
              "operatorlog": "0",
              "recycleOrderId": "7635440"
         }
    }
    return getHonorOrderInfo


def param_list():
    param_eg = ["接口参数示例："]
    param_eg.append(buyHonorMaintainValueService())
    param_eg.append(placeOrder())
    param_eg.append(submitHonorNewMachinOrder())
    param_eg.append(getHonorOrderList())
    param_eg.append(getHonorMaintainValueService())
    param_eg.append(getHonorOrderInfo())
    return param_eg


dict_honor = {
    "zero": "zero",
    "key_01": "/order_center/old4new/buyHonorMaintainValueService",
    "key_02": "/order_center/old4new/placeOrder",
    "key_03": "/order_center/old4new/submitHonorNewMachinOrder",
    "key_04": "/order_center/old4new/getHonorOrderList",
    "key_05": "/order_center/old4new/getHonorMaintainValueService",
    "key_06": "/order_center/old4new/getHonorOrderInfo",
    "key_07": "/order_center/old4new/submitHonorNewMachineInfo",
    "key_08": "/order_center/old4new/submitHonorNewMachinePayInfo",
}


def get_url_eg_list():
    api_list = []
    for value in dict_honor.values():
        api_list.append(value)
    return api_list


def get_eg_url(index):
    if not isinstance(index, int):
        index = int(index)
    url_eg_list = get_url_eg_list()
    return url_eg_list[index]


def get_eg_param(index):
    if not isinstance(index, int):
        index = int(index)
    param_eg = param_list()
    return param_eg[index]
