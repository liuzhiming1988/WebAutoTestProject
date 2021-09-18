#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 26.检测标准选项在统一估价和所有子平台下估价接口 - http://wiki.huishoubao.com/index.php?s=/105&page_id=5562
    入参：productId：估价产品ID	17等	是  |  userId：登录用户，用户可为空  |  skuList：标准检测sku选项  |  optionList：标砖检测机况选项
        evaluateFlag：去估价标记	不传或传1则去估价 传入0不估价 只转换选项  |  platformList：平台信息  |  channelList：渠道列表

    1-对应服务：server-evaluate_detect（服务器应用名：server-evaluate_detect）  |  2-对应URL http://codserver.huishoubao.com
'''

import hashlib, requests, json, os
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def get_standard_option_all_evaluate(optionList, skuList, platformList, productId):
    param = {"_head":{"_callerServiceId":"212011","_groupNo":"1","_interface":"get_standard_option_all_evaluate","_invokeId":"20201014","_msgType":"request","_remark":"","_timestamps":"1602667953","_version":"0.01"},"_param":{"cookies":"20201014","interface":"get_standard_option_all_evaluate","ip":"127.0.0.1","optionList":optionList, "productId":productId,"server":"eva_detect","skuList":skuList, "platformList":platformList, "url":"/detect/get_standard_option_all_evaluate","userId":"test_zhangjinfa@huishoubao.com.cn"}}

    secret_key = "74175426afa280184b62591b58c671b3"
    callerserviceid = "212011"
    url = "http://codserver.huishoubao.com/detect/get_standard_option_all_evaluate"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    # get_standard_option_all_evaluate(optionList=[], skuList=[], platformList={"0":"统一估价","1":"2C","2":"2B","10":"B端帮卖平台"}, productId="41567")
    # get_standard_option_all_evaluate(optionList=[], skuList=["14","471","17","2236","38","1091","1773"], platformList={"0":"统一估价","1":"2C","2":"2B","10":"B端帮卖平台"}, productId="41567")
    # get_standard_option_all_evaluate(optionList=["7420","7423","7425","7430","7432","7438"], skuList=["14","471","17","2236","38","1091","1773"], platformList={"0":"统一估价","1":"2C","2":"2B","10":"B端帮卖平台"}, productId="41567")
    # get_standard_option_all_evaluate(optionList=["7419","7423","7426","7428","7432","7437","7443","7445","7450","7452","7460","7463","7466","7467","7470","7473","7483","7489","7490","7495","7503","7507","7513","7519","7523","7530","7532","7536","7542","7548","7555","7557","7560","7565","7571","7575","7578","7581","7587","7591","7599","7614"], skuList=["6047","471","18","2236"], platformList={"0":"统一估价","1":"2C","2":"2B","10":"B端帮卖平台"}, productId="41567")
    # get_standard_option_all_evaluate(optionList=["7420","7422","7426","7429","7434","7440","7442","7447","7449","7452","7461","7463","7465","7469","7472","7474","7483","7487","7492","7496","7501","7508","7515","7519","7523","7530","7534","7536","7544","7548","7553","7557","7559","7563","7572","7575","7579","7581","7586","7591","7610","7614"], skuList=["13","471","17","2236","36","1091","2241"], platformList={}, productId="41567")
    # get_standard_option_all_evaluate(optionList=["7420","7422","7426","7429","7434","7440","7442","7447","7449","7452","7461","7463","7465","7469","7472","7474","7483","7487","7492","7496","7501","7508","7515","7519","7523","7530","7534","7536","7544","7548","7553","7557","7559","7563","7572","7575","7579","7581","7586","7591","7610","7614"], skuList=["13","471","17","2236","36","1091","2241"], platformList={"0":"统一估价","1":"2C","2":"2B","10":"B端帮卖平台"}, productId="")
    # get_standard_option_all_evaluate(optionList=["7418","7422","7425","7428","7432","7436","7442","7445","7449","7452","7460","7462","7464","7467","7470","7473","7481","7487","7490","7493","7499","7506","7510","7517","7522","7528","7532","7536","7541","7547","7553","7556","7559","7562","7570","7574","7578","7580","7586","7589","7599","7613"], skuList=["12","18","36","1091","130","2241","2236"], platformList={"0":"统一估价","1":"2C","2":"2B","10":"B端帮卖平台"}, productId="41567")

    # get_standard_option_all_evaluate(optionList=[], skuList=["12","18","36","1091","130","2241","2236"], platformList={"0":"统一估价","1":"2C"}, productId="41567")

    # get_standard_option_all_evaluate(optionList=[], skuList=["12","18","36","1091","130","2241","2236"], platformList={"0":"统一估价"}, productId="41567")

    ''' 2021年5月27日 对接口list进行严格校验'''
    # get_standard_option_all_evaluate(optionList=[], skuList=[], platformList={"0":"统一估价","1":"2C","2":"2B","10":"B端帮卖平台"}, productId="41567") # 正常返回

    # "_errStr":"skuList 参数格式错误"
    # get_standard_option_all_evaluate(optionList=[""], skuList=[""], platformList={"0":"统一估价","1":"2C","2":"2B","10":"B端帮卖平台"}, productId="41567")

    # 正常
    # get_standard_option_all_evaluate(optionList=[], skuList=["12","18","36","1091","130","2241","2236"], platformList={"0":"统一估价","1":"2C","2":"2B","10":"B端帮卖平台"}, productId="41567")

    # "_errStr":"optionList 参数格式错误"
    # get_standard_option_all_evaluate(optionList=[""], skuList=["12","18","36","1091","130","2241","2236"], platformList={"0":"统一估价","1":"2C","2":"2B","10":"B端帮卖平台"}, productId="41567")

    # "_errStr":"optionList 参数格式错误"
    # get_standard_option_all_evaluate(optionList=["abc"], skuList=["12","18","36","1091","130","2241","2236"], platformList={"0":"统一估价","1":"2C","2":"2B","10":"B端帮卖平台"}, productId="41567")

    # 正常
    get_standard_option_all_evaluate(optionList=["7418","7422","7425","7428","7432","7436","7442","7445","7449"], skuList=["12","18","36","1091","130","2241","2236"], platformList={"0":"统一估价","1":"2C","2":"2B","10":"B端帮卖平台"}, productId="41567")

