#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 46.检测商品库sku信息加大质检机况估价接口 - http://wiki.huishoubao.com/index.php?s=/105&page_id=8007
    1. 对应服务：server-evaluate_detect（服务器应用名：server-evaluate_detect）
    2. 对应URL http://codserver.huishoubao.com

    入参：orderId：是，订单id | productId：是，修改产品后的产品id 优先使用这个 未传递则使用DB中的
        skuList：是，商品库sku答案选项 | optionList：是，大质检答案选项 | userId：是，检测工程师id
        isOverInsurance：否，是否强制过保 0:否 1:强制过保,默认为0   ------  20201020新增
    出参：select：是，转换出来的估价选项； | selectName：是，转化后的选项的选项描述； | checkPrice：是，检测价格,单位为分 | evaluateId：是，估价Id;
        insured：是，保价标记，1-保价 0-不保价; | orderId：是，订单Id; | productId：是，产品Id | transformList：是，转换出来的估价选项详细信息

    此脚本【依赖】产品服务 - 45.检测获取产品商品库sku信息和大质检机况信息  - http://wiki.huishoubao.com/index.php?s=/105&page_id=7967
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test, hsb_response_print

class Product_Lib_And_Option_To_Evaluate:
    def __init__(self):
        self.secret_key = "gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU"
        self.callerserviceid = "112006"

    def get_product_lib_sku_option_item(self, productId, orderId, isOverInsurance):
        param = {"_head": {"_interface": "get_product_lib_sku_option_item", "_msgType": "request", "_remark": "","_version": "0.01", "_timestamps": "123456", "_invokeId": "123456","_callerServiceId": "112006", "_groupNo": "1"},"_param": {"productId": productId, "orderId": orderId, "isOverInsurance":isOverInsurance}}
        url = "http://codserver.huishoubao.com/detect/get_product_lib_sku_option_item"
        md5value = json.dumps(param) + "_" + self.secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID": self.callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典
        skuList = respone_dict['_data']['_data']['skuList']
        optionList = respone_dict['_data']['_data']['optionList']

        strSkuList = []
        for info_sku in skuList:
            answerList_sku = info_sku['answerList']
            index_sku = random.randint(0, len(answerList_sku) - 1)
            strSkuList.append(answerList_sku[index_sku]['answerId'])

        strOptionList = []
        for info_option in optionList:
            answerList_option = info_option['answerList']
            index_option = random.randint(0, len(answerList_option) - 1)
            strOptionList.append(answerList_option[index_option]['answerId'])

        return strSkuList, strOptionList

    def product_lib_and_option_to_evaluate(self, orderId, productId, isOverInsurance):
        skuList = ['6047', '471', '18', '2236', '38', '42', '1773']
        optionList = ['6931', '56', '58', '63', '236', '73', '3242', '7642', '65', '82', '5534', '224', '1077', '3245', '2171', '23', '20']
        # (skuList, optionList) = self.get_product_lib_sku_option_item(productId=productId, orderId=orderId, isOverInsurance=isOverInsurance)
        param = {"_head": {"_interface": "product_lib_and_option_to_evaluate", "_msgType": "request", "_remark": "","_version": "0.01", "_timestamps": "123456", "_invokeId": "123456", "_callerServiceId": "112006", "_groupNo": "1"},"_param": {"orderId": orderId, "productId": productId, "skuList": skuList, "optionList": optionList, "isOverInsurance":isOverInsurance,"userId": "1311"}}
        url = "http://codserver.huishoubao.com/detect/product_lib_and_option_to_evaluate"
        md5value = json.dumps(param) + "_" + self.secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID": self.callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置

        print('==========>1. 订单ID：『{0}』，产品ID：『{1}』，『商品库sku答案项』(随机取)为：\n'.format(orderId, productId), skuList)
        print('\n==========>2. 订单ID：『{0}』，产品ID：『{1}』，『大质检机况答案项』(随机取)为：\n'.format(orderId, productId), optionList)
        print()
        hsb_response_print(respone=respone)

if __name__ == '__main__':
    product_46 = Product_Lib_And_Option_To_Evaluate()
    ''' 第一次 "_errCode":"3004","_errStr":"转换估价sku错误,估价sku问题项 存储容量 没有匹配上任何答案项" '''
    # skuList = ['14', '471', '18', '2236', '38', '2202', '2269']
    # optionList = ['24', '55', '58', '62', '65', '68', '5530', '78', '82', '223', '1078', '20', '3245', '2171', '5534', '6930', '7642']
    # product_46.product_lib_and_option_to_evaluate(productId='64000', orderId='7598633', isOverInsurance='0') # 华为 P40 | Forder_time=2020-10-23 10:57:48

    ''' 【非正常场景】 第二次 （不重新获取选项）单单 product_lib_and_option_to_evaluate 传强制过保'''
    # product_46.product_lib_and_option_to_evaluate(productId='64000', orderId='7598633', isOverInsurance='1') # 华为 P40 | Forder_time=2020-10-23 10:57:48

    ''' 【正常场景】 第二次，get_product_lib_sku_option_item 和 product_lib_and_option_to_evaluate 均重新调用，均传’强制过保‘参数 '''
    # "insured":"1","isItemConsistent":"0","isItemTemplateConsistent":"1"
    # "evaluateType":"1","evaluateid":"20107598","evaversion":"","quotation":"6400"
    # product_46.product_lib_and_option_to_evaluate(productId='64000', orderId='7598633', isOverInsurance='1') # 华为 P40 | Forder_time=2020-10-23 10:57:48
    # product_46.product_lib_and_option_to_evaluate(productId='63233', orderId='7605481', isOverInsurance='0') #


    # product_46.product_lib_and_option_to_evaluate(productId='41567', orderId='7632330', isOverInsurance='1') #
    # product_46.product_lib_and_option_to_evaluate(productId='41567', orderId='7632330', isOverInsurance='0') #
    # product_46.product_lib_and_option_to_evaluate(productId='63330', orderId='7632330', isOverInsurance='0') #
    # product_46.product_lib_and_option_to_evaluate(productId='63330', orderId='7632330', isOverInsurance='1') #

    ''' 2021年5月27日 对接口list进行严格校验'''
    # "_errStr":"转换估价sku错误,估价sku问题项 购买渠道 没有匹配上任何答案项"
    # product_46.product_lib_and_option_to_evaluate(productId='41567', orderId='7633197', isOverInsurance='0') # skuList = []  optionList = []

    # "_errStr":"skuList 参数格式错误"
    # product_46.product_lib_and_option_to_evaluate(productId='41567', orderId='7633197', isOverInsurance='0') # skuList = [""]  optionList = [""]

    # "_errStr":"optionList 参数格式错误"
    # product_46.product_lib_and_option_to_evaluate(productId='41567', orderId='7633197', isOverInsurance='0') # skuList = []  optionList = [""]

    # "_errStr":"skuList 参数格式错误"
    # product_46.product_lib_and_option_to_evaluate(productId='41567', orderId='7633197', isOverInsurance='0') # skuList = ["abc"]  optionList = ["abc"]

    # skuList = ['6047', '471', '18', '2236', '38', '42', '1773']   optionList = []   |  "_errStr":"保价价格计算失败"
    # product_46.product_lib_and_option_to_evaluate(productId='41567', orderId='7633197', isOverInsurance='0')

    # skuList = ['6047', '471', '18', '2236', '38', '42']  sku少一个  optionList = []
    # "_errStr":"转换估价sku错误,估价sku问题项 型号 没有匹配上任何答案项"
    # product_46.product_lib_and_option_to_evaluate(productId='41567', orderId='7633197', isOverInsurance='0')

    # skuList = ['6047', '471', '18', '2236', '38', '42', '1773']
    # optionList = ['6931', '56', '58', '63', '236', '73', '3242', '7642', '65', '82', '5534', '224', '1077', '3245', '2171', '23', '20']  |  正常
    product_46.product_lib_and_option_to_evaluate(productId='41567', orderId='7633197', isOverInsurance='0')

''' 【注意场景】第一次，检测人员选错了（安卓机，内存+机身存储，选择的组合是不存在的），返回3004，第二次请求，强制过保。（不是因为sku选项变更而让强制过保，返回的却是强制过保后的价格）
第二次，检测人员选错了（安卓机，内存+机身存储，选择的组合是不存在的），返回3004，再次请求，强制过保'''

'''
问题项（选项）（questionId）- 答案项（answerId），一个问题项 -> 有一个答案项（不能没有）
POST_DATA = {"_head": {"_interface": "get_product_lib_sku_option_item", "_msgType": "request", "_remark": "", "_version": "0.01", "_timestamps": "123456", "_invokeId": "123456", "_callerServiceId": "112006", "_groupNo": "1"}, "_param": {"productId": "64000", "orderId": "7598633", "isOverInsurance": "1"}}

    curl -H 'HSB-OPENAPI-SIGNATURE:11b635c51a1e038c1bf101f99e7ab5c1' -H 'HSB-OPENAPI-CALLERSERVICEID:216008' -d '{"_head":{"_callerServiceId":"216008","_groupNo":"1","_interface":"pdt_sku_query","_invokeId":"a9bf836bd718b6a8337d50998160622c","_msgType":"request","_remark":"","_timestamps":"1603422685","_version":"0.01"},"_param":{"info":{"combination":"0","productId":"64000"},"subInterface":"sku_option_combination_get"}}' http://prdserver.huishoubao.com/rpc/new_product_lib

    curl -d '{"head":{"interface":"insured_options","msgtype":"request","remark":"","version":"0.01"},"params":{"isOverInsurance":"1","order_id":"7598633","productId":"64000","user_name":"server-evaluate_detect"}}' http://evaserver.huishoubao.com/rpc/insured

POST_DATA = {"_head": {"_interface": "product_lib_and_option_to_evaluate", "_msgType": "request", "_remark": "", "_version": "0.01", "_timestamps": "123456", "_invokeId": "123456", "_callerServiceId": "112006", "_groupNo": "1"}, "_param": {"orderId": "7598633", "productId": "64000", "skuList": ["12", "124", "2238", "38", "6869"], "optionList": ["63", "66", "59", "69", "2171", "55", "3245", "3244", "53", "3243", "7641", "6931", "24", "9", "21", "6702", "5535", "224"], "isOverInsurance": "1", "userId": "1311"}}

    curl -d '{"head":{"interface":"insured_options","msgtype":"request","remark":"","version":"0.01"},"params":{"isOverInsurance":"1","order_id":"7598633","productId":"64000","user_name":"server-evaluate_detect"}}' http://evaserver.huishoubao.com/rpc/insured

    curl -d '{"head":{"interface":"evaluateengineer","msgtype":"request","remark":"","version":"0.01"},"params":{"cookies":"server-evaluate_detect.BAQGKWRJ","ip":"127.0.0.1","isOverInsurance":"1","orderid":"7598633","productId":"64000","select":["1062","1340","124","12","63","66","59","69","2171","55","3245","3244","53","3243","7641","6931","24","9","21","6702","5535","224"],"userid":"1311"}}' http://evaserver.huishoubao.com/rpc/evaluate
        
            curl -d '{"head":{"interface":"insured_judge","msgtype":"request","remark":"","version":"0.01"},"params":{"checkItem":["1062","1340","124","12","63","65","58","236","2171","55","3246","3244","53","3242","7641","6930","23","9","20","6703","5534","224"],"order_id":"7598633","productId":"64000","user_name":"evaluate_server"}}
            
{"_data":{"_data":{"checkPrice":"6400","evaluateId":"20107638","insured":"0","orderId":"7598633","productId":"64000","select":["832","46","124","2492","61","66","58","71","2171","56","3246","5531","53","3243","7641","6930","24","8","21","6703","5534","224"],"selectName":["存储容量:6GB+128GB","颜色:亮黑色","制式:移动版","购买渠道:非大陆国行","维修:修主板/多次维修","通话:通话不正常","进水:机身进水/受潮","屏幕显示:显示完美，无瑕疵","屏幕更换:屏幕未更换/维修","WIFI:WIFI/蓝牙不正常","触屏功能:触摸屏正常","屏幕外观:屏幕明显划痕","指纹功能:指纹功能正常","机身外观:机身弯曲或断裂","小故障项:声音/麦克风/按键/充电/震动正常","拍照:拍照有斑","开机:不能正常开机","ID锁:ID/账户锁无法解除","成色:二手","面容识别:面容识别不正常","电池:电池更换/维修","拍照摄像:拍照摄像不正常"],"transformList":[{"ansId":"832","ansName":"6GB+128GB","confType":"1","queId":"32","queName":"存储容量"},{"ansId":"46","ansName":"亮黑色","confType":"1","queId":"39","queName":"颜色"},{"ansId":"124","ansName":"移动版","confType":"1","queId":"122","queName":"制式"},{"ansId":"2492","ansName":"非大陆国行","confType":"1","queId":"11","queName":"购买渠道"},{"ansId":"61","ansName":"修主板/多次维修","confType":"2","queId":"60","queName":"维修"},{"ansId":"66","ansName":"通话不正常","confType":"3","queId":"64","queName":"通话"},{"ansId":"58","ansName":"机身进水/受潮","confType":"3","queId":"57","queName":"进水"},{"ansId":"71","ansName":"显示完美，无瑕疵","confType":"2","queId":"67","queName":"屏幕显示"},{"ansId":"2171","ansName":"屏幕未更换/维修","confType":"3","queId":"2169","queName":"屏幕更换"},{"ansId":"56","ansName":"WIFI/蓝牙不正常","confType":"3","queId":"54","queName":"WIFI"},{"ansId":"3246","ansName":"触摸屏正常","confType":"3","queId":"1461","queName":"触屏功能"},{"ansId":"5531","ansName":"屏幕明显划痕","confType":"2","queId":"72","queName":"屏幕外观"},{"ansId":"53","ansName":"指纹功能正常","confType":"3","queId":"51","queName":"指纹功能"},{"ansId":"3243","ansName":"机身弯曲或断裂","confType":"2","queId":"76","queName":"机身外观"},{"ansId":"7641","ansName":"声音/麦克风/按键/充电/震动正常","confType":"3","queId":"7640","queName":"小故障项"},{"ansId":"6930","ansName":"拍照有斑","confType":"3","queId":"6929","queName":"拍照"},{"ansId":"24","ansName":"不能正常开机","confType":"3","queId":"22","queName":"开机"},{"ansId":"8","ansName":"ID/账户锁无法解除","confType":"2","queId":"7","queName":"ID锁"},{"ansId":"21","ansName":"二手","confType":"3","queId":"19","queName":"成色"},{"ansId":"6703","ansName":"面容识别不正常","confType":"3","queId":"6701","queName":"面容识别"},{"ansId":"5534","ansName":"电池更换/维修","confType":"3","queId":"5533","queName":"电池"},{"ansId":"224","ansName":"拍照摄像不正常","confType":"3","queId":"222","queName":"拍照摄像"}]},"_errCode":"0","_errStr":"success","_ret":"0"},"_head":{"_callerServiceId":"112006","_groupNo":"1","_interface":"product_lib_and_option_to_evaluate","_invokeId":"123456","_msgType":"response","_remark":"","_timestamps":"1603433921","_version":"0.01"}}

线上调用
curl -H 'HSB-OPENAPI-SIGNATURE:00a2af23cae30602d0da62787f42591b' -H 'HSB-OPENAPI-CALLERSERVICEID:112006' -d '{"_head": {"_interface": "product_lib_and_option_to_evaluate", "_msgType": "request", "_remark": "","_version": "0.01", "_timestamps": "123456", "_invokeId": "123456", "_callerServiceId": "112006", "_groupNo": "1"},"_param": {"orderId": "10192534", "productId": "23007", "skuList": [], "optionList": ["23"], "isOverInsurance":"0","userId": "1311"}}' http://codserver.huishoubao.com/detect/product_lib_and_option_to_evaluate
'''

