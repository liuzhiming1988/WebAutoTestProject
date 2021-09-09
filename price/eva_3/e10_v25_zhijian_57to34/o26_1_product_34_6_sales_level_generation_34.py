#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 34. 销售等级的生成 - http://wiki.huishoubao.net/index.php?s=/105&page_id=6051
    服务：base_product
    1. 标准检机况：不需要传channelId  |  2. 大质检机况：需要传channelId（销售价格查询需求中，产品需要的是是2C平台，默认使用 回收宝主站 渠道id

    入参：_interface：sales_level_generation_34，销售等级生成（灰度测试接口）
        productId：产品Id （必填） | channelId：渠道Id （必填）；
        aIdList：估价答案项列表（可直接通过 产品服务 - 6.可估价产品产品选项获取（eva_option_get） 取到估价答案项）（必填）；
        cIdList：估价检测细化项列表（必填，可传空） |  orderId：订单号（非必填）
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
    def product_check_item_34(self, productId):
        param = {"_head": { "_interface":"product_check_item_34", "_msgType":"request", "_remark":"", "_version":"0.01", "_timestamps":"123456", "_invokeId":"123456", "_callerServiceId":"112006", "_groupNo":"1" },"_param": {"productId":productId}}
        url = "http://codserver.huishoubao.com/detect/product_check_item"
        md5value = json.dumps(param) + "_" + self.secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":self.callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
        respone.encoding = respone.apparent_encoding  # 编码设置
        respone_dict = json.loads(respone.text)  # 转成字典
        checkList = respone_dict['_data']['_data']['checkList']

        strCheckList = []
        strCheckDesc = ''
        for info in checkList:
            answerList = info['answerList']
            '''第一种方式：在answerList下随机取1个'''
            # index = random.randint(0, len(answerList) - 1)
            # strCheckList.append(answerList[index]['answerId'])
            # strCheckDesc += '"' + info['questionName'] + ":" + answerList[index]['answerName'] + '",'

            '''第二种方式：在answerList下取answerWeight最大的那个'''
            index = sorted(answerList, key=lambda x: int(x['answerWeight']), reverse=True)[0]
            strCheckList.append(index['answerId'])
            strCheckDesc += '"' + info['questionName'] + ":" + index['answerName'] + '",'
        return strCheckList, strCheckDesc

    def sales_level_generation_34(self, productId, channelId):
        (checkAIdList, checkAIdList_desc) = self.product_check_item_34(productId=productId)
        param = {"_head":{"_interface":"sales_level_generation_34","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"","_invokeId":"","_callerServiceId":"112002","_groupNo":"1"},"_param":{"productId":productId, "channelId":channelId, "orderId":"", "aIdList":"", "cIdList":"", "checkAIdList":checkAIdList}}
        secret_key = "HKmTk03iDUCLIrFrrQkfOxPiGyGPqxb9"
        callerserviceid = "112002"
        url = "http://prdserver.huishoubao.com/product/sales_level_generation"
        md5value = json.dumps(param) + "_" + secret_key
        headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
        respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())

        print('==========1. 产品ID：『{0}』，『请求获取‘销售等级’的标准检测选项-答案项-ID』为：\n'.format(productId), checkAIdList)
        print()
        print('==========2. 产品ID：『{0}』，『请求获取‘销售等级’的标准检测选项-答案项-名称』为：\n'.format(productId), checkAIdList_desc)
        hsb_response_print(respone=respone)

if __name__ == '__main__':
    product_34 = Sales_Level_Generation()
    # product_34.sales_level_generation_34(productId="23007", channelId="10000837")
    # product_34.sales_level_generation_34(productId="3", channelId="10000837")
    # product_34.sales_level_generation_34(productId="30932", channelId="10000837")
    # product_34.sales_level_generation_34(productId="64000", channelId="10000837")
    # product_34.sales_level_generation_34(productId="63904", channelId="10000837")
    # product_34.sales_level_generation_34(productId="38201", channelId="10000837")
    # product_34.sales_level_generation_34(productId="38200", channelId="10000837")
    # product_34.sales_level_generation_34(productId="30833", channelId="10000837")
    # product_34.sales_level_generation_34(productId="30832", channelId="300000010")
    # product_34.sales_level_generation_34(productId="41567", channelId="10000837")
    # product_34.sales_level_generation_34(productId="63330", channelId="10000837")
    # product_34.sales_level_generation_34(productId="64494", channelId="10000837")
    # product_34.sales_level_generation_34(productId="64493", channelId="10000837")
    # product_34.sales_level_generation_34(productId="64495", channelId="10000837")
    # product_34.sales_level_generation_34(productId="64496", channelId="10000837")
    # product_34.sales_level_generation_34(productId="54789", channelId="10000837")
    # product_34.sales_level_generation_34(productId="54790", channelId="10000837")
    # product_34.sales_level_generation_34(productId="54791", channelId="10000837")
    # product_34.sales_level_generation_34(productId="63328", channelId="10000837")
    # product_34.sales_level_generation_34(productId="63329", channelId="10000837")
    # product_34.sales_level_generation_34(productId="63330", channelId="10000837")
    # product_34.sales_level_generation_34(productId="64536", channelId="10000837")
    product_34.sales_level_generation_34(productId="41567", channelId="10000837")

''' 
【销售等级的生成 34项】【base_product】
SELECT * FROM t_bangmai_bottom_channel_map WHERE  Fchannel_id= 40000001;
select Fproduct_id, Ftemplate_id, Fvalid, Fuser_name from t_sales_level_template_product  where Fproduct_id='41567';
select Ftemplate_id from t_pdt_use_check_template_34 where Fvalid=1 and Fproduct_id=41567;
select tpc.Fid Fclass_id, tpc.Fname Fclass_name, tslt.Fid Ftemplate_id, tslt.Fname Ftemplate_name, tslt.Fremarks Fremarks, tslt.Fvalid Fvalid, tslmc.Fcheck_group Fcheck_group, tslmc.Fvalid Fm_valid, tcot.Ftemplate_id Fc_id, tcot.Ftemplate_name Fc_name, tcot.Fvalid Fc_valid, tcot.Fitem_info Fproduct_item from t_pdt_class tpc, t_sales_level_template tslt, t_sales_level_map_check tslmc, t_check_option_template tcot where tpc.Fid=tslt.Fclass_id and tslt.Fid=tslmc.Ftemplate_id and tslmc.Fcheck_template_id=tcot.Ftemplate_id and tslmc.Ftemplate_id='12' and tslmc.Fcheck_template_id='25';
select Ftemplate_id, Flevel, Flevel_name, Flevel_desc, Flevel_label, Fbangmai_desc, Fbangmai_visible, Fbangmai_label, Fvalid from t_sales_level_template_level  where Ftemplate_id='12' and Flevel='260';

outPacket=[{"_data":{"_data":{"level":"260","levelDesc":"外壳：包装已拆封，机身完好配件齐全未激活。可能无原机膜和卡针#屏幕：完好#显示：完好#功能：完好","levelLabel":["全新机","明星之选","满分报告"],"levelName":"S","productId":"41567","templateId":"12"},"_errCode":"0","_errStr":"成功","_ret":"0"},"_head":{"_callerServiceId":"112002","_groupNo":"1","_interface":"sales_level_generation_34","_invokeId":"beb859e7-3cfe-4ca8-9b8f-99589df2eff8","_msgType":"response","_remark":"","_timestamps":"1621933438","_version":"0.01"}}]
'''