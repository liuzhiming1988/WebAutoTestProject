#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : patrol_system_info.py
@Author  : liuzhiming
@Time    : 2021/11/4 17:25
"""

import random
import json

# product_check_item_34   【41567】34项检测标准——检测标准化产品信息http://wiki.huishoubao.com/web/#/105?page_id=3295
checkList_34 = [
    {
        "answerList": [
            {
                "answerId": "9015",
                "answerName": "iCloud已注销",
                "answerWeight": "100",
                "singleFlag": "true"
            },
            {
                "answerId": "9016",
                "answerName": "iCloud无法注销",
                "answerWeight": "90",
                "singleFlag": "true"
            }
        ],
        "questionId": "8996",
        "questionName": "iCloud账号"
    },
    {
        "answerList": [
            {
                "answerId": "9019",
                "answerName": "正常开机",
                "answerWeight": "100",
                "singleFlag": "true"
            },
            {
                "answerId": "9021",
                "answerName": "有开机密码",
                "answerWeight": "90",
                "singleFlag": "true"
            },
            {
                "answerId": "9022",
                "answerName": "重启/不能进桌面",
                "answerWeight": "80",
                "singleFlag": "true"
            },
            {
                "answerId": "9023",
                "answerName": "无法开机",
                "answerWeight": "70",
                "singleFlag": "true"
            },
            {
                "answerId": "9024",
                "answerName": "可进入桌面，进入后间歇性自动重启",
                "answerWeight": "85",
                "singleFlag": "true"
            }
        ],
        "questionId": "8998",
        "questionName": "开机情况"
    },
    {
        "answerList": [
            {
                "answerId": "9025",
                "answerName": "二手",
                "answerWeight": "80",
                "singleFlag": "true"
            },
            {
                "answerId": "9026",
                "answerName": "全新（拆封/整套/未激活/未使用）",
                "answerWeight": "90",
                "singleFlag": "true"
            },
            {
                "answerId": "9027",
                "answerName": "全新（未拆封/未激活）",
                "answerWeight": "95",
                "singleFlag": "true"
            }
        ],
        "questionId": "7421",
        "questionName": "是否全新"
    },
    {
        "answerList": [
            {
                "answerId": "9028",
                "answerName": "完好",
                "answerWeight": "100",
                "singleFlag": "true"
            },
            {
                "answerId": "9029",
                "answerName": "轻微划痕（<10毫米）",
                "answerWeight": "90",
                "singleFlag": "true"
            },
            {
                "answerId": "9030",
                "answerName": "明显划痕（≥10毫米）/轻微磕碰（≤3毫米）",
                "answerWeight": "80",
                "singleFlag": "true"
            },
            {
                "answerId": "9031",
                "answerName": "外壳明显磕碰/掉漆（≥3毫米）",
                "answerWeight": "70",
                "singleFlag": "true"
            },
            {
                "answerId": "9032",
                "answerName": "壳缺失/裂缝/孔变形/翘起/刻字",
                "answerWeight": "60",
                "singleFlag": "true"
            },
            {
                "answerId": "9033",
                "answerName": "屏支架断裂/错位",
                "answerWeight": "50",
                "singleFlag": "true"
            },
            {
                "answerId": "9034",
                "answerName": "壳缺失/裂缝/孔变形/翘起/刻字+屏支架断裂/错位",
                "answerWeight": "40",
                "singleFlag": "true"
            }
        ],
        "questionId": "8999",
        "questionName": "边框背板"
    },
    {
        "answerList": [
            {
                "answerId": "9035",
                "answerName": "完好",
                "answerWeight": "10",
                "singleFlag": "true"
            },
            {
                "answerId": "9036",
                "answerName": "轻微弯曲（弯曲1-2毫米）",
                "answerWeight": "9",
                "singleFlag": "true"
            },
            {
                "answerId": "9037",
                "answerName": "明显弯曲（弯曲≥2毫米）",
                "answerWeight": "8",
                "singleFlag": "true"
            }
        ],
        "questionId": "7859",
        "questionName": "机身弯曲"
    },
    {
        "answerList": [
            {
                "answerId": "9039",
                "answerName": "完好",
                "answerWeight": "100",
                "singleFlag": "true"
            },
            {
                "answerId": "9040",
                "answerName": "轻微划痕（<10毫米）",
                "answerWeight": "90",
                "singleFlag": "true"
            },
            {
                "answerId": "9041",
                "answerName": "明显划痕（≥10毫米）",
                "answerWeight": "80",
                "singleFlag": "true"
            },
            {
                "answerId": "9042",
                "answerName": "屏有硬划痕（<10毫米）",
                "answerWeight": "70",
                "singleFlag": "true"
            },
            {
                "answerId": "9043",
                "answerName": "屏有硬划痕/脱胶/气泡",
                "answerWeight": "60",
                "singleFlag": "true"
            },
            {
                "answerId": "9044",
                "answerName": "屏幕有小缺角（<1.5毫米）",
                "answerWeight": "50",
                "singleFlag": "true"
            },
            {
                "answerId": "9045",
                "answerName": "屏幕有碎裂/缺角（≥1.5毫米）",
                "answerWeight": "40",
                "singleFlag": "true"
            }
        ],
        "questionId": "9038",
        "questionName": "屏幕外观"
    },
    {
        "answerList": [
            {
                "answerId": "9047",
                "answerName": "完好",
                "answerWeight": "100",
                "singleFlag": "true"
            },
            {
                "answerId": "9048",
                "answerName": "显示色差（发黄/红屏/轻微透图）",
                "answerWeight": "90",
                "singleFlag": "true"
            },
            {
                "answerId": "9049",
                "answerName": "轻微亮度问题（亮点/亮斑/黑角）",
                "answerWeight": "80",
                "singleFlag": "true"
            },
            {
                "answerId": "9050",
                "answerName": "显示坏点（白色或黑色界面下有颜色点）",
                "answerWeight": "70",
                "singleFlag": "true"
            },
            {
                "answerId": "9051",
                "answerName": "显示色斑（白色界面下有非黑紫绿斑块）",
                "answerWeight": "60",
                "singleFlag": "true"
            },
            {
                "answerId": "9052",
                "answerName": "显示老化（显示透图/背光不亮）",
                "answerWeight": "50",
                "singleFlag": "true"
            },
            {
                "answerId": "9053",
                "answerName": "屏幕压伤（黑色界面下有静止的非黑色区域）",
                "answerWeight": "40",
                "singleFlag": "true"
            },
            {
                "answerId": "9054",
                "answerName": "屏幕漏液/闪屏/屏生线/屏抖动",
                "answerWeight": "30",
                "singleFlag": "true"
            },
            {
                "answerId": "9055",
                "answerName": "无法显示/全花屏",
                "answerWeight": "20",
                "singleFlag": "true"
            }
        ],
        "questionId": "9046",
        "questionName": "屏幕显示"
    },
    {
        "answerList": [
            {
                "answerId": "7481",
                "answerName": "正常",
                "answerWeight": "100",
                "singleFlag": "true"
            },
            {
                "answerId": "9056",
                "answerName": "触屏延迟/失灵",
                "answerWeight": "70",
                "singleFlag": "true"
            }
        ],
        "questionId": "7480",
        "questionName": "触屏功能"
    },
    {
        "answerList": [
            {
                "answerId": "9057",
                "answerName": "正常",
                "answerWeight": "100",
                "singleFlag": "true"
            },
            {
                "answerId": "9058",
                "answerName": "无线异常",
                "answerWeight": "90",
                "singleFlag": "true"
            }
        ],
        "questionId": "9000",
        "questionName": "无线功能（WIFI/蓝牙）"
    },
    {
        "answerList": [
            {
                "answerId": "9059",
                "answerName": "正常",
                "answerWeight": "100",
                "singleFlag": "true"
            },
            {
                "answerId": "9060",
                "answerName": "通话异常（不读卡/不通话/无信号/无基带）",
                "answerWeight": "90",
                "singleFlag": "true"
            }
        ],
        "questionId": "9001",
        "questionName": "通话功能"
    },
    {
        "answerList": [
            {
                "answerId": "9062",
                "answerName": "正常",
                "answerWeight": "100",
                "singleFlag": "true"
            },
            {
                "answerId": "9063",
                "answerName": "拍照有黑斑",
                "answerWeight": "90",
                "singleFlag": "true"
            },
            {
                "answerId": "9064",
                "answerName": "拍照画面异常（抖动/模糊/不对焦/颠倒/分层）",
                "answerWeight": "80",
                "singleFlag": "true"
            },
            {
                "answerId": "9065",
                "answerName": "无法开关/报错/全黑/闪光灯坏",
                "answerWeight": "70",
                "singleFlag": "true"
            }
        ],
        "questionId": "9061",
        "questionName": "前置摄像头"
    },
    {
        "answerList": [
            {
                "answerId": "9067",
                "answerName": "正常",
                "answerWeight": "100",
                "singleFlag": "true"
            },
            {
                "answerId": "9068",
                "answerName": "拍照有黑斑",
                "answerWeight": "90",
                "singleFlag": "true"
            },
            {
                "answerId": "9069",
                "answerName": "拍照画面异常（抖动/模糊/不对焦/颠倒/分层）",
                "answerWeight": "80",
                "singleFlag": "true"
            },
            {
                "answerId": "9070",
                "answerName": "无法开关/报错/全黑/闪光灯坏",
                "answerWeight": "70",
                "singleFlag": "true"
            }
        ],
        "questionId": "9066",
        "questionName": "后置摄像头"
    },
    {
        "answerList": [
            {
                "answerId": "9071",
                "answerName": "正常",
                "answerWeight": "100",
                "singleFlag": "true"
            },
            {
                "answerId": "9072",
                "answerName": "杂音/小声",
                "answerWeight": "90",
                "singleFlag": "true"
            },
            {
                "answerId": "9073",
                "answerName": "无声",
                "answerWeight": "80",
                "singleFlag": "true"
            }
        ],
        "questionId": "9002",
        "questionName": "声音功能（麦克风/扬声器/听筒）"
    },
    {
        "answerList": [
            {
                "answerId": "9074",
                "answerName": "正常",
                "answerWeight": "100",
                "singleFlag": "true"
            },
            {
                "answerId": "9075",
                "answerName": "屏幕传感器功能异常",
                "answerWeight": "90",
                "singleFlag": "true"
            }
        ],
        "questionId": "9003",
        "questionName": "屏幕传感器功能（光线/距离感应）"
    },
    {
        "answerList": [
            {
                "answerId": "7559",
                "answerName": "正常",
                "answerWeight": "100",
                "singleFlag": "true"
            },
            {
                "answerId": "9076",
                "answerName": "指南针功能异常",
                "answerWeight": "70",
                "singleFlag": "true"
            }
        ],
        "questionId": "7551",
        "questionName": "指南针"
    },
    {
        "answerList": [
            {
                "answerId": "9077",
                "answerName": "正常",
                "answerWeight": "100",
                "singleFlag": "true"
            },
            {
                "answerId": "9078",
                "answerName": "侧键异常",
                "answerWeight": "90",
                "singleFlag": "true"
            }
        ],
        "questionId": "9004",
        "questionName": "侧键（开关键/音量键/振动键/静音键/AI键等）"
    },
    {
        "answerList": [
            {
                "answerId": "7570",
                "answerName": "正常",
                "answerWeight": "100",
                "singleFlag": "true"
            },
            {
                "answerId": "9081",
                "answerName": "无法充电/充电孔接触不良",
                "answerWeight": "70",
                "singleFlag": "true"
            }
        ],
        "questionId": "7569",
        "questionName": "有线充电"
    },
    {
        "answerList": [
            {
                "answerId": "7574",
                "answerName": "正常",
                "answerWeight": "100",
                "singleFlag": "true"
            },
            {
                "answerId": "7575",
                "answerName": "无法连接电脑",
                "answerWeight": "90",
                "singleFlag": "true"
            }
        ],
        "questionId": "7573",
        "questionName": "USB联机"
    },
    {
        "answerList": [
            {
                "answerId": "9082",
                "answerName": "正常",
                "answerWeight": "80",
                "singleFlag": "true"
            },
            {
                "answerId": "9083",
                "answerName": "振动异常",
                "answerWeight": "70",
                "singleFlag": "true"
            }
        ],
        "questionId": "7576",
        "questionName": "振动"
    },
    {
        "answerList": [
            {
                "answerId": "9084",
                "answerName": "电池健康度≥90%",
                "answerWeight": "100",
                "singleFlag": "true"
            },
            {
                "answerId": "9085",
                "answerName": "80%≤电池健康度<90%",
                "answerWeight": "90",
                "singleFlag": "true"
            },
            {
                "answerId": "9086",
                "answerName": "电池健康度<80%",
                "answerWeight": "70",
                "singleFlag": "true"
            },
            {
                "answerId": "9192",
                "answerName": "未检测",
                "answerWeight": "50",
                "singleFlag": "true"
            }
        ],
        "questionId": "5179",
        "questionName": "电池健康度"
    },
    {
        "answerList": [
            {
                "answerId": "7589",
                "answerName": "正常",
                "answerWeight": "100",
                "singleFlag": "true"
            },
            {
                "answerId": "9088",
                "answerName": "Face ID无法录入或识别",
                "answerWeight": "80",
                "singleFlag": "true"
            }
        ],
        "questionId": "7583",
        "questionName": "Face ID"
    },
    {
        "answerList": [
            {
                "answerId": "9090",
                "answerName": "屏幕无维修",
                "answerWeight": "100",
                "singleFlag": "true"
            },
            {
                "answerId": "9091",
                "answerName": "更换屏幕玻璃盖板",
                "answerWeight": "90",
                "singleFlag": "true"
            },
            {
                "answerId": "9092",
                "answerName": "更换非原装屏",
                "answerWeight": "80",
                "singleFlag": "true"
            },
            {
                "answerId": "9093",
                "answerName": "屏幕维修",
                "answerWeight": "70",
                "singleFlag": "true"
            }
        ],
        "questionId": "9006",
        "questionName": "屏幕维修情况"
    },
    {
        "answerList": [
            {
                "answerId": "9094",
                "answerName": "主板完好",
                "answerWeight": "100",
                "singleFlag": "true"
            },
            {
                "answerId": "9095",
                "answerName": "主板维修/故障",
                "answerWeight": "90",
                "singleFlag": "true"
            },
            {
                "answerId": "9096",
                "answerName": "内存扩容",
                "answerWeight": "80",
                "singleFlag": "true"
            },
            {
                "answerId": "9097",
                "answerName": "序列号异常",
                "answerWeight": "70",
                "singleFlag": "true"
            }
        ],
        "questionId": "9007",
        "questionName": "主板维修情况"
    },
    {
        "answerList": [
            {
                "answerId": "9098",
                "answerName": "后摄像头无维修和缺失",
                "answerWeight": "100",
                "singleFlag": "true"
            },
            {
                "answerId": "9099",
                "answerName": "后摄像头维修",
                "answerWeight": "90",
                "singleFlag": "true"
            },
            {
                "answerId": "9100",
                "answerName": "后摄像头缺失",
                "answerWeight": "80",
                "singleFlag": "true"
            }
        ],
        "questionId": "9008",
        "questionName": "后摄像头维修情况"
    },
    {
        "answerList": [
            {
                "answerId": "9102",
                "answerName": "前摄像头无维修和缺失",
                "answerWeight": "100",
                "singleFlag": "true"
            },
            {
                "answerId": "9103",
                "answerName": "前摄像头维修",
                "answerWeight": "90",
                "singleFlag": "true"
            },
            {
                "answerId": "9104",
                "answerName": "前摄像头缺失",
                "answerWeight": "80",
                "singleFlag": "true"
            }
        ],
        "questionId": "9009",
        "questionName": "前摄像头维修情况"
    },
    {
        "answerList": [
            {
                "answerId": "9106",
                "answerName": "零件无维修和缺失",
                "answerWeight": "100",
                "singleFlag": "true"
            },
            {
                "answerId": "9108",
                "answerName": "维修电池/后壳/指纹",
                "answerWeight": "80",
                "singleFlag": "true"
            },
            {
                "answerId": "9109",
                "answerName": "缺失尾插小板/电池",
                "answerWeight": "70",
                "singleFlag": "true"
            },
            {
                "answerId": "9110",
                "answerName": "缺失扬声器/马达",
                "answerWeight": "60",
                "singleFlag": "true"
            }
        ],
        "questionId": "9010",
        "questionName": "其他零部件情况"
    },
    {
        "answerList": [
            {
                "answerId": "9111",
                "answerName": "无",
                "answerWeight": "100",
                "singleFlag": "true"
            },
            {
                "answerId": "9112",
                "answerName": "机身受潮（防拆标变色/非主板处生锈）",
                "answerWeight": "90",
                "singleFlag": "true"
            },
            {
                "answerId": "9113",
                "answerName": "机身进水（主板处生锈/水渍/霉斑/短路）",
                "answerWeight": "80",
                "singleFlag": "true"
            }
        ],
        "questionId": "9011",
        "questionName": "进水/受潮"
    },
    {
        "answerList": [
            {
                "answerId": "9117",
                "answerName": "已激活，可还原",
                "answerWeight": "101",
                "singleFlag": "true"
            },
            {
                "answerId": "9118",
                "answerName": "已激活，无法还原",
                "answerWeight": "80",
                "singleFlag": "true"
            },
            {
                "answerId": "9116",
                "answerName": "未激活",
                "answerWeight": "100",
                "singleFlag": "true"
            },
            {
                "answerId": "9119",
                "answerName": "无法激活",
                "answerWeight": "70",
                "singleFlag": "true"
            }
        ],
        "questionId": "9013",
        "questionName": "是否可恢复出厂设置"
    },
    {
        "answerList": [
            {
                "answerId": "9120",
                "answerName": "无售后维修案例",
                "answerWeight": "100",
                "singleFlag": "true"
            },
            {
                "answerId": "9121",
                "answerName": "有售后维修案例",
                "answerWeight": "90",
                "singleFlag": "true"
            },
            {
                "answerId": "9191",
                "answerName": "未检测售后案例",
                "answerWeight": "80",
                "singleFlag": "true"
            }
        ],
        "questionId": "9014",
        "questionName": "售后案例情况"
    }
]
skuList_34 = [
    {
        "answerList": [
            {
                "answerId": "12",
                "answerName": "大陆国行",
                "priority": "0"
            },
            {
                "answerId": "13",
                "answerName": "香港行货",
                "priority": "0"
            },
            {
                "answerId": "14",
                "answerName": "其他国家地区-无锁版",
                "priority": "0"
            },
            {
                "answerId": "15",
                "answerName": "其他国家地区-有锁版",
                "priority": "0"
            },
            {
                "answerId": "1124",
                "answerName": "国行官换机/官翻机",
                "priority": "0"
            },
            {
                "answerId": "6047",
                "answerName": "国行展示机",
                "priority": "0"
            },
            {
                "answerId": "6116",
                "answerName": "国行BS机",
                "priority": "0"
            },
            {
                "answerId": "7630",
                "answerName": "监管机",
                "priority": "0"
            },
            {
                "answerId": "8012",
                "answerName": "官修机",
                "priority": "0"
            }
        ],
        "questionId": "11",
        "questionName": "购买渠道"
    },
    {
        "answerList": [
            {
                "answerId": "130",
                "answerName": "全网通",
                "priority": "0"
            },
            {
                "answerId": "471",
                "answerName": "移动联通",
                "priority": "0"
            }
        ],
        "questionId": "122",
        "questionName": "制式"
    },
    {
        "answerList": [
            {
                "answerId": "17",
                "answerName": "剩余保修期大于一个月",
                "priority": "0"
            },
            {
                "answerId": "18",
                "answerName": "剩余保修期不足一个月或过保",
                "priority": "0"
            }
        ],
        "questionId": "16",
        "questionName": "保修期"
    },
    {
        "answerList": [
            {
                "answerId": "2236",
                "answerName": "3GB",
                "priority": "0"
            }
        ],
        "questionId": "2232",
        "questionName": "机身内存"
    },
    {
        "answerList": [
            {
                "answerId": "36",
                "answerName": "64GB",
                "priority": "0"
            },
            {
                "answerId": "38",
                "answerName": "256GB",
                "priority": "0"
            }
        ],
        "questionId": "32",
        "questionName": "存储容量"
    },
    {
        "answerList": [
            {
                "answerId": "42",
                "answerName": "银色",
                "priority": "0"
            },
            {
                "answerId": "1091",
                "answerName": "深空灰色",
                "priority": "0"
            }
        ],
        "questionId": "39",
        "questionName": "颜色"
    },
    {
        "answerList": [
            {
                "answerId": "1083",
                "answerName": "其他型号",
                "priority": "0"
            },
            {
                "answerId": "1773",
                "answerName": "A1901",
                "priority": "0"
            },
            {
                "answerId": "2241",
                "answerName": "A1865",
                "priority": "0"
            },
            {
                "answerId": "2242",
                "answerName": "A1903",
                "priority": "0"
            }
        ],
        "questionId": "918",
        "questionName": "型号"
    }
]

# product_check_item  57项检测标准——检测标准化产品信息http://wiki.huishoubao.com/web/#/105?page_id=3295


def get_checks(options):
    strCheckList = []
    strCheckDesc = ''
    for info in options:
        answerList = info['answerList']
        '''第一种方式：在answerList下随机取1个'''
        # index = random.randint(0, len(answerList) - 1)
        # strCheckList.append(answerList[index]['answerId'])
        # strCheckDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'

        '''第二种方式：在answerList下取answerWeight最大的那个'''
        index = sorted(answerList, key=lambda x: int(x['answerWeight']), reverse=True)[0]
        strCheckList.append(index["answerId"])
        strCheckDesc += '"' + info['questionName'] + ":" + index['answerName'] + '",'
    print("机况选项{}".format(json.dumps(strCheckList)))
    print("机况描述{}".format(strCheckDesc))


def get_skus(options):
    strSkuList = []
    strSkuDesc = ''
    for info in options:
        answerList = info['answerList']
        index = 0
        # index = random.randint(0, len(answerList) - 1)
        strSkuList.append(answerList[index]['answerId'])
        strSkuDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'
    print("==sku==={}\n{}\n\n==sku描述===".format(json.dumps(strSkuList), strSkuDesc))


# 34项标准检   41567
get_checks(checkList_34)
get_skus(skuList_34)