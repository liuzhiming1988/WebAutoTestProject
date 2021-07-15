#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : wms_data.py
@Author  : liuzhiming
@Time    : 2021/7/8 14:25
"""
import json
import requests
from sqlalchemy import true, false

text = """{
    "_head": {
        "_version": "0.01",
        "_msgType": "response",
        "_timestamps": "1625739567",
        "_interface": "getDetectOptionTmp",
        "_remark": ""
    },
    "_data": {
        "_data": {
            "options": [
                {
                    "id": "7263",
                    "name": "开机",
                    "item": [
                        {
                            "id": "7418",
                            "name": "正常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7419",
                            "name": "不开机",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7420",
                            "name": "开机异常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "7424",
                    "name": "账号锁",
                    "item": [
                        {
                            "id": "7425",
                            "name": "已注销",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7426",
                            "name": "无法注销/隐藏账号",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "7421",
                    "name": "是否全新",
                    "item": [
                        {
                            "id": "7422",
                            "name": "全新机",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7423",
                            "name": "二手机",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "918",
                    "name": "型号",
                    "item": [
                        {
                            "id": "1083",
                            "name": "其他型号",
                            "item": [ ],
                            "type": "1",
                            "singleFlag": true
                        },
                        {
                            "id": "1883",
                            "name": "A1549",
                            "item": [ ],
                            "type": "1",
                            "singleFlag": true
                        },
                        {
                            "id": "2245",
                            "name": "A1586",
                            "item": [ ],
                            "type": "1",
                            "singleFlag": true
                        },
                        {
                            "id": "2246",
                            "name": "A1589",
                            "item": [ ],
                            "type": "1",
                            "singleFlag": true
                        }
                    ],
                    "type": "1",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "39",
                    "name": "颜色",
                    "item": [
                        {
                            "id": "42",
                            "name": "银色",
                            "item": [ ],
                            "type": "1",
                            "singleFlag": true
                        },
                        {
                            "id": "44",
                            "name": "金色",
                            "item": [ ],
                            "type": "1",
                            "singleFlag": true
                        },
                        {
                            "id": "1091",
                            "name": "深空灰色",
                            "item": [ ],
                            "type": "1",
                            "singleFlag": true
                        }
                    ],
                    "type": "1",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "32",
                    "name": "存储容量",
                    "item": [
                        {
                            "id": "34",
                            "name": "16GB",
                            "item": [ ],
                            "type": "1",
                            "singleFlag": true
                        },
                        {
                            "id": "35",
                            "name": "32GB",
                            "item": [ ],
                            "type": "1",
                            "singleFlag": true
                        },
                        {
                            "id": "36",
                            "name": "64GB",
                            "item": [ ],
                            "type": "1",
                            "singleFlag": true
                        },
                        {
                            "id": "37",
                            "name": "128GB",
                            "item": [ ],
                            "type": "1",
                            "singleFlag": true
                        }
                    ],
                    "type": "1",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "2232",
                    "name": "机身内存",
                    "item": [
                        {
                            "id": "2233",
                            "name": "1GB",
                            "item": [ ],
                            "type": "1",
                            "singleFlag": true
                        }
                    ],
                    "type": "1",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "122",
                    "name": "制式",
                    "item": [
                        {
                            "id": "124",
                            "name": "移动版",
                            "item": [ ],
                            "type": "1",
                            "singleFlag": true
                        },
                        {
                            "id": "130",
                            "name": "全网通",
                            "item": [ ],
                            "type": "1",
                            "singleFlag": true
                        },
                        {
                            "id": "471",
                            "name": "移动联通",
                            "item": [ ],
                            "type": "1",
                            "singleFlag": true
                        },
                        {
                            "id": "472",
                            "name": "联通电信",
                            "item": [ ],
                            "type": "1",
                            "singleFlag": true
                        }
                    ],
                    "type": "1",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "16",
                    "name": "保修期",
                    "item": [
                        {
                            "id": "17",
                            "name": "剩余保修期大于一个月",
                            "item": [ ],
                            "type": "1",
                            "singleFlag": true
                        },
                        {
                            "id": "18",
                            "name": "剩余保修期不足一个月或过保",
                            "item": [ ],
                            "type": "1",
                            "singleFlag": true
                        }
                    ],
                    "type": "1",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "11",
                    "name": "购买渠道",
                    "item": [
                        {
                            "id": "12",
                            "name": "大陆国行",
                            "item": [ ],
                            "type": "1",
                            "singleFlag": true
                        },
                        {
                            "id": "13",
                            "name": "香港行货",
                            "item": [ ],
                            "type": "1",
                            "singleFlag": true
                        },
                        {
                            "id": "14",
                            "name": "其他国家地区-无锁版",
                            "item": [ ],
                            "type": "1",
                            "singleFlag": true
                        },
                        {
                            "id": "15",
                            "name": "其他国家地区-有锁版",
                            "item": [ ],
                            "type": "1",
                            "singleFlag": true
                        },
                        {
                            "id": "1124",
                            "name": "国行官换机/官翻机",
                            "item": [ ],
                            "type": "1",
                            "singleFlag": true
                        },
                        {
                            "id": "6047",
                            "name": "国行展示机",
                            "item": [ ],
                            "type": "1",
                            "singleFlag": true
                        },
                        {
                            "id": "6116",
                            "name": "国行BS机",
                            "item": [ ],
                            "type": "1",
                            "singleFlag": true
                        },
                        {
                            "id": "7630",
                            "name": "监管机",
                            "item": [ ],
                            "type": "1",
                            "singleFlag": true
                        },
                        {
                            "id": "8012",
                            "name": "官修机",
                            "item": [ ],
                            "type": "1",
                            "singleFlag": true
                        }
                    ],
                    "type": "1",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "7427",
                    "name": "机身划痕",
                    "item": [
                        {
                            "id": "7428",
                            "name": "完好",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7429",
                            "name": "轻微",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7430",
                            "name": "明显",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "7431",
                    "name": "机身磕碰/掉漆/刻字",
                    "item": [
                        {
                            "id": "7432",
                            "name": "完好",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7433",
                            "name": "轻微",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7434",
                            "name": "明显",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "3",
                    "isMust": "1"
                },
                {
                    "id": "7435",
                    "name": "机身异常",
                    "item": [
                        {
                            "id": "7436",
                            "name": "无",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7437",
                            "name": "机身有弯曲",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        },
                        {
                            "id": "7438",
                            "name": "机身有缝隙",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        },
                        {
                            "id": "7439",
                            "name": "背面有破损",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        },
                        {
                            "id": "7440",
                            "name": "中框有断裂",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        }
                    ],
                    "type": "2",
                    "spotType": "3",
                    "isMust": "1"
                },
                {
                    "id": "7441",
                    "name": "屏幕支架断裂/脱胶",
                    "item": [
                        {
                            "id": "7442",
                            "name": "无",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7443",
                            "name": "有",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "3",
                    "isMust": "1"
                },
                {
                    "id": "7444",
                    "name": "屏幕划痕",
                    "item": [
                        {
                            "id": "7445",
                            "name": "完好",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7446",
                            "name": "轻微划痕",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7447",
                            "name": "明显划痕",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "8054",
                            "name": "屏幕划伤",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "3",
                    "isMust": "1"
                },
                {
                    "id": "7448",
                    "name": "屏幕碎裂",
                    "item": [
                        {
                            "id": "7449",
                            "name": "无",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7450",
                            "name": "屏幕碎裂",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "8055",
                            "name": "屏幕小缺角",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "3",
                    "isMust": "1"
                },
                {
                    "id": "7451",
                    "name": "屏幕气泡",
                    "item": [
                        {
                            "id": "7452",
                            "name": "无",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7453",
                            "name": "有",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "3",
                    "isMust": "2"
                },
                {
                    "id": "7454",
                    "name": "亮点/坏点",
                    "item": [
                        {
                            "id": "7460",
                            "name": "无",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7461",
                            "name": "有",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "3",
                    "isMust": "2"
                },
                {
                    "id": "7455",
                    "name": "进灰",
                    "item": [
                        {
                            "id": "7462",
                            "name": "无",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7463",
                            "name": "有",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "3",
                    "isMust": "2"
                },
                {
                    "id": "7456",
                    "name": "亮斑",
                    "item": [
                        {
                            "id": "7464",
                            "name": "无",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7465",
                            "name": "轻微",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7466",
                            "name": "明显",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "3",
                    "isMust": "2"
                },
                {
                    "id": "7457",
                    "name": "色差/透字",
                    "item": [
                        {
                            "id": "7467",
                            "name": "无",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7468",
                            "name": "轻微",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7469",
                            "name": "明显",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "3",
                    "isMust": "2"
                },
                {
                    "id": "7458",
                    "name": "色斑/压伤",
                    "item": [
                        {
                            "id": "7470",
                            "name": "无",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7471",
                            "name": "轻微",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7472",
                            "name": "明显",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "3",
                    "isMust": "2"
                },
                {
                    "id": "7459",
                    "name": "显示异常",
                    "item": [
                        {
                            "id": "7473",
                            "name": "无",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7474",
                            "name": "漏液",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        },
                        {
                            "id": "7475",
                            "name": "错乱花屏",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        },
                        {
                            "id": "7476",
                            "name": "屏生线",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        },
                        {
                            "id": "7477",
                            "name": "屏幕抖动",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        },
                        {
                            "id": "7478",
                            "name": "显示不均匀",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        },
                        {
                            "id": "7479",
                            "name": "间歇性不显示",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        }
                    ],
                    "type": "2",
                    "spotType": "3",
                    "isMust": "2"
                },
                {
                    "id": "7480",
                    "name": "触屏功能",
                    "item": [
                        {
                            "id": "7481",
                            "name": "正常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7482",
                            "name": "触屏失灵",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7483",
                            "name": "触屏间歇性失灵",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "7484",
                    "name": "扬声器",
                    "item": [
                        {
                            "id": "7487",
                            "name": "正常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7488",
                            "name": "杂音/小声",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7489",
                            "name": "无声",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "7485",
                    "name": "听筒",
                    "item": [
                        {
                            "id": "7490",
                            "name": "正常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7491",
                            "name": "杂音/小声",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7492",
                            "name": "无声",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "7486",
                    "name": "麦克风",
                    "item": [
                        {
                            "id": "7493",
                            "name": "正常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7494",
                            "name": "麦克风小声",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        },
                        {
                            "id": "7495",
                            "name": "录音无声",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        },
                        {
                            "id": "7496",
                            "name": "打电话无声",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        },
                        {
                            "id": "7497",
                            "name": "录像无声",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        }
                    ],
                    "type": "2",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "7498",
                    "name": "前像头功能",
                    "item": [
                        {
                            "id": "7499",
                            "name": "正常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7500",
                            "name": "拍照有黑斑",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7501",
                            "name": "拍照画面抖动",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7502",
                            "name": "无法聚焦",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7503",
                            "name": "无法启用",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7504",
                            "name": "不支持",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "7505",
                    "name": "前像头外观",
                    "item": [
                        {
                            "id": "7506",
                            "name": "正常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7507",
                            "name": "像头有进灰",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7508",
                            "name": "不支持",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "3",
                    "isMust": "2"
                },
                {
                    "id": "7509",
                    "name": "后像头功能",
                    "item": [
                        {
                            "id": "7510",
                            "name": "正常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7511",
                            "name": "拍照有黑斑",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7512",
                            "name": "拍照画面抖动",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7513",
                            "name": "无法聚焦",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7514",
                            "name": "无法启用",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7515",
                            "name": "不支持",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "7516",
                    "name": "后像头外观",
                    "item": [
                        {
                            "id": "7517",
                            "name": "正常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7518",
                            "name": "像头有进灰",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7519",
                            "name": "像头镜片碎裂",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7520",
                            "name": "不支持",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "3",
                    "isMust": "2"
                },
                {
                    "id": "7521",
                    "name": "WiFi",
                    "item": [
                        {
                            "id": "7522",
                            "name": "功能正常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7523",
                            "name": "信号弱",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7524",
                            "name": "无法打开",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7525",
                            "name": "无法使用",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7526",
                            "name": "不支持",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "7527",
                    "name": "蓝牙",
                    "item": [
                        {
                            "id": "7528",
                            "name": "功能正常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7529",
                            "name": "无法搜索设备",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7530",
                            "name": "无法打开",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7615",
                            "name": "不支持",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "7531",
                    "name": "SIM卡托",
                    "item": [
                        {
                            "id": "7532",
                            "name": "完好",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7533",
                            "name": "卡托损坏/缺失",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7534",
                            "name": "无法取出",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "7535",
                    "name": "SIM卡1",
                    "item": [
                        {
                            "id": "7536",
                            "name": "正常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7537",
                            "name": "不读卡",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7538",
                            "name": "无信号",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7539",
                            "name": "不通话",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "7540",
                    "name": "SIM卡2",
                    "item": [
                        {
                            "id": "7541",
                            "name": "正常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7542",
                            "name": "不读卡",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7543",
                            "name": "无信号",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7544",
                            "name": "不通话",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7545",
                            "name": "不支持",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "7546",
                    "name": "基带",
                    "item": [
                        {
                            "id": "7547",
                            "name": "正常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7548",
                            "name": "无基带",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "7549",
                    "name": "光线感应",
                    "item": [
                        {
                            "id": "7553",
                            "name": "正常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7554",
                            "name": "功能异常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7555",
                            "name": "不支持",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "7550",
                    "name": "距离感应",
                    "item": [
                        {
                            "id": "7556",
                            "name": "正常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7557",
                            "name": "功能异常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7558",
                            "name": "不支持",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "7551",
                    "name": "指南针",
                    "item": [
                        {
                            "id": "7559",
                            "name": "正常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7560",
                            "name": "功能异常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7561",
                            "name": "不支持",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "7552",
                    "name": "按键",
                    "item": [
                        {
                            "id": "7562",
                            "name": "正常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7563",
                            "name": "开关键异常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        },
                        {
                            "id": "7564",
                            "name": "音量键异常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        },
                        {
                            "id": "7565",
                            "name": "震动/静音键异常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        },
                        {
                            "id": "7566",
                            "name": "HOME键异常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        }
                    ],
                    "type": "2",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "7569",
                    "name": "有线充电",
                    "item": [
                        {
                            "id": "7570",
                            "name": "正常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7571",
                            "name": "无法充电",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7572",
                            "name": "充电孔接触不良",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "7573",
                    "name": "USB联机",
                    "item": [
                        {
                            "id": "7574",
                            "name": "正常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7575",
                            "name": "无法连接电脑",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "7576",
                    "name": "振动",
                    "item": [
                        {
                            "id": "7578",
                            "name": "有振动",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7579",
                            "name": "无振动",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "7577",
                    "name": "闪光灯",
                    "item": [
                        {
                            "id": "7580",
                            "name": "正常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7581",
                            "name": "功能异常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "7582",
                    "name": "指纹解锁",
                    "item": [
                        {
                            "id": "7586",
                            "name": "正常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7587",
                            "name": "异常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7588",
                            "name": "不支持",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "7583",
                    "name": "Face ID",
                    "item": [
                        {
                            "id": "7589",
                            "name": "正常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7590",
                            "name": "异常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7591",
                            "name": "不支持",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        }
                    ],
                    "type": "2",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "7598",
                    "name": "维修/异常机况",
                    "item": [
                        {
                            "id": "7599",
                            "name": "无维修",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7600",
                            "name": "更换屏幕玻璃盖板",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        },
                        {
                            "id": "7601",
                            "name": "更换屏幕-高仿屏/山寨屏",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        },
                        {
                            "id": "7602",
                            "name": "屏幕维修",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        },
                        {
                            "id": "7603",
                            "name": "更换电池",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        },
                        {
                            "id": "7604",
                            "name": "电池鼓包",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        },
                        {
                            "id": "7605",
                            "name": "更换后盖",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        },
                        {
                            "id": "7606",
                            "name": "缺件/少螺丝",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        },
                        {
                            "id": "7607",
                            "name": "原厂防拆标破损",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        },
                        {
                            "id": "7608",
                            "name": "更换摄像头",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        },
                        {
                            "id": "7609",
                            "name": "更换外壳",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        },
                        {
                            "id": "7610",
                            "name": "主板维修/故障",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        },
                        {
                            "id": "7611",
                            "name": "序列号异常",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        }
                    ],
                    "type": "2",
                    "spotType": "2",
                    "isMust": ""
                },
                {
                    "id": "7612",
                    "name": "进水",
                    "item": [
                        {
                            "id": "7613",
                            "name": "无",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": true
                        },
                        {
                            "id": "7614",
                            "name": "机身浸液/受潮",
                            "item": [ ],
                            "type": "2",
                            "singleFlag": false
                        }
                    ],
                    "type": "2",
                    "spotType": "2",
                    "isMust": ""
                }
            ],
            "select": [ ],
            "objectivitySum": "37",
            "subjectivitySum": "14",
            "subjectivityMustSum": "5",
            "subjectivityNotMustSum": "9"
        },
        "_ret": 0,
        "_errCode": "0",
        "_errStr": "success"
    }
}
"""

str_final = """
{
    "_head": {
        "_interface": "productEvaluate"
    }, 
    "_param": {
        "engineerOptions": [
            {
                "id": "7263", 
                "name": "开机", 
                "type": "2", 
                "item": [
                    {
                        "id": "7418", 
                        "name": "正常", 
                        "type": "2"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "7424", 
                "name": "账号锁", 
                "type": "2", 
                "item": [
                    {
                        "id": "7425", 
                        "name": "已注销", 
                        "type": "2"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "7421", 
                "name": "是否全新", 
                "type": "2", 
                "item": [
                    {
                        "id": "7422", 
                        "name": "全新机", 
                        "type": "2"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "918", 
                "name": "型号", 
                "type": "1", 
                "item": [
                    {
                        "id": "1083", 
                        "name": "其他型号", 
                        "type": "1"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "39", 
                "name": "颜色", 
                "type": "1", 
                "item": [
                    {
                        "id": "42", 
                        "name": "银色", 
                        "type": "1"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "32", 
                "name": "存储容量", 
                "type": "1", 
                "item": [
                    {
                        "id": "34", 
                        "name": "16GB", 
                        "type": "1"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "2232", 
                "name": "机身内存", 
                "type": "1", 
                "item": [
                    {
                        "id": "2233", 
                        "name": "1GB", 
                        "type": "1"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "122", 
                "name": "制式", 
                "type": "1", 
                "item": [
                    {
                        "id": "124", 
                        "name": "移动版", 
                        "type": "1"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "16", 
                "name": "保修期", 
                "type": "1", 
                "item": [
                    {
                        "id": "17", 
                        "name": "剩余保修期大于一个月", 
                        "type": "1"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "11", 
                "name": "购买渠道", 
                "type": "1", 
                "item": [
                    {
                        "id": "12", 
                        "name": "大陆国行", 
                        "type": "1"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "7427", 
                "name": "机身划痕", 
                "type": "2", 
                "item": [
                    {
                        "id": "7428", 
                        "name": "完好", 
                        "type": "2"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "7431", 
                "name": "机身磕碰/掉漆/刻字", 
                "type": "2", 
                "item": [
                    {
                        "id": "7432", 
                        "name": "完好", 
                        "type": "2"
                    }
                ], 
                "spotType": "3", 
                "isMust": "1"
            }, 
            {
                "id": "7435", 
                "name": "机身异常", 
                "type": "2", 
                "item": [
                    {
                        "id": "7436", 
                        "name": "无", 
                        "type": "2"
                    }
                ], 
                "spotType": "3", 
                "isMust": "1"
            }, 
            {
                "id": "7441", 
                "name": "屏幕支架断裂/脱胶", 
                "type": "2", 
                "item": [
                    {
                        "id": "7442", 
                        "name": "无", 
                        "type": "2"
                    }
                ], 
                "spotType": "3", 
                "isMust": "1"
            }, 
            {
                "id": "7444", 
                "name": "屏幕划痕", 
                "type": "2", 
                "item": [
                    {
                        "id": "7445", 
                        "name": "完好", 
                        "type": "2"
                    }
                ], 
                "spotType": "3", 
                "isMust": "1"
            }, 
            {
                "id": "7448", 
                "name": "屏幕碎裂", 
                "type": "2", 
                "item": [
                    {
                        "id": "7449", 
                        "name": "无", 
                        "type": "2"
                    }
                ], 
                "spotType": "3", 
                "isMust": "1"
            }, 
            {
                "id": "7451", 
                "name": "屏幕气泡", 
                "type": "2", 
                "item": [
                    {
                        "id": "7452", 
                        "name": "无", 
                        "type": "2"
                    }
                ], 
                "spotType": "3", 
                "isMust": "2"
            }, 
            {
                "id": "7454", 
                "name": "亮点/坏点", 
                "type": "2", 
                "item": [
                    {
                        "id": "7460", 
                        "name": "无", 
                        "type": "2"
                    }
                ], 
                "spotType": "3", 
                "isMust": "2"
            }, 
            {
                "id": "7455", 
                "name": "进灰", 
                "type": "2", 
                "item": [
                    {
                        "id": "7462", 
                        "name": "无", 
                        "type": "2"
                    }
                ], 
                "spotType": "3", 
                "isMust": "2"
            }, 
            {
                "id": "7456", 
                "name": "亮斑", 
                "type": "2", 
                "item": [
                    {
                        "id": "7464", 
                        "name": "无", 
                        "type": "2"
                    }
                ], 
                "spotType": "3", 
                "isMust": "2"
            }, 
            {
                "id": "7457", 
                "name": "色差/透字", 
                "type": "2", 
                "item": [
                    {
                        "id": "7467", 
                        "name": "无", 
                        "type": "2"
                    }
                ], 
                "spotType": "3", 
                "isMust": "2"
            }, 
            {
                "id": "7458", 
                "name": "色斑/压伤", 
                "type": "2", 
                "item": [
                    {
                        "id": "7470", 
                        "name": "无", 
                        "type": "2"
                    }
                ], 
                "spotType": "3", 
                "isMust": "2"
            }, 
            {
                "id": "7459", 
                "name": "显示异常", 
                "type": "2", 
                "item": [
                    {
                        "id": "7473", 
                        "name": "无", 
                        "type": "2"
                    }
                ], 
                "spotType": "3", 
                "isMust": "2"
            }, 
            {
                "id": "7480", 
                "name": "触屏功能", 
                "type": "2", 
                "item": [
                    {
                        "id": "7481", 
                        "name": "正常", 
                        "type": "2"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "7484", 
                "name": "扬声器", 
                "type": "2", 
                "item": [
                    {
                        "id": "7487", 
                        "name": "正常", 
                        "type": "2"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "7485", 
                "name": "听筒", 
                "type": "2", 
                "item": [
                    {
                        "id": "7490", 
                        "name": "正常", 
                        "type": "2"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "7486", 
                "name": "麦克风", 
                "type": "2", 
                "item": [
                    {
                        "id": "7493", 
                        "name": "正常", 
                        "type": "2"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "7498", 
                "name": "前像头功能", 
                "type": "2", 
                "item": [
                    {
                        "id": "7499", 
                        "name": "正常", 
                        "type": "2"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "7505", 
                "name": "前像头外观", 
                "type": "2", 
                "item": [
                    {
                        "id": "7506", 
                        "name": "正常", 
                        "type": "2"
                    }
                ], 
                "spotType": "3", 
                "isMust": "2"
            }, 
            {
                "id": "7509", 
                "name": "后像头功能", 
                "type": "2", 
                "item": [
                    {
                        "id": "7510", 
                        "name": "正常", 
                        "type": "2"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "7516", 
                "name": "后像头外观", 
                "type": "2", 
                "item": [
                    {
                        "id": "7517", 
                        "name": "正常", 
                        "type": "2"
                    }
                ], 
                "spotType": "3", 
                "isMust": "2"
            }, 
            {
                "id": "7521", 
                "name": "WiFi", 
                "type": "2", 
                "item": [
                    {
                        "id": "7522", 
                        "name": "功能正常", 
                        "type": "2"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "7527", 
                "name": "蓝牙", 
                "type": "2", 
                "item": [
                    {
                        "id": "7528", 
                        "name": "功能正常", 
                        "type": "2"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "7531", 
                "name": "SIM卡托", 
                "type": "2", 
                "item": [
                    {
                        "id": "7532", 
                        "name": "完好", 
                        "type": "2"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "7535", 
                "name": "SIM卡1", 
                "type": "2", 
                "item": [
                    {
                        "id": "7536", 
                        "name": "正常", 
                        "type": "2"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "7540", 
                "name": "SIM卡2", 
                "type": "2", 
                "item": [
                    {
                        "id": "7541", 
                        "name": "正常", 
                        "type": "2"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "7546", 
                "name": "基带", 
                "type": "2", 
                "item": [
                    {
                        "id": "7547", 
                        "name": "正常", 
                        "type": "2"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "7549", 
                "name": "光线感应", 
                "type": "2", 
                "item": [
                    {
                        "id": "7553", 
                        "name": "正常", 
                        "type": "2"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "7550", 
                "name": "距离感应", 
                "type": "2", 
                "item": [
                    {
                        "id": "7556", 
                        "name": "正常", 
                        "type": "2"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "7551", 
                "name": "指南针", 
                "type": "2", 
                "item": [
                    {
                        "id": "7559", 
                        "name": "正常", 
                        "type": "2"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "7552", 
                "name": "按键", 
                "type": "2", 
                "item": [
                    {
                        "id": "7562", 
                        "name": "正常", 
                        "type": "2"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "7569", 
                "name": "有线充电", 
                "type": "2", 
                "item": [
                    {
                        "id": "7570", 
                        "name": "正常", 
                        "type": "2"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "7573", 
                "name": "USB联机", 
                "type": "2", 
                "item": [
                    {
                        "id": "7574", 
                        "name": "正常", 
                        "type": "2"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "7576", 
                "name": "振动", 
                "type": "2", 
                "item": [
                    {
                        "id": "7578", 
                        "name": "有振动", 
                        "type": "2"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "7577", 
                "name": "闪光灯", 
                "type": "2", 
                "item": [
                    {
                        "id": "7580", 
                        "name": "正常", 
                        "type": "2"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "7582", 
                "name": "指纹解锁", 
                "type": "2", 
                "item": [
                    {
                        "id": "7586", 
                        "name": "正常", 
                        "type": "2"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "7583", 
                "name": "Face ID", 
                "type": "2", 
                "item": [
                    {
                        "id": "7589", 
                        "name": "正常", 
                        "type": "2"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "7598", 
                "name": "维修/异常机况", 
                "type": "2", 
                "item": [
                    {
                        "id": "7599", 
                        "name": "无维修", 
                        "type": "2"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }, 
            {
                "id": "7612", 
                "name": "进水", 
                "type": "2", 
                "item": [
                    {
                        "id": "7613", 
                        "name": "无", 
                        "type": "2"
                    }
                ], 
                "spotType": "2", 
                "isMust": ""
            }
        ], 
        "seriesNum": "ZY0101210708000027", 
        "partnerCode": "100002", 
        "productId": "30748", 
        "orderId": "7634420", 
        "detTpl": 2, 
        "channelId": "10000060", 
        "aIdList": [ ], 
        "optionList": [ ], 
        "cIdList": [ ], 
        "skuList": [
            "1083", 
            "42", 
            "34", 
            "2233", 
            "124", 
            "17", 
            "12"
        ], 
        "isOverInsurance": "0", 
        "user_id": "1930", 
        "userId": "1930", 
        "login_token": "8495e3b8fd6bcfbda8115ded3a308190"
    }
}
"""


text = json.loads(text)
str_final = json.loads(str_final)

options = text["_data"]["_data"]["options"]

options_final = str_final["_param"]["engineerOptions"]

# print(json.dumps(options,indent=5,ensure_ascii=False))
# print(json.dumps(options_final,indent=5,ensure_ascii=False))

for x in options:
    y = len(x["item"])
    raw_list = x["item"]
    del raw_list[1:y]
    item_son=raw_list[0]
    del item_son["item"]
    del item_son["singleFlag"]

    # print(raw_list)
# print(json.dumps(options, indent=6, ensure_ascii=False))

uDetOptions=["12","34","44","1083","83","79","3244","3247","61","6930","55","59","53","65","223","23","3246","2171","21","5535","7641"]

detect_select = []
for x in options:
    y = len(x["item"])
    for i in range(y):
        value = x["item"][i]["id"]
        detect_select.append(value)

# print(detect_select)
# get sku list
# print(detect_select[3:10])
# print(len(options))

new_list = []
for x in uDetOptions:
    for y in detect_select:
        if x==y:
            new_list.append(x)
        else:
            pass
# print(new_list)
# print(new_list[0:2])


sku_list = ["1083","42","34","2233","124","17","12"]
test = "adbcsdre"
# print(test[:-2])

import time
time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

print(time_str)
print(type(time_str))


