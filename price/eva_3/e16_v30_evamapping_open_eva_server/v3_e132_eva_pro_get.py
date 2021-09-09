#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:MikingZhang


''' 定价系统+商品库系统+调价系统+估价系统 - 获取产品列表（可估价）  - http://wiki.huishoubao.com/web/#/347?page_id=15706
    入参：channel_id：渠道id  |  pid：pid，渠道id和pid优先使用pid，但必须都传递，另一个传””即可
        keyword：根据关键字查询，值可为空，此关键字只针对产品名称、产品关键词做匹配
        brandid：根据品牌id（2.0）查询,值可为空  |  brandidV1：1.0品牌id，（可传递空值，当brandid空值，brandidV1有值时，才有效）
        classid：根据类目id查询，值可为空  |  recycletype：根据回收类型查询，可为空值，表示不根据该字段值过滤，3-正常回收，2-山寨机，1-公益回收
        os：根据操作系统过滤，值可为空  |  orderField：排序字段，值可为空，0-id（默认），1-基准价，2-平台最高价
        orderType：排序方式,值可为空，0-正序（默认），1-倒序
        excludeClassId：排除的类目 1手机 2笔记本 3平板 传多个时可用#分割 如:2#3
        ip：用户公网访问IP，例如：10.0.10.62
        pageindex：分页的页码，获取全部数据时值为空，获取分页数据时，值不能为空，代表当前的页码
        pagesize：每页的数据量，获取全部数据时值为空，获取分页数据时，值不能为空，代表每页数据量，最大500
    出参：pageIndex：分页的页码  |  pageSize：每页的数据量
        pdtList：产品列表
            productId：产品id  |  productName：产品名称  |  productLogo：产品图片  |  productMaxPrice：产品最高价
            brandId：品牌id  |  brandName：品牌名称  |  classId：类目id  |  className：类目名称
            pdtSum：产品总数  |  pageInfo：分页信息（新增的字段）
'''

import hashlib, requests, json, os, random
from price.hsb_MD5_Enerypt import Md5Enerypt
from price.hsb_ipProxy_responsePrint import hsb_eva_ipProxy_test,hsb_response_print

def v3_eva_pro_get(channel_id, pid, keyword, brandid, classid, os, recycletype, pageindex, pagesize):
    param = {"_head":{"_interface":"eva_pro_get","_msgType":"request","_remark":"","_version":"0.01","_timestamps":"123","_invokeId":"111","_callerServiceId":"816006","_groupNo":"1"},"_param":{"pageindex":pageindex, "pagesize":pagesize, "channel_id":channel_id, "pid":pid, "keyword":keyword, "brandid":brandid, "classid":classid, "recycletype":recycletype, "os":os, "orderField":'0', "orderType":"1"}}
    secret_key = "R2gFCRbILiNhwv3YbtaGceYJlPS5Ku02"
    callerserviceid = "816006"
    url = "http://prdserver.huishoubao.com/eva_product_v3/eva_spu_get"
    md5value = json.dumps(param) + "_" + secret_key
    headers = {"Content-Type":"application/json;charset=UTF-8","HSB-OPENAPI-SIGNATURE":Md5Enerypt(md5value),"HSB-OPENAPI-CALLERSERVICEID":callerserviceid}
    respone = requests.post(url, json=param, headers=headers, proxies=hsb_eva_ipProxy_test())
    respone.encoding = respone.apparent_encoding  # 编码设置
    hsb_response_print(respone=respone)

if __name__ == '__main__':
    ''' 走了ES 和 Redis，目前2分钟更新一次 '''
    '''1. 渠道ID 和 PID 为空 | "_retcode":"70020100","_ret":"70020100","_retinfo":"请求参数错误 [pid和channel必须传一个，不可都为空]"'''
    # v3_eva_pro_get(channel_id='', pid='', keyword='', brandid='', classid='1', os='', recycletype='3', pageindex='0', pagesize='10')

    '''2. 只传渠道ID | 渠道关联的估价模板-有多个估价子模板，分别被不同的机型使用'''
    # "_retcode":"70020300","_ret":"70020300","_retinfo":"获取估价机型列表失败 [渠道关联的估价模板存在多个估价子模板且被不同机型使用]"
    # v3_eva_pro_get(channel_id='40000001', pid='', keyword='', brandid='', classid='1', os='', recycletype='3', pageindex='0', pagesize='10')

    '''3. 只传PID  |  渠道关联的估价模板-有多个估价子模板，分别被不同的机型使用  | 正常返回多个机型'''
    # v3_eva_pro_get(channel_id='', pid='1001', keyword='', brandid='', classid='1', os='', recycletype='3', pageindex='0', pagesize='10')

    '''4. 传的渠道ID 或 PID，不存在、未绑定过任何估价模板 等 |  价格不做这个渠道ID/PID的合法性校验，查询不到记录，则使用 全部渠道 对应的数据返回'''
    # v3_eva_pro_get(channel_id='202108021111', pid='', keyword='', brandid='', classid='1', os='', recycletype='3', pageindex='0', pagesize='10')
    # v3_eva_pro_get(channel_id='', pid='202108021111', keyword='', brandid='', classid='1', os='', recycletype='3', pageindex='0', pagesize='10')
    # v3_eva_pro_get(channel_id='202108021111', pid='202108021111', keyword='', brandid='', classid='1', os='', recycletype='3', pageindex='0', pagesize='10')

    '''5. 同时传渠道ID 和 PID，但它们不对应 | 价格不做这个渠道ID/PID的合法性校验，查询不到记录，则使用 全部渠道 对应的数据返回'''
    # v3_eva_pro_get(channel_id='10000837', pid='1001', keyword='', brandid='', classid='1', os='', recycletype='3', pageindex='0', pagesize='10')

    '''6. 同时传渠道ID 和 PID，按品牌ID、类目ID查询 | 正常'''
    # v3_eva_pro_get(channel_id='40000001', pid='1001', keyword='', brandid='2', classid='1', os='', recycletype='3', pageindex='0', pagesize='10')
    # v3_eva_pro_get(channel_id='40000001', pid='1001', keyword='', brandid='2', classid='2', os='', recycletype='3', pageindex='0', pagesize='10')

    '''7. 同时传渠道ID 和 PID，渠道和PID 对应，但是没有关联任何估价模板 | 正常（搜索模板产品表，没有找到机型）'''
    # v3_eva_pro_get(channel_id='10000334', pid='1996', keyword='', brandid='2', classid='2', os='', recycletype='3', pageindex='0', pagesize='10')

    '''8. 同时传渠道ID 和 PID（正常value）'''
    # v3_eva_pro_get(channel_id='40000001', pid='1001', keyword='', brandid='', classid='1', os='', recycletype='3', pageindex='0', pagesize='10')
    # v3_eva_pro_get(channel_id='40000001', pid='1001', keyword='', brandid='', classid='1', os='', recycletype='3', pageindex='0', pagesize='20')

    '''9. 同时传渠道ID 和 PID | 满足条件的机型中，有不支持估价的 | 正常（不支持估价的机型，不会返回）'''
    # v3_eva_pro_get(channel_id='40000001', pid='1001', keyword='', brandid='', classid='1', os='', recycletype='3', pageindex='0', pagesize='20')

    '''10. 同时传渠道ID 和 PID | 满足条件的机型中，有禁用状态的机型 | 正常（禁用状态的机型，不会返回）'''
    # v3_eva_pro_get(channel_id='40000001', pid='1001', keyword='', brandid='', classid='1', os='', recycletype='3', pageindex='0', pagesize='20')

    '''11. 同时传渠道ID 和 PID | PID没有被“部分渠道/PID”的估价模板关联，估价模板中有“使用中、全部渠道”属性的 | 正常（使用了 全部渠道 的这个估价模板的机型会返回'''
    # v3_eva_pro_get(channel_id='10000837', pid='3415', keyword='', brandid='', classid='1', os='', recycletype='3', pageindex='0', pagesize='20')


    v3_eva_pro_get(channel_id='10000164', pid='1405', keyword='41567', brandid='', classid='1', os='', recycletype='3', pageindex='0', pagesize='20') # 估价系统2C自测
    v3_eva_pro_get(channel_id='10000165', pid='1406', keyword='', brandid='', classid='1', os='', recycletype='3', pageindex='0', pagesize='20') # 估价系统2B自测
    v3_eva_pro_get(channel_id='10000166', pid='1407', keyword='', brandid='', classid='1', os='', recycletype='3', pageindex='0', pagesize='20') # 估价系统微回收自测
    v3_eva_pro_get(channel_id='10000167', pid='1408', keyword='', brandid='', classid='1', os='', recycletype='3', pageindex='0', pagesize='20') # 估价系统转转自测
    v3_eva_pro_get(channel_id='10000168', pid='1409', keyword='', brandid='', classid='1', os='', recycletype='3', pageindex='0', pagesize='20') # 估价系统vivo自测
