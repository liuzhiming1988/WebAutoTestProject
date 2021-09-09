#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 定价系统+商品库系统+调价系统+估价系统 - 定价服务 - 获取定价价格 - http://wiki.huishoubao.com/web/#/347?page_id=11998

    入参：productId：产品Id（必填） |  select：选项id（必填）  |  userId：用户Id或是名称（必填）  |  ip：ip（必填）
        evaType：质检类型，1-标准质检，2-大质检，3-34项标准检（必填）
    出参：quotation：估出的定价价格 ,单位分  |  standPrice：初始化价格，基准价，单位分  |  recordId：估价记录id  |  levelId：等级ID

    BasePriceServerProxy
    解释：BasePriceServer是接口是thrift 我们目前使用的是Binary二进制编码格式进行数据传输，所以正常http协议的请求识别不了，
    解释：所以在BasePriceServer加了层代理 BasePriceServerProxy层，你可以认为BasePriceServerProxy接收http协议，然后转成Binary和BasePriceServer进行通讯
'''

import requests, json, time, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_baseprice_ipProxy_test, hsb_eva_ipProxy_test, hsb_response_print

class Evaluate_Base_Price:
    def product_check_item_34(self, productId):
        param = {"_head": {"_interface": "product_check_item_34", "_msgType": "request", "_remark": "", "_version": "0.01","_timestamps": int(time.time()), "_invokeId": "test_zhangjinfa", "_callerServiceId": "112006", "_groupNo": "1"},"_param": {"productId": productId}}

        secret_key = "gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU"
        callerserviceid = "112006"
        url = "http://codserver.huishoubao.com/detect/product_check_item"
        md5value = json.dumps(param) + "_" + secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID": callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典
        # print(respone.text)
        checkList = respone_dict['_data']['_data']['checkList']
        skuList = respone_dict['_data']['_data']['skuList']

        strCheckList = []
        strCheckDesc = ''
        for info in checkList:
            answerList = info['answerList']
            index = random.randint(0, len(answerList) - 1)
            strCheckList.append(answerList[index]['answerId'])
            strCheckDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'

        strSkuList = []
        strSkuDesc = ''
        for info in skuList:
            answerList = info['answerList']
            index = random.randint(0, len(answerList) - 1)
            strSkuList.append(answerList[index]['answerId'])
            strSkuDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'

        select = strSkuList + strCheckList
        select_desc = strSkuDesc + strCheckDesc

        return select, select_desc

    def evaluate_base_price(self, evaType, productId):
        # (select, select_desc) = self.product_check_item_34(productId=productId)
        # 1. "quotation":"292500"
        select = ['12', '471', '18', '2236', '38', '1091', '2242',     '9016', '9019', '9027', '9029', '9037', '9039', '9052', '9056', '9057', '9059', '9062', '9070', '9072', '9074', '7559', '9078', '9079', '9081', '7575', '9082', '9086', '9088', '9090', '9095', '9099', '9104', '9106', '9113', '9117', '7532']
        param = {"_head":{"_interface":"evaluate_base_price","_msgType":"request","_remark":"","_version":"0.01","_timestamps":str(int(time.time())),"_invokeId":"111","_callerServiceId":"216008","_groupNo":"1"},"_param":{"evaType":evaType, "ip":"127.0.0.1", "productId":productId, "select":select, "userId":"0"}}
        secret_key = "f5dca47cdabddec161b3150107b96a87"
        callerserviceid = "216008"
        url = "http://basepriceserver.huishoubao.com/BPP/EvaluateBasePrice"
        md5value = json.dumps(param) + "_" + secret_key
        headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value), "HSB-OPENAPI-CALLERSERVICEID": callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_baseprice_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置

        print('========>1.『{0}』 产品的『检测标准化选项-34』(随机取)为：\n'.format(productId), select)
        # print('\n========>2. 以上『检测标准化选项-34』为：\n', '{' + select_desc[:-1] + '}')
        hsb_response_print(respone=respone)

''' 请求方：server-evaluate_detect、server-bangmai_pro_eva    响应方：BasePriceServerProxy、BasePriceServer'''
if __name__ == '__main__':
    baseprice_15 = Evaluate_Base_Price()
    baseprice_15.evaluate_base_price(evaType='3', productId='41567')

'''
【内部接口】获取定价价格

【BasePriceServerProxy】   【逻辑层】【BasePriceServer】
paramsCheck() Start ...
db.t_base_price_product.findOne({"Fproduct_id":41567},{"Fprice_status":1,"Frecycle_status":1,"Fstatus":1});
db.t_answer_item.aggregate({ "0" : { "$match" : { "Fastatus" : 1, "Faid" : { "$in" : [ 12, 18, 38, 471, 1091, 2236, 2242, 7532, 7559, 7575, 9016, 9019, 9027, 9029, 9037, 9039, 9052, 9056, 9057, 9059, 9062, 9070, 9072, 9074, 9078, 9079, 9081, 9082, 9086, 9088, 9090, 9095, 9099, 9104, 9106, 9113, 9117 ] } } }, "1" : { "$lookup" : { "from" : "t_question_item", "localField" : "Fqid", "foreignField" : "Fqid", "as" : "tmp_docs" } }, "2" : { "$match" : { "tmp_docs.Fqstatus" : 1 } }, "3" : { "$project" : { "tmp_docs.Fqid" : 1, "tmp_docs.Fqname" : 1, "tmp_docs.Fqtype" : 1, "Faid" : 1, "Faname" : 1 } } });

getProductParams() Start ...
db.t_item_params_config.findOne({"Fproduct_id":41567},{"Fbase_price":1,"Fcombination_price_info":1,"Flevel_params_info":1,"Flevel_temp_id":1,"Fsku_params_info":1,"Fversion_id":1});

formatProParams() Start ...
Sku Sub Type:2 绝对值
setItemAid:12#18#38#471#1091#2236#2242#7532#7559#7575#9016#9019#9027#9029#9037#9039#9052#9056#9057#9059#9062#9070#9072#9074#9078#9079#9081#9082#9086#9088#9090#9095#9099#9104#9106#9113#9117
Sku Item:[12,18,38,471,1091,2236,2242]
Opt Item:[7532,7559,7575,9016,9019,9027,9029,9037,9039,9052,9056,9057,9059,9062,9070,9072,9074,9078,9079,9081,9082,9086,9088,9090,9095,9099,9104,9106,9113,9117]

getProTempInfo() Start ...
db.t_level_template_info.findOne({"Flevel_temp_id":15},{"Fcheck_item_34":1})

formatProTempInfo() Start ...

levelMatching() Start ...
Hit Level:600 Item:9027
Level Matching:600 OptItem:[7532,7559,7575,9016,9019,9027,9029,9037,9039,9052,9056,9057,9059,9062,9070,9072,9074,9078,9079,9081,9082,9086,9088,9090,9095,9099,9104,9106,9113,9117]
priceCombMatching() Start ...
Price Comb Matching Fail: lv:600 Suk:12#18#38#471#1091#2236#2242

priceByFactor() Start ...
BasePric:161600
sku:12 value:1 FactorPrice = 161601
sku:18 value:0 FactorPrice = 161601
sku:38 value:53419 FactorPrice = 215020
sku:471 value:-1767 FactorPrice = 213253
sku:1091 value:1 FactorPrice = 213254
sku:2236 value:0 FactorPrice = 213254
sku:2242 value:-5753 FactorPrice = 207501
level:600 value:1410 FactorPrice = 292576
Quatation = 292576
Remove Score:292500

addEvaluateRecode() Start ...
db.counters.find_one_and_update({ "_id" : "eva_record_2105" },{ "$inc" : { "sequence_value" : 1 } },{filter:{ "sequence_value" : 1 }, return:1, upsert:1})
 db.t_eva_record_2105.insertOne({"Fbase_price":161600,"Fcreate_time":{"$date":1621700105773},"Ferror_code":0,"Ferror_info":"success","Feva_type":3,"Fevaluate_id":85715,"Flevel_temp_id":15,"Fopt_item":[7532,7559,7575,9016,9019,9027,9029,9037,9039,9052,9056,9057,9059,9062,9070,9072,9074,9078,9079,9081,9082,9086,9088,9090,9095,9099,9104,9106,9113,9117],"Fopt_level_id":600,"Fproduct_id":41567,"Fquatation":292500,"Fsbu_type":2,"Fselect":[12,471,18,2236,38,1091,2242,9016,9019,9027,9029,9037,9039,9052,9056,9057,9059,9062,9070,9072,9074,7559,9078,9079,9081,7575,9082,9086,9088,9090,9095,9099,9104,9106,9113,9117,7532],"Fsku_item":[12,18,38,471,1091,2236,2242],"Fspend_time":3,"Fversion_id":196})
'''