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

maintainValueServiceOrderId = "ming"+times_13()[:10]
serialnum = "num"+times_13()[:10]
imei = generate_imei()
externalOrderNo = "MT"+times_13()
orderCode = "honor"+times_13()
trackingNo = "SF"+times_13()
user_id = "602809907"
phone = "18676702152"
open_id = "fhjkdaler"

new_sku_code = "0086011001290100201"
new_product_id = "64537"
new_product_name = "荣耀50 Pro"
old_sku_code = "0086011001290100201"
old_product_id = "64537"
old_product_name = "荣耀40"

recycle_order_id = times_13()[3:]


buyHonorMaintainValueService = {
    "_head": {
        "_callerServiceId": "110001",
        "_groupNo": "1",
        "_interface": "/order_center/old4new/buyHonorMaintainValueService",
        "_invokeId": "7940480c99334bff09dae5d16b133559",
        "_msgType": "request",
        "_remark": "",
        "_timestamps": times_13(),
        "_version": "0.01"
    },
    "_param": {
        "createTime": times_13(),
        "maintainValueServiceList": [
            {
                "maintainValueServiceOrderId": maintainValueServiceOrderId,
                "orderType": "1",
                "imei": imei,
                "serialnum": serialnum,
                "productName": "honor p50",
                "productSku": "honor p50 pro",
                "salesPrice": "560000",
                "maintainValueServiceName": "Honor50 old4new",
                "maintainValueServiceSkuCode": "oldsku12345678",
                "maintainValueServicePrice": "9900",
                "maintainValueServiceCount": "2",
                "maintainValueServiceEffectTime": "2021-08-01 12:00:15+0800",
                "maintainValueServiceExpireTime": "2022-08-01 00:00:00+0800",
                "maintainValueRatio": "70",
                "orderFinishTime": "",
                "orderRefundTime": "",
                "orderRefundNo": ""
            }
        ]
    }
}

placeOrder = {
     "_head": {
          "_callerServiceId": "110001",
          "_groupNo": "1",
          "_interface": "/order_center/old4new/placeOrder",
          "_invokeId": "7940480c99334bff09dae5d16b133559",
          "_msgType": "request",
          "_remark": "",
          "_timestamps": times_13(),
          "_version": "0.01"
     },
     "_param": {
          "externalOrderNo": externalOrderNo,
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
               "maintainValueType": "0"
          },
          "oldGoodsInfo": {
               "productId": old_product_id,
               "serialNum": serialnum,
               "imei": imei
          },
          "newGoodsInfo": {
               "productId": new_product_id,
               "productName": new_product_name,
               "productPrice": "666600",
               "productImage": "123.jpg",
              "skuName": "65980",
              "skuId": "65980"
          },
          "userInfo": {
               "userId": user_id,
               # "userName": "liuzhiming",
               "userPhone": phone,
               "userOpenId": open_id
          },
          "priceInfo": {
               "isMatchMaintainValue": "1",
               "maintainValueAmount": "100000",
               "maintainValueServiceFee": "19900",
               "userEvaluatePrice": "500000",
               # "newSalesPrice": "650000",
               "evaRecordId": "210722088"
          }
     }
}

submitHonorNewMachinOrder = {
    "_head": {
        "_interface": "submitHonorNewMachinOrder",
        "_msgType": "request",
        "_remark": "",
        "_version": "0.01",
        "_timestamps": times_13(),
        "_invokeId": "beb1496652ef7e39d3c9ee0af3ed4d63",
        "_callerServiceId": "110001",
        "_groupNo": "1"
    },
    "_param": {
        "basicInfo": {
            #"orderId": orderCode,
            "recycleOrderId": recycle_order_id,
            "recycleType": "1"
        },
        "oldGoodsInfo": {
            "serialNum": serialnum,
            "skuCode": old_sku_code,
            # "skuName": "内存"
        },
        "newGoodsInfo": [
            {
                "qty": "1",
                "skuCode": "0086011001290100201",
                "skuName": "荣耀50 1亿像素超清影像 （初雪水晶）",
                "logisticsCompany": "顺丰快递",
                "trackingNo": trackingNo
            },
            {
                "qty": "1",
                "skuCode": "00860116090000301",
                "skuName": "荣耀商城保值换新服务",
                "logisticsCompany": "韵达",
                "trackingNo": trackingNo
            },
            {
                "qty": "1",
                "skuCode": "00860116090000302",
                "skuName": "延保商品",
                "logisticsCompany": "京东",
                "trackingNo": trackingNo
            },
            {
                "qty": "1",
                "skuCode": "301006C",
                "skuName": "phone",
                "logisticsCompany": "圆通",
                "trackingNo": trackingNo
            },
            {
                "qty": "1",
                "skuCode": "1001010007701001",
                "skuName": "赠品1",
                "logisticsCompany": "顺丰快递",
                "trackingNo": trackingNo
            }
        ],
        "priceInfo": {
            "recycleAmount": "600",
            "recycleRemain": "0.00"
        },
        "userVisitInfo": {
            "province": "广东省",
            "city": "深圳市",
            "area": "南山区",
            "street": "高新南九道光明路888号",
            "address": "金地威新科技园18楼168号",
            "userName": "刘志明",
            "phone": phone
        },
        "customData": {
            "orderName": "下单联系人",
            "orderPhone": "18886668888",
            "address": "南山区",
            "longitude": "116.794345",
            "latitude": "33.959893",
            "areaId": "3583"
        }
    }
}

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
          "honorOrderId": "honor00010"
     }
}

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
          "orderId": "",
          "operatorlog": "0",
          "recycleOrderId": "7635189"
     }
}


def param_list():
    param_eg = ["接口参数示例："]
    param_eg.append(buyHonorMaintainValueService)
    param_eg.append(placeOrder)
    param_eg.append(submitHonorNewMachinOrder)
    param_eg.append(getHonorOrderList)
    param_eg.append(getHonorMaintainValueService)
    param_eg.append(getHonorOrderInfo)
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
