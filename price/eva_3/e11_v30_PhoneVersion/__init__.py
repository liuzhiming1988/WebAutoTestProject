# -*- coding: utf-8 -*-
# @File    : __init__.py.py
# @Time    : 2021/8/26 15:30
# @Author  : MikingZhang

'''
/huishoubao/config
vim BasePriceConfServer.xml

# 1. 1-走价格2.0，等级模板；   2-走价格3.0，等级标准
<Other>
    <Key>V3PhoneVersion</Key>
    <Value>1</Value>
</Other>
# 2. 更改后，重启BasePriceConfServer服务

用例1：version保留1，销售方案估价，使用类型-34-估价，
    1.1. 销售定价维护，保存一遍机型
    1.2. http://bpeserver.huishoubao.com/base_price/evaluate  （旧的定价估价接口）
    {"_head":{"_callerServiceId":"116006","_groupNo":"1","_interface":"evaluate","_invokeId":"mikingzhang_adjustPrice2nd","_msgType":"response","_remark":"","_timestamps":"1629967396","_version":"0.01"},"_data":{"_errStr":"SUCCESS","_data":{"quotation":"34400","evaBasePrice":"33900","adjustPrice":"31800","adjustPrice2nd":"34400","recordId":"92108919251","levelId":"2","levelName":"K11","saleLevelId":"","saleLevelName":"","baseLevelTag":[],"saleLevelTag":[]},"_errCode":"0","_ret":"0"}}

    1.3. http://bpeserver.huishoubao.com/adjustment_price/sale_apply_price  （新的 销售价应用方案估价接口，出4个价格）
    {"_head":{"_callerServiceId":"116006","_groupNo":"1","_interface":"sale_apply_price","_invokeId":"mikingzhang_adjustPrice","_msgType":"response","_remark":"","_timestamps":"1629967558","_version":"0.01"},"_data":{"_errStr":"SUCCESS","_data":{"evaBasePrice":"165800","sellerPrice":"193900","sellerMaxPrice":"232600","buyerPrice":"207400","recordId":"92108919454","levelId":"600","levelName":"S","saleLevelId":"0","saleLevelName":"","baseLevelTag":[],"saleLevelTag":[]},"_errCode":"0","_ret":"0"}}

用例2：version切成2，  销售方案估价，可以继续使用类型-34，如果同样选项的机型，价格会是一致
    2.1. 销售定价维护，保存一遍机型
    2.2. http://bpeserver.huishoubao.com/base_price/evaluate  （旧的定价估价接口）
    {"_head":{"_callerServiceId":"116006","_groupNo":"1","_interface":"evaluate","_invokeId":"mikingzhang_adjustPrice2nd","_msgType":"response","_remark":"","_timestamps":"1629968112","_version":"0.01"},"_data":{"_errStr":"SUCCESS","_data":{"quotation":"34400","evaBasePrice":"33900","adjustPrice":"31800","adjustPrice2nd":"34400","recordId":"92108920147","levelId":"2","levelName":"K11","saleLevelId":"","saleLevelName":"","baseLevelTag":[],"saleLevelTag":[]},"_errCode":"0","_ret":"0"}}

    2.3. http://bpeserver.huishoubao.com/adjustment_price/sale_apply_price  （新的 销售价应用方案估价接口，出4个价格）
     {"_head":{"_callerServiceId":"116006","_groupNo":"1","_interface":"sale_apply_price","_invokeId":"mikingzhang_adjustPrice","_msgType":"response","_remark":"","_timestamps":"1629968298","_version":"0.01"},"_data":{"_errStr":"SUCCESS","_data":{"evaBasePrice":"165800","sellerPrice":"193900","sellerMaxPrice":"232600","buyerPrice":"207400","recordId":"92108920350","levelId":"600","levelName":"S","saleLevelId":"0","saleLevelName":"","baseLevelTag":[],"saleLevelTag":[]},"_errCode":"0","_ret":"0"}}
'''