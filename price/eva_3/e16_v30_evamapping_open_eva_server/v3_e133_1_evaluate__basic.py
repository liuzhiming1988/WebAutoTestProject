#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 定价系统+商品库系统+调价系统+估价系统 - 获取产品列表（可估价）  - http://wiki.huishoubao.com/web/#/347?page_id=15706
    入参：cookies：用户浏览器使用的cookies，如果没有，给随机字符串，方便问题查找
        ip：用户公网访问IP  |  pid：回收宝对外入口ID  |  channel_id：渠道ID，10000031
        productid：产品Id  |  userid：登录用户ID  |  select：用户选择的估价选项
    出参：quotation：估出的定价价格，单位分  |  evaluateid：估价记录id，(id 会超过int(11)，请不要用int保存）
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def v3_evaluate(productid, pid, channel_id, select):
    param = {"_head":{"_interface":"evaluate","_msgType":"request","_remark":"zhangjinfa_autoTest","_version":"0.01","_timestamps":"123","_invokeId":"111","_callerServiceId":"816006","_groupNo":"1"},"_param":{"productid":productid, "ip":"127.0.0.1", "cookies":"zhangjinfa_autoTest", "userid":"1895", "select":select, "pid":pid,"channel_id":channel_id}}
    secret_key = "9aee61caf448b65fdf84c0e7d77c7348"
    callerserviceid = "816006"
    url = "http://evaserver.huishoubao.com/evaluate_price_v3/evaluate"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    respone.encoding = respone.apparent_encoding  # 编码设置
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    ''' 估价系统 与 定价系统 区分开理解，此处，不考虑机型的 定价状态'''
    # 1、渠道 和 PID 为空 | "_errStr":"请求参数错误 [ChannelId为必填字段]","_data":null,"_errCode":"70021100","_ret":"70021100"
    # v3_evaluate(channel_id='', pid='', productid='41567', select=['12','17','38','42','100053','100054'])

    # 2、只传渠道ID 或 只传PID
    # "_errStr":"请求参数错误 [Pid为必填字段]","_data":null,"_errCode":"70021100","_ret":"70021100"
    # v3_evaluate(channel_id='40000001', pid='', productid='41567', select=['12','17','38','42','100053','100054'])

    # "_errStr":"请求参数错误 [ChannelId为必填字段]","_data":null,"_errCode":"70021100","_ret":"70021100"
    # v3_evaluate(channel_id='', pid='1001', productid='41567', select=['12','17','38','42','100053','100054'])

    # 3、productid为空 | "_errStr":"请求参数错误 [ProductId为必填字段]","_data":null,"_errCode":"70021100","_ret":"70021100"
    # v3_evaluate(channel_id='40000001', pid='1001', productid='', select=['12','17','38','42','100053','100054'])

    # 4、productid为 “不支持估价” 状态机型  |  "_errStr":"未定价或不支持估价状态机型","_data":null,"_errCode":"907","_ret":"907"
    # v3_evaluate(channel_id='40000001', pid='1001', productid='1010', select=['12', '17', '38', '42', '100053', '100054'])

    # 5、productid为 “禁用” 状态机型  |  "_errStr":"产品为下架状态","_data":null,"_errCode":"903","_ret":"903"
    # v3_evaluate(channel_id='40000001', pid='1001', productid='1037', select=['12', '17', '38', '42', '100053', '100054'])

    # 6、启用、支持估价状态机型，但是 “回收未定价” 状态机型（有回收定价版本） |  "_errStr":"未定价状态机型","_data":null,"_errCode":"907","_ret":"907"
    # v3_evaluate(channel_id='40000001', pid='1001', productid='54791', select=['12', '17', '38', '40', '5410', '100049'])

    # 7、启用、支持估价状态机型，但是 “回收未定价” 状态机型（无回收定价版本） |  "_errStr":"未定价状态机型","_data":null,"_errCode":"907","_ret":"907"
    # v3_evaluate(channel_id='40000001', pid='1001', productid='65783', select=['12', '37', '1282', '130', '2238', '100049'])

    # 8、启用、支持估价状态、有回收定价版本 机型 | 无SKU机型  |  正常
    # v3_evaluate(channel_id='40000001', pid='1001', productid='1', select=['100049'])

    ''' SPU名称：iPhone X | SPU ID：41567 | 估价模板名称：65-测试3个接口-勿动12 (ID：65)  | 使用的估价子模板：65第1个子模板 (ID:91) | 估价等级模板名称： 54-等级模板-测试3个接口(ID：54) '''
    # 9、启用、支持估价状态、有回收定价版本 机型 | 用户侧不展示的估价SKU问题项，也传了，传的就是默认答案项
    # 用户侧不展示的估价SKU问题项 还是会使用默认项 去估价  |  正常（可以不考虑这种场景的验证，调用方拿不到这些用户侧不展示的选项）
    # v3_evaluate(channel_id='40000001', pid='1001', productid='41567', select=['12', '17', '38', '42', '130', '1083', '2236', '100049'])

    # 10、启用、支持估价状态、有回收定价版本 机型 | 用户侧不展示的估价SKU问题项，也传了，传的部分是默认答案项，部分不是默认答案项
    # 用户侧不展示的估价SKU问题项 还是会使用默认项 去估价  |  正常（可以不考虑这种场景的验证，调用方拿不到这些用户侧不展示的选项）
    # v3_evaluate(channel_id='40000001', pid='1001', productid='41567', select=['12', '17', '38', '42', '471', '2241', '2236', '100049'])

    # 11、启用、支持估价状态、有回收定价版本 机型 | 用户侧不展示的估价SKU问题项，也传了，传的部分是默认答案项，部分不是默认答案项
    # 用户侧不展示的估价SKU问题项 还是会使用默认项 去估价  |  正常（可以不考虑这种场景的验证，调用方拿不到这些用户侧不展示的选项）
    # v3_evaluate(channel_id='40000001', pid='1001', productid='41567', select=['12', '17', '38', '42', '471', '2241', '2236', '100049'])

    # 12、启用、支持估价状态、有回收定价版本 机型 | 不传或少传SKU | "_errStr":"SKU个数错误: U[3] P[7]","_data":null,"_errCode":"901","_ret":"901"
    # v3_evaluate(channel_id='40000001', pid='1001', productid='41567', select=['100049']) #不传SKU（概念不包括 用户侧不展示的估价SKU，会自动拿）
    # v3_evaluate(channel_id='40000001', pid='1001', productid='41567', select=['12', '17', '38', '100049']) #少传SKU（概念不包括 用户侧不展示的估价SKU，会自动拿）

    # 13、启用、支持估价状态、有回收定价版本 机型 | 一个SKU问题项，传多个答案项 | "_errStr":"SKU个数错误: U[8] P[7]","_data":null,"_errCode":"901","_ret":"901"
    # v3_evaluate(channel_id='40000001', pid='1001', productid='41567', select=['12', '13', '17', '38', '42', '100049']) # '12','13' 属于同一个问题项

    # 14、启用、支持估价状态、有回收定价版本 机型 | 传了机型没有配置的某个答案项 | "_errStr":"SKU个数错误: U[6] P[7]","_data":null,"_errCode":"901","_ret":"901"
    # v3_evaluate(channel_id='40000001', pid='1001', productid='41567', select=['12', '17', '38', '6869', '100049']) #'6869' 零度白 这个机型没有（当少传处理）

    ''' SKU-多传：①是这个机型的SKU，同个问题项传多个答案项，不行； ②是这个机型的SKU，属于用户侧不展示的sku项，传或多传，不影响； ③不是这个机型的SKU，传了或者多传都没影响'''
    # v3_evaluate(channel_id='40000001', pid='1001', productid='41567', select=['12', '17', '38', '42', '6869', '100049']) #'6869' 零度白 不是这个机型的
    # v3_evaluate(channel_id='40000001', pid='1001', productid='41567', select=['12', '17', '38', '42', '471', '100049']) #不会走471，还是会走默认的130
    # v3_evaluate(channel_id='40000001', pid='1001', productid='41567', select=['12', '17', '38', '42', '130', '471', '100049']) #130和471同传不影响，用默认的130

    # 15、启用、支持估价状态、有回收定价版本 机型 | 估价SKU答案项 与 标准SKU答案项，一对多 | 正常
    # v3_evaluate(channel_id='40000001', pid='1001', productid='41567', select=['7630', '17', '38', '42', '100049']) #7630映射7630、8012，默认是8012，使用默认

    # 16、启用、支持估价状态、有回收定价版本 机型 | 机型存在聚合型的SKU问题项和答案项 | 正常
    # v3_evaluate(channel_id='40000001', pid='1001', productid='64000', select=['12', '6869', '1062', '100049'])  #1062映射38+2238

    '''机况'''
    # 17、启用、支持估价状态、有回收定价版本 机型 | 不传机况 | "_errStr":"机况选项未匹配到选项等级组合","_data":null,"_errCode":"905","_ret":"905"
    # v3_evaluate(channel_id='40000001', pid='1001', productid='41567', select=['12', '17', '38', '42'])

    # 18、启用、支持估价状态、有回收定价版本 机型 | 传了这个机型不存在的机况 | 正常
    # v3_evaluate(channel_id='40000001', pid='1001', productid='41567', select=['12', '17', '38', '42', '100049', '20210805001'])

    # 19、启用、支持估价状态、有回收定价版本 机型 | 支持多选属性的机况场景 | 走正常 机况选项匹配选项等级组合 流程
    # v3_evaluate(channel_id='40000001', pid='1001', productid='41567', select=['12', '17', '38', '42', '100057', '100058'])

    # 20、启用、支持估价状态、有回收定价版本 机型 | 传的机况同时命中多个等级 | 正常（由差往好匹配，优先命中 100064）
    # v3_evaluate(channel_id='40000001', pid='1001', productid='41567', select=['12', '17', '38', '42', '100056', '100064'])

    # 21、启用、支持估价状态、有回收定价版本 机型 | 传的是PID-关联等级模板中，不存在的机况选项 | "_errStr":"机况选项未匹配到选项等级组合","_data":null,"_errCode":"905","_ret":"905"
    # v3_evaluate(channel_id='40000001', pid='1001', productid='41567', select=['12', '17', '38', '42', '100057'])

    # 22、启用、支持估价状态、有回收定价版本 机型 | 机况匹配到的选项等级，对应的定价等级系数为 0 | 正常 | "quotation":"0","evaluateid":"8210872"
    # v3_evaluate(channel_id='40000001', pid='1001', productid='41567', select=['12', '17', '38', '42', '100049'])

    # 24、启用、支持估价状态、有回收定价版本 机型 | 渠道调价，命中规则（按比例，触发 -101%） | 正常 | "quotation":"0","evaluateid":"8210873"
    v3_evaluate(channel_id='40000001', pid='1001', productid='41567', select=['12', '17', '38', '42', '100049'])

'''
【EvaluatePrice】 【价格3.0】 【回收定价】
匹配价格等级模板
匹配渠道 回收调价方案
计算定价价格（匹配穷举、按系数计算定价价格） 等级一对一（一次），等级一对多（多次）
计算渠道调价加成价格
    一次加成：
        等级一对一（一次）
        等级一对多（多次）
    二次加成：
        等级一对一（一次加成：一次，二次加成：一次）
        等级一对多（一次加成：多次，二次加成：多次）
根据调价等级及渠道调价加成价格，再根据等级权重系数，计算估价价格
    等级一对一
        渠道加成价格 * 等级权重系数）
    等级一对多
        渠道加成价格1 * 等级1权重系数
        渠道加成价格2 * 等级2权重系数
        渠道加成价格3 * 等级3权重系数
        ......
        相加即为：估价价格
'''