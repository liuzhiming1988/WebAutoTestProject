#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 41.1.标准检测选项获取商品评估价和保底价 - http://wiki.huishoubao.com/index.php?s=/105&page_id=7271
    1. 对应服务：server-evaluate_detect（服务器应用名：server-evaluate_detect） |  2. 对应URL http://codserver.huishoubao.com

    入参：productId：必填，产品id | skuList：必填，sku答案选项 | checkList：必填，检测答案选项
        channelId：非必填，渠道id，不传时，获取固定的“定价专用平台（10000192）”的价格即评估价，可以不传，但不能传空
        isBottom：是否取保底价，1获取保底价，0不取保底价， 默认为1
    出参：mapOptionList：转换出来的机况选项 | mapSkuList：转化后的sku选项
        evaluatePrice：商品评估价 | bottomPrice：保底价 | evaluateId：估价Id

    注意：channelId，不传，获取的是固定的 “定价专用平台” 的价格； |  channelId 传值，则获取对应渠道的价格
'''

import hashlib, requests,json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test, hsb_response_print


class  Get_Product_Sale_Evaluate_Price:
    def __init__(self):
        self.secret_key = "gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU"
        self.callerserviceid = "112006"

    def product_check_item_34(self, productId):
        param = {"_head": { "_interface":"product_check_item_34", "_msgType":"request", "_remark":"product_check_item_34", "_version":"0.01", "_timestamps":"123456", "_invokeId":"123456", "_callerServiceId":"112006", "_groupNo":"1" },"_param": {"productId":productId, "orderId":"" }}
        url = "http://codserver.huishoubao.com/detect/product_check_item"
        md5value = json.dumps(param) + "_" + self.secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":self.callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典
        checkList = respone_dict['_data']['_data']['checkList']
        skuList = respone_dict['_data']['_data']['skuList']

        strCheckList = []
        strCheckDesc = ''
        for info in checkList:
            answerList = info['answerList']
            index = random.randint(0, len(answerList) - 1)
            strCheckList.append(answerList[index]['answerId'])
            # 以下只为打印输出随机取的检测标准化机况选项数据
            strCheckDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'

        strSkuList = []
        strSkuDesc = ''
        for info in skuList:
            answerList = info['answerList']
            index = random.randint(0, len(answerList) - 1)
            strSkuList.append(answerList[index]['answerId'])
            # 以下只为打印输出随机取的检测标准化SKU选项数据
            strSkuDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'

        # print('接口响应『json』格式数据为：\n', json.dumps(respone_dict, ensure_ascii=False),'\n')
        print('==========1. 检测【sku】答案项ID传参数据为（随机取）：\n',strSkuList)
        print()
        print('==========2. 检测【机况】答案项ID传参数据为（随机取）：\n',strCheckList)
        print()
        print('==========3. 以上【sku】+以上【机况】选项名称+答案项名称：\n', '{' + strSkuDesc + strCheckDesc[:-1] + '}' + '\n')
        return strSkuList, strCheckList

    def get_product_sale_evaluate_price(self, productId, channelId):
        (skuList, checkList) = self.product_check_item_34(productId=productId)
        # skuList = ['12', '130', '17', '2236', '38', '1091', '1773']
        # checkList = ['7418', '7423', '7426', '7428', '7434', '7438', '7442', '7445', '7450', '7453', '7461', '7462', '7464', '7469', '7472', '7474', '7483', '7487', '7490', '7496', '7499', '7508', '7515', '7518', '7523', '7615', '7534', '7536', '7544', '7547', '7554', '7557', '7561', '7563', '7570', '7575', '7578', '7580', '7586', '7590', '7610', '7613']
        param = {"_head":{"_interface":"get_product_sale_evaluate_price","_msgType":"request","_remark":"hello","_version":"0.01","_timestamps":"123","_invokeId":"111","_callerServiceId":"112006","_groupNo":"1"},"_param":{"productId":productId, "skuList":skuList, "checkList":checkList, "channelId":channelId, "isBottom":"0" }}
        url = "http://codserver.huishoubao.com/detect/get_product_sale_evaluate_price"
        md5value = json.dumps(param) + "_" + self.secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":self.callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        hsb_response_print(respone=respone)


if __name__ == '__main__':
    ''' 迅捷业务估价接口支持 
    https://www.tapd.cn/21967291/prong/stories/view/1121967291001062339?url_cache_key=a29d90ce8da4cfad5587a1fc3e207d95&action_entry_type=story_tree_list
    1. 店员帮用户估价：
        使用34项估价，先走3.0销售价接口拿销售参考价（业务侧自行配置利润空间，展示回收价给用户）；
        如没有拿到销售参考价，则使用34项，走价格2.0系统拿回收价；（价格侧提供接口支持）。
    2. 下单后店员检测
        先使用57项，走3.0销售价接口拿销售参考价（业务侧自行配置利润空间，展示回收价给用户）；
        如没有拿到销售参考价，则使用57项，走价格2.0系统拿回收价。
    3. 配置34项与17项的映射关系（运营完成）'''

    product_41 = Get_Product_Sale_Evaluate_Price()
    # product_41.get_product_sale_evaluate_price(productId='41567',channelId='40000001')

    # strPlatform: 9 PlatformName: 定价专用平台(和不传channelID场景一样）
    # product_41.get_product_sale_evaluate_price(productId='41567',channelId='10000192')

    # "_errStr":"channelId不为空"
    # product_41.get_product_sale_evaluate_price(productId='41567',channelId='')


    # "_errStr":"渠道获取平台信息失败"
    # product_41.get_product_sale_evaluate_price(productId='41567',channelId='20200202')

    product_41.get_product_sale_evaluate_price(productId='41567',channelId='40000001')

'''
流程
SELECT Fanswer_id, Feva_id, Fweight FROM t_check_mapping_eva, t_eva_item_base  WHERE t_eva_item_base.Fid = t_check_mapping_eva.Feva_id AND t_check_mapping_eva.Fvalid=1 AND t_eva_item_base.Fvalid=1 AND t_check_mapping_eva.Fanswer_id IN (7419,7423,7426,7429,7433,7439,7443,7445,7450,7452,7460,7463,7465,7468,7470,7475,7482,7487,7490,7493,7503,7506,7511,7520,7524,7615,7532,7538,7544,7548,7555,7557,7560,7562,7571,7575,7578,7580,7586,7589,7610,7613);

curl -H 'HSB-OPENAPI-SIGNATURE:7c8ed48789d2231c52a66828a0cd4c79' -H 'HSB-OPENAPI-CALLERSERVICEID:216008' -d '{"_head":{"_callerServiceId":"216008","_groupNo":"1","_interface":"product_id_info_get","_invokeId":"cf29136d40e01f682dfb57a9d5c31131","_msgType":"request","_remark":"","_timestamps":"1612259614","_version":"0.01"},"_param":{"evaFlag":"1","fchannel_id":"","fproduct_id":"41567","platformType":"1"}}' http://prdserver.huishoubao.com/rpc/new_product_lib

curl -H 'HSB-OPENAPI-SIGNATURE:cccfcab55aa699e20251c9dcec822e05' -H 'HSB-OPENAPI-CALLERSERVICEID:216008' -d '{"_head":{"_callerServiceId":"216008","_groupNo":"1","_interface":"eva_option_get","_invokeId":"908f753b3d5e1b3f8aa44b77a3b049b2","_msgType":"request","_remark":"","_timestamps":"1612259614","_version":"0.01"},"_param":{"channel_id":"","pid":"","platform_type":"1","product_id":"41567"}}' http://prdserver.huishoubao.com/rpc/new_product_lib

curl -d '{"head":{"interface":"evaluateSecond","msgtype":"request","remark":"","version":"0.01"},"params":{"channel_id":"40000001","cookies":"server-evaluate_detect","ip":"127.0.0.1","isBottomPrice":"1","productid":"41567","select":["1078","12","3245","17","21","2171","24","224","36","1091","56","5535","59","61","66","3247","6930","3244","3242","7642","82","1083"],"userid":"0"}}' http://evaserver.huishoubao.com/rpc/evaluate  
    Reply:{"body":{"data":{"bottomPrice":"11500","evaluateid":"21025742","quotation":"11500"},"ret":"0","retcode":"0","retinfo":"成功"},"head":{"interface":"evaluateSecond","msgtype":"response","remark":"","version":"0.01"}}
    
    hit cache time:1612257985 PId:0 tagId:0 channelId:40000001 channelFlag:1 platformId:1 platformName:2C
    productId:41567 pId: channelId:40000001 platformType:1
    
    select Fevaluate_item, Fstandard_price, Fmax_price, Fmin_price, Fversion, Fplatform_type, Fitem_group, Fvalid, Fitem_add_sub, Falgorithm_order, Fall_combination_price from t_eva_product_operate  where Fproduct_id = 41567 and Fchannel_id = 40000001 and Fdelete_flag = 1
    Platform Eva Version: 926 standardPrice:225000
    
    select tbp.Fproduct_id, tbbr.Frule_info, tbbr.Fmin_price, tbbr.Fvalid from t_bangmai_product tbp, t_bangmai_bottom_rule tbbr where tbp.Fbottom_price_rule_id=tbbr.Fid and tbp.Fproduct_id=41567
    输入值:11500 最低价:1100 选定保底价区间, 起始值:5000 终止值:20000 类型:2 值:0 11500+0=11500

sku 必须全
标准检测机况，可以没有，可以全，也可以只有部分；价格拿到标准检测选项->映射成17项的估价选项，完成估价；如果17项里有的没找到映射选项，默认取最好的那个估价
'''