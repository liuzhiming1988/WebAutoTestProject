#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : IMEI.py
@Author  : liuzhiming
@Time    : 2021/6/17 17:09
"""

from random import randint

"""
IMEI为15位数字
格式为AAAAAAAA BBBBBB C
AAAAAAAA 为 Type Allocation Code
BBBBBB 为 Serial Number
C 为 Check Digit
IMEI校验码算法：
(1).将偶数位数字分别乘以2，分别计算个位数和十位数之和
(2).将奇数位数字相加，再加上上一步算得的值
(3).如果得出的数个位是0则校验位为0，否则为10减去个位数
"""


def generate_imei():
    """

    :param number:
    :return:
    """
    num = randint(10000000000000, 99999999999999)
    st = str(num)
    odd_sum = 0  # 奇数
    ten_digit = 0  # 个位数之和
    single_digit = 0  # 十位数之和
    for x in range(14):
        if x % 2 == 0:
            odd_sum += int(st[x])  # 奇数位处理
        else:
            num = int(st[x]) * 2
            ten_digit += int(num / 10)  # 偶数位的十位数处理
            single_digit += num % 10   # 偶数位的个位数处理

    # 相加计算最后结果
    res = odd_sum + ten_digit + single_digit
    ass = res % 10
    if ass == 0:
        check_digit = "0"
    else:
        check_digit = str(10-ass)
    imei = st+check_digit
    # print(imei)
    return imei


if __name__ == '__main__':
    imei = generate_imei()
    print(imei)

    # 打印可下单的机型ID
    raw = {"_data":{"productList":[{"productId":"64494","productLogo":"https:\/\/s1.huishoubao.com\/img\/phone\/604259_1602657029320.jpg","productMaxPrice":"508000","productName":"iPhone 12","icon":"","brandId":"2","brandName":"苹果","brandIdV2":"2","classId":"1","className":"手机","activityIcon":"","activityText":"","activityDesc":""},{"productId":"64495","productLogo":"https:\/\/s1.huishoubao.com\/img\/phone\/820112_1602657247140.jpg","productMaxPrice":"774900","productName":"iPhone 12 Pro","icon":"","brandId":"2","brandName":"苹果","brandIdV2":"2","classId":"1","className":"手机","activityIcon":"","activityText":"","activityDesc":""},{"productId":"64493","productLogo":"https:\/\/s1.huishoubao.com\/img\/phone\/526772_1602655951462.jpg","productMaxPrice":"409000","productName":"iPhone 12 mini","icon":"","brandId":"2","brandName":"苹果","brandIdV2":"2","classId":"1","className":"手机","activityIcon":"","activityText":"","activityDesc":""},{"productId":"63330","productLogo":"https:\/\/s1.huishoubao.com\/img\/phone\/63330_20191106155429_525.png","productMaxPrice":"388900","productName":"iPhone 11","icon":"","brandId":"2","brandName":"苹果","brandIdV2":"2","classId":"1","className":"手机","activityIcon":"","activityText":"","activityDesc":""},{"productId":"63328","productLogo":"https:\/\/s1.huishoubao.com\/img\/phone\/63328_20191106155004_685.jpg","productMaxPrice":"501900","productName":"iPhone 11 Pro","icon":"","brandId":"2","brandName":"苹果","brandIdV2":"2","classId":"1","className":"手机","activityIcon":"","activityText":"","activityDesc":""},{"productId":"54791","productLogo":"https:\/\/s1.huishoubao.com\/img\/phone\/54791_20180922111425_245.png","productMaxPrice":"237400","productName":"iPhone XR","icon":"","brandId":"2","brandName":"苹果","brandIdV2":"2","classId":"1","className":"手机","activityIcon":"","activityText":"","activityDesc":""},{"productId":"38200","productLogo":"https:\/\/s1.huishoubao.com\/img\/phone\/38200_20191106172157_109.png","productMaxPrice":"122800","productName":"iPhone 8","icon":"","brandId":"2","brandName":"苹果","brandIdV2":"2","classId":"1","className":"手机","activityIcon":"","activityText":"","activityDesc":""},{"productId":"38201","productLogo":"https:\/\/s1.huishoubao.com\/img\/phone\/38201_20191106172137_892.jpg","productMaxPrice":"186900","productName":"iPhone 8 Plus","icon":"","brandId":"2","brandName":"苹果","brandIdV2":"2","classId":"1","className":"手机","activityIcon":"","activityText":"","activityDesc":""},{"productId":"30831","productLogo":"https:\/\/s1.huishoubao.com\/img\/phone\/30831.jpg","productMaxPrice":"72800","productName":"iPhone 7","icon":"","brandId":"2","brandName":"苹果","brandIdV2":"2","classId":"1","className":"手机","activityIcon":"","activityText":"","activityDesc":""},{"productId":"30832","productLogo":"https:\/\/s1.huishoubao.com\/img\/phone\/30832_20191106172219_783.png","productMaxPrice":"104000","productName":"iPhone 7 Plus","icon":"","brandId":"2","brandName":"苹果","brandIdV2":"2","classId":"1","className":"手机","activityIcon":"","activityText":"","activityDesc":""},{"productId":"30748","productLogo":"https:\/\/s1.huishoubao.com\/img\/phone\/30748.png","productMaxPrice":"33400","productName":"iPhone 6","icon":"","brandId":"2","brandName":"苹果","brandIdV2":"2","classId":"1","className":"手机","activityIcon":"","activityText":"","activityDesc":""},{"productId":"65783","productLogo":"https:\/\/s1.huishoubao.com\/img\/phone\/401791_1620972970111.jpg","productMaxPrice":"206900","productName":"华为 P40","icon":"","brandId":"1","brandName":"华为","brandIdV2":"1","classId":"1","className":"手机","activityIcon":"","activityText":"","activityDesc":""},{"productId":"64000","productLogo":"https:\/\/s1.huishoubao.com\/img\/phone\/119144_1585385521386.jpg","productMaxPrice":"286500","productName":"华为 P40（5G）","icon":"","brandId":"1","brandName":"华为","brandIdV2":"1","classId":"1","className":"手机","activityIcon":"","activityText":"","activityDesc":""},{"productId":"64001","productLogo":"https:\/\/s1.huishoubao.com\/img\/phone\/020623_1585385684334.jpg","productMaxPrice":"447500","productName":"华为 P40 Pro（5G）","icon":"","brandId":"1","brandName":"华为","brandIdV2":"1","classId":"1","className":"手机","activityIcon":"","activityText":"","activityDesc":""},{"productId":"64247","productLogo":"https:\/\/s1.huishoubao.com\/img\/phone\/837908_1592201103669.jpg","productMaxPrice":"509300","productName":"华为 P40 Pro+（5G）","icon":"","brandId":"1","brandName":"华为","brandIdV2":"1","classId":"1","className":"手机","activityIcon":"","activityText":"","activityDesc":""},{"productId":"2071","productLogo":"https:\/\/s1.huishoubao.com\/img\/phone\/2071_20180818163852_311.png","productMaxPrice":"6900","productName":"OPPO A57","icon":"","brandId":"5","brandName":"OPPO","brandIdV2":"5","classId":"1","className":"手机","activityIcon":"","activityText":"","activityDesc":""},{"productId":"30742","productLogo":"https:\/\/s1.huishoubao.com\/img\/phone\/30742.jpg","productMaxPrice":"200","productName":"华为 Y300","icon":"","brandId":"1","brandName":"华为","brandIdV2":"1","classId":"1","className":"手机","activityIcon":"","activityText":"","activityDesc":""},{"productId":"30746","productLogo":"https:\/\/s1.huishoubao.com\/img\/phone\/30746.jpg","productMaxPrice":"200","productName":"华为 Y540","icon":"","brandId":"1","brandName":"华为","brandIdV2":"1","classId":"1","className":"手机","activityIcon":"","activityText":"","activityDesc":""},{"productId":"30833","productLogo":"https:\/\/s1.huishoubao.com\/img\/phone\/30833.jpg","productMaxPrice":"57200","productName":"iPhone 6s Plus","icon":"","brandId":"2","brandName":"苹果","brandIdV2":"2","classId":"1","className":"手机","activityIcon":"","activityText":"","activityDesc":""},{"productId":"30749","productLogo":"https:\/\/s1.huishoubao.com\/img\/phone\/30749.jpg","productMaxPrice":"10400","productName":"iPhone 5s","icon":"","brandId":"2","brandName":"苹果","brandIdV2":"2","classId":"1","className":"手机","activityIcon":"","activityText":"","activityDesc":""}],"pageInfo":{"pageIndex":"1","pageSize":"20","total":30,"totalPage":2}},"_errCode":"0","_errStr":"成功"}
    products = {}
    p_list = raw["_data"]["productList"]
    for p in p_list:
        brand_id = p["brandId"]
        product_id = p["productId"]
        p_name = p["productName"]
        print(brand_id,product_id,p_name)


