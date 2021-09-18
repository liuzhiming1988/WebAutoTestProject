#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 产品服务 - 39.闲鱼帮卖检测估价接口返回回收价,定价,最高可售价 - http://wiki.huishoubao.com/web/#/105?page_id=6810
    现在是优先取 channelId， 再取  orderId对应渠道 | 对应服务：server-evaluate_detect

    依赖接口：产品服务 | 21.获取检测标准化产品信息【产品商品库sku信息 + 标准检测机况信息】【57】 | http://wiki.huishoubao.com/index.php?s=/105&page_id=3295
    服务：base_product | 标准检（多、细项，一般检测侧使用）

    skuList：【产品商品库SKU信息】对应新后台，product_lib_new——>SPU列表——>SKU选项管理
    checkList：【标准检测机况信息】对应新后台，机况检测模板——>(搜索：类目-手机，状态-开启）
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test
from price.dingdingTalk_push_demo import dingdingTalk_push_run

class Check_Evaluate_All_Price:
	def product_21_product_check_item(self, productId, orderId):
		param = {"_head": {"_interface": "product_check_item", "_msgType": "request", "_remark": "", "_version": "0.01","_timestamps": "123456", "_invokeId": "123456", "_callerServiceId": "112006","_groupNo": "1"}, "_param": {"productId": productId, "orderId": orderId}}

		secret_key = "gYt8YHmZVUtq9BxHzmNBQ0Eo7oGi8IKU"
		callerserviceid = "112006"
		url = "http://codserver.huishoubao.com/detect/product_check_item"
		md5value = json.dumps(param) + "_" + secret_key
		headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID": callerserviceid}
		respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
		respone.encoding = respone.apparent_encoding  # 编码设置
		respone = json.loads(respone.text)  # 转成字典
		checkList = respone['_data']['_data']['checkList']
		skuList = respone['_data']['_data']['skuList']

		strSkuList = []
		for info_sku in skuList:
			answerList_sku = info_sku['answerList']
			index_sku = random.randint(0, len(answerList_sku) - 1)
			strSkuList.append(answerList_sku[index_sku]['answerId'])

		strCheckList = []
		for info_check in checkList:
			answerList_check = info_check['answerList']
			index_check = random.randint(0, len(answerList_check) - 1)
			strCheckList.append(answerList_check[index_check]['answerId'])

		return strSkuList, strCheckList

	def check_evaluate_all_price(self, productId, orderId, channelId ):
		# (skuList, checkList) = self.product_21_product_check_item(productId=productId,orderId=orderId)
		skuList = ['15', '471', '18', '2236', '38', '1091', '1773']
		checkList = ['7420', '7423', '7426', '7430', '7434', '7436', '7442', '7445', '7449', '7453', '7460', '7462']
		param = {"_head": {"_interface": "check_evaluate_all_price", "_msgType": "request", "_remark": "hello","_version": "0.01", "_timestamps": "123", "_invokeId": "111", "_callerServiceId": "200001","_groupNo": "1"},"_param": {"orderId": orderId, "productId": productId,"skuList": skuList,"checkList": checkList,"channelId": channelId}}
		secret_key = "dk26kmdasnph0voz69fj0jpv7t3ixev8"
		callerserviceid = "200001"
		url = "http://codserver.huishoubao.com/detect/check_evaluate_all_price"
		md5value = json.dumps(param) + "_" + secret_key
		headers = {"Content-Type": "application/json;charset=UTF-8", "HSB-OPENAPI-SIGNATURE": Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID": callerserviceid}
		respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
		respone.encoding = respone.apparent_encoding  # 编码设置

		print('『{0}』 产品的『sku信息』(随机取)为：\n'.format(productId), skuList)
		print('\n『{0}』 产品的『标准检测机况信息』(随机取)为：\n'.format(productId), checkList)
		print('\ncheck_evaluate_all_price接口响应数据为：\n', respone.text + '接口响应时长：{0} 秒\n'.format(respone.elapsed.total_seconds()))

if __name__ == '__main__':
	product_39 = Check_Evaluate_All_Price()
	''' 10000253 渠道id 一期，两个渠道id不一样'''
	# product_39.check_evaluate_all_price(productId='63398', orderId='7573755', channelId='10000253') # 华为 Mate 30   √
	# product_39.check_evaluate_all_price(productId='63330', orderId='7573755', channelId='10000253') # iPhone 11   √
	# product_39.check_evaluate_all_price(productId='54789', orderId='7573755', channelId='10000253') # iPhone XS Max   √
	# product_39.check_evaluate_all_price(productId='63399', orderId='7573755', channelId='10000253') # 华为 Mate 30 Pro  20200730-B端帮卖价格切换至定价系统
	# product_39.check_evaluate_all_price(productId='2068', orderId='7573755', channelId='10000253') # OPPO R9s  √
	# product_39.check_evaluate_all_price(productId='2063', orderId='7573755', channelId='10000253') # OPPO R9 Plus  √
	# product_39.check_evaluate_all_price(productId='60477', orderId='7573755', channelId='10000253') # 华为 Mate 20 Pro 屏幕指纹版  √
	# product_39.check_evaluate_all_price(productId='60292', orderId='7573755', channelId='10000253') # 华为 P30 Pro  √
	# product_39.check_evaluate_all_price(productId='49239', orderId='7573755', channelId='10000253') # 小米 8  √
	# product_39.check_evaluate_all_price(productId='23036', orderId='7573755', channelId='10000253') # 小米 5  √
	# product_39.check_evaluate_all_price(productId='41567', orderId='7573755', channelId='10000253') # iPhone x 20200730-B端帮卖价格切换至定价系统
	# product_39.check_evaluate_all_price(productId='30751', orderId='7573755', channelId='10000253') # iPhone 5 20200730-B端帮卖价格切换至定价系统（未定价）
	# product_39.check_evaluate_all_price(productId='3', orderId='7573755', channelId='10000253') # iPhone 4 20200730-B端帮卖价格切换至定价系统（机况匹配不上等级）

	# for i in range(5):
	# 	# 20200803-B端帮卖价格切换至定价系统（跑更多的机型） 华为 Mate 30 Pro
	# 	product_39.check_evaluate_all_price(productId='63399', orderId='7573755', channelId='10000253')

	''' 10000293  两个渠道id一样 '''
	# product_39.check_evaluate_all_price(productId='63398', orderId='7573755', channelId='10000253')
	# product_39.check_evaluate_all_price(productId='41567', orderId='7573755', channelId='10000253')
	# product_39.check_evaluate_all_price(productId='63330', orderId='7573755', channelId='10000253')
	# product_39.check_evaluate_all_price(productId='60477', orderId='7573755', channelId='10000253')

	''' 2021年5月27日 对接口list进行严格校验'''
	# "_errStr":"估价SKU项 购买渠道 在标准检测中未传递对应选项 或者 估价Sku映射配置错误未匹配到"
	# product_39.check_evaluate_all_price(productId='41567', orderId='7632136', channelId='10000253') # skuList = []  checkList = []

	# "_errStr":"skuList 参数格式错误"
	# product_39.check_evaluate_all_price(productId='41567', orderId='7632136', channelId='10000253') # skuList = [""]  checkList = [""]

	# "_errStr":"skuList 参数格式错误"
	# product_39.check_evaluate_all_price(productId='41567', orderId='7632136', channelId='10000253') # skuList = ["abc"]  checkList = [""]

	# skuList = ['15', '471', '18', '2236', '38', '1091', '1773']  checkList = []   |  正常
	# product_39.check_evaluate_all_price(productId='41567', orderId='7632136', channelId='10000253')

	# skuList = ['15', '471', '18', '2236', '38', '1091', '1773']  checkList = [""]   |  "_errStr":"checkList 参数格式错误"
	# product_39.check_evaluate_all_price(productId='41567', orderId='7632136', channelId='10000253')

	# skuList = ['15', '471', '18', '2236', '38', '1091', '1773']  checkList = ["abc"]   |  "_errStr":"checkList 参数格式错误"
	# product_39.check_evaluate_all_price(productId='41567', orderId='7632136', channelId='10000253')

	# skuList = ['15', '471', '18', '2236', '38', '1091', '1773']
	# checkList = ['7420', '7423', '7426', '7430', '7434', '7436', '7442', '7445', '7449', '7453', '7460', '7462']  |  正常
	product_39.check_evaluate_all_price(productId='41567', orderId='7632136', channelId='10000253')
