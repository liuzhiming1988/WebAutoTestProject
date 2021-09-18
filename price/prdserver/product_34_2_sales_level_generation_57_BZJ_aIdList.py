#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 34.销售等级的生成 - sales_level_generation - http://wiki.huishoubao.net/index.php?s=/105&page_id=6051
    服务：base_product
    1. 标准检机况：不需要传channelId  |  2. 大质检机况：需要传channelId（销售价格查询需求中，产品需要的是2C平台，默认使用 回收宝主站 渠道id

    入参：productId：产品Id （必填） | channelId：渠道Id （必填）；
        aIdList：估价答案项列表（可直接通过 产品服务 - 6.可估价产品产品选项获取（eva_option_get）  取到估价答案项） （必填）；
        cIdList：估价检测细化项列表（必填，可传空） | orderId：订单号（非必填）
        checkAIdList：检测答案项列表,检测,估价答案项只要包含其一就可，即(channelId&&aIdList&&cIdList) or checkAIdList  （非必填）；
        isRecord：是否做记录,1-做记录，0-不做记录，只给估价后台使用，默认记录（非必填）
    出参：productId：产品id | templateId：使用的销售等级模版Id | level：成色等级
        levelName：成色名称 | levelDesc：成色描述 | levelLabel：销售标签
        _retcode：3001：配置问题 根据产品ID获取不到销售等级模版; | 3002：配置问题 该产品已被禁用,无法生成销售等级;
            3003：配置问题 该产品配置的销售等级模版被禁用; | 3004：配置问题 该产品配置的销售等级模版和选项模版的映射被禁用;
            3005：配置问题 产品使用的检测模版未和销售等级模版建立映射; | 3006：配置问题 产品未使用检测模版;
            3008：配置问题 无法生成等级; 1-系统错误和参数错误，0-成功
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

class Sales_Level_Generation:
    def __init__(self):
        self.secret_key = "gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU"
        self.callerserviceid = "112006"

    # 产品服务 - 21.获取检测标准化产品信息【产品商品库sku信息 + 标准检测机况信息】【57】 - http://wiki.huishoubao.com/index.php?s=/105&page_id=3295
    def product_check_item(self, productId):
        param = {"_head": { "_interface":"product_check_item", "_msgType":"request", "_remark":"", "_version":"0.01", "_timestamps":"123456", "_invokeId":"123456", "_callerServiceId":"112006", "_groupNo":"1" },"_param": {"productId":productId}}
        url = "http://codserver.huishoubao.com/detect/product_check_item"
        md5value = json.dumps(param) + "_" + self.secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":self.callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典
        skuList = respone_dict['_data']['_data']['skuList']
        checkList = respone_dict['_data']['_data']['checkList']

        strSkuList = []
        strSkuDesc = ''
        for info in skuList:
            answerList = info['answerList']
            index = random.randint(0, len(answerList) - 1)
            strSkuList.append(answerList[index]['answerId'])
            strSkuDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'

        strCheckList = []
        strCheckDesc = ''
        for info in checkList:
            answerList = info['answerList']
            index = random.randint(0, len(answerList) - 1)
            strCheckList.append(answerList[index]['answerId'])
            strCheckDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'
        return strSkuList, strCheckList, strSkuDesc, strCheckDesc

    # 产品服务 | 22.检测标准化选项转换估价选项 | http://wiki.huishoubao.com/index.php?s=/105&page_id=3297
    def convert_check_item_to_eva(self, orderId, productId, isOverInsurance):
        (skuList, checkList, skuDesc, checkDesc) = self.product_check_item(productId=productId)
        param = {"_head": { "_interface":"convert_check_item_to_eva", "_msgType":"request", "_remark":"", "_version":"0.01", "_timestamps":"123456", "_invokeId":"123456", "_callerServiceId":"112006", "_groupNo":"1" },"_param": {"orderId":orderId, "productId":productId, "skuList":skuList, "checkList":checkList, "isOverInsurance":isOverInsurance }}
        url = "http://codserver.huishoubao.com/detect/convert_check_item_to_eva"
        md5value = json.dumps(param) + "_" + self.secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":self.callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典
        print("======转换估价选项参数==========={}".format(param))
        print('==========1. 产品sku选项-答案项ID（随机取）：\n', skuList)
        print()
        print('==========2. 检测机况选项-答案项ID（随机取）：\n', checkList)
        print()
        print('==========3. 以上【sku】+【机况】选项对应的问题项名称+答案项名称：\n', '{' + skuDesc + checkDesc[:-1] + '}' + '\n')

        return respone_dict['_data']['_data']['select'], respone_dict['_data']['_data']['selectName']

    def sales_level_generation_57(self, productId, orderId, isOverInsurance, channelId):
        (aIdList, aIdListOption) = self.convert_check_item_to_eva(orderId=orderId, productId=productId, isOverInsurance=isOverInsurance)
        param = {"_head":{"_interface":"sales_level_generation","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"","_invokeId":"","_callerServiceId":"112002","_groupNo":"1"},"_param":{"productId":productId,"orderId":orderId,"channelId":channelId,"aIdList":aIdList,"cIdList":[]}}
        secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
        callerserviceid = "112002"
        url = "http://prdserver.huishoubao.com/product/sales_level_generation"
        md5value = json.dumps(param) + "_" + secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())

        print('==========4. 产品ID：『{0}』，『请求获取‘销售等级’的估价答案项』为：\n'.format(productId), aIdList)
        print()
        print('==========5. 转换后的SKU+机况选项的描述：\n', aIdListOption)
        print()
        hsb_response_print(respone=respone)

if __name__ == '__main__':
    product_34 = Sales_Level_Generation()
    product_34.sales_level_generation_57(productId='41567', orderId='7601020', isOverInsurance='1', channelId='40000001')

    ''' 0422 下单时机型使用的选项模板。
    检测调获取销售等级接口传参。  正常场景如下 --- 188  电池测试   拍照测试     屏幕测试'''
    # product_34.sales_level_generation_57(productId="63994", orderId='7583699', isOverInsurance='1', channelId="40000001")

    ''' 0422 检测之前，机型使用的选项模板已更新（新增的模板，有添加/删除选项）
    0422 检测时，订单仍在保价周期内，检测获取的机型选项还是来自下单时使用的选项模板
    0422 检测调获取销售等级接口传参同上，还是旧选项模板的答案项）。异常场景如下 --  189  电池测试   问题项测试   屏幕测试。
    "_errCode":"3008","_errStr":"配置问题 无法生成等级"
    ①传订单id，正常，价格才能查到对应使用的版本号及其对应模板；  ②不传订单id或传空，不正常，会使用线上版本号对应模板'''
    # product_34.sales_level_generation_57(productId="63994", orderId='7583699', isOverInsurance='1', channelId="40000001")

    ''' 回归（平台不运营，走统一估价）'''
    # product_34.sales_level_generation_57(productId="63994", orderId='7583719', isOverInsurance='1', channelId="40000001")

    ''' 回归 B端帮卖测试  2020.03.06
    SELECT * FROM t_bangmai_bottom_channel_map WHERE  Fchannel_id= 10000253; 中 Fsale_type：是否是定价平台：1是
    2C（B端寄卖平台渠道）帮卖业务渠道，Fsale_type=1  '''
    # product_34.sales_level_generation_57(productId="30748", orderId='', isOverInsurance='1', channelId="10000253")

    ''' 2B（回收宝APP测试）非帮卖业务渠道（属正常流程）'''
    # product_34.sales_level_generation_57(productId="30748", orderId='', isOverInsurance='1', channelId="5032000")
    # product_34.sales_level_generation_57(productId="57071", orderId='', isOverInsurance='1', channelId="40000001")

    '''【20210120原则上】平板和笔记本，只有大质检，没有保价概念
    但是，获取销售等级，不管走标准检还是大质检，最终都可以通过传 aIdList（估价答案项list）来获取销售等级
    即使是走标准件，价格接口会将其检测选项转换成估价选项，检测只需要传 aIdList，就可以通过销售等级模板映射的估价选项模板来获取到等级 '''
    # 平板  | 64011 | ZY0101210120000136 | iPad Pro 12.9寸 4代 2020款
    # product_34.sales_level_generation_57(productId="64011", orderId='7605607', isOverInsurance='0', channelId="40000001") # iPad Pro 12.9寸 4代 2020款
    # product_34.sales_level_generation_57(productId="30765", orderId='7605614', isOverInsurance='0', channelId="40000001") # iPad Pro 9.7寸 2016款
    # product_34.sales_level_generation_57(productId="31150", orderId='7605615', isOverInsurance='0', channelId="40000001") # iPad 1代
    # product_34.sales_level_generation_57(productId="31201", orderId='7605617', isOverInsurance='0', channelId="40000001") # iPad 4代 (Retina屏)
    # product_34.sales_level_generation_57(productId="31231", orderId='7605618', isOverInsurance='0', channelId="40000001") # iPad mini4
    # product_34.sales_level_generation_57(productId="59114", orderId='7605619', isOverInsurance='0', channelId="40000001") # iPad Pro 12.9寸 3代 2018款
    # product_34.sales_level_generation_57(productId="64011", orderId='7605620', isOverInsurance='0', channelId="40000001") # iPad Pro 12.9寸 4代 2020款

    # product_34.sales_level_generation_57(productId="64327", orderId='7605660', isOverInsurance='0', channelId="40000001") # 华为MediaPad T5 10.1英寸
    # product_34.sales_level_generation_57(productId="63815", orderId='7605670', isOverInsurance='0', channelId="40000001") # 华为 MatePad Pro 10.8英寸

''' 
正常的
SELECT * FROM t_bangmai_bottom_channel_map WHERE  Fchannel_id= 40000001 ;
select Fproduct_id, Ftemplate_id, Fvalid, Fuser_name from t_sales_level_template_product  where Fproduct_id='30748';
select Fitem_template_id from t_eva_platform_product where Fvalid=1 and Fproduct_id='30748' and Fplatform_type='1';
select tpc.Fid Fclass_id, tpc.Fname Fclass_name, tslt.Fid Ftemplate_id, tslt.Fname Ftemplate_name, tslt.Fremarks Fremarks, tslt.Fvalid Fvalid, tslmo.Foption_group Foption_group, tslmo.Fvalid Fm_valid, teot.Fid Fo_id, teot.Ftemplate_name Fo_name, teot.Fvalid Fo_valid, teot.Fproduct_item Fproduct_item from t_pdt_class tpc, t_sales_level_template tslt, t_sales_level_map_option tslmo, t_eva_option_template teot where tpc.Fid=tslt.Fclass_id and tslt.Fid=tslmo.Ftemplate_id and tslmo.Foption_template_id=teot.Fid  and tslmo.Ftemplate_id='12' and tslmo.Foption_template_id='127';
select Ftemplate_id, Flevel, Flevel_name, Flevel_desc, Flevel_label, Fbangmai_desc, Fbangmai_visible, Fbangmai_label, Fvalid from t_sales_level_template_level  where Ftemplate_id='12' and Flevel='260';

B端帮卖
SELECT * FROM t_bangmai_bottom_channel_map WHERE  Fchannel_id= 10000253;
BottomChannelMap Rule: channel[10000253] SaleType[1]
select Fproduct_id, Ftemplate_id, Fvalid, Fuser_name from t_sales_level_template_product  where Fproduct_id='30748';
定价渠道，强制转换成2C平台
select Fitem_template_id from t_eva_platform_product where Fvalid=1 and Fproduct_id='30748' and Fplatform_type='1';
select tpc.Fid Fclass_id, tpc.Fname Fclass_name, tslt.Fid Ftemplate_id, tslt.Fname Ftemplate_name, tslt.Fremarks Fremarks, tslt.Fvalid Fvalid, tslmo.Foption_group Foption_group, tslmo.Fvalid Fm_valid, teot.Fid Fo_id, teot.Ftemplate_name Fo_name, teot.Fvalid Fo_valid, teot.Fproduct_item Fproduct_item from t_pdt_class tpc, t_sales_level_template tslt, t_sales_level_map_option tslmo, t_eva_option_template teot where tpc.Fid=tslt.Fclass_id and tslt.Fid=tslmo.Ftemplate_id and tslmo.Foption_template_id=teot.Fid  and tslmo.Ftemplate_id='12' and tslmo.Foption_template_id='127';
select Ftemplate_id, Flevel, Flevel_name, Flevel_desc, Flevel_label, Fbangmai_desc, Fbangmai_visible, Fbangmai_label, Fvalid from t_sales_level_template_level  where Ftemplate_id='12' and Flevel='260';
'''