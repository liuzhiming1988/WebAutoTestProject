#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : baidu_ocr.py
@Author  : liuzhiming
@Time    : 2021/6/13 17:15
"""

from aip import AipOcr
from public import ocr_conf


class BaiduOcr:

    def __init__(self):
        self.client = AipOcr(ocr_conf.APP_ID, ocr_conf.API_KEY, ocr_conf.SECRET_KEY)

    def get_file_content(self, filepath):
        """
        This method is used to read local images, And returns an object
        :param filepath:
        :return:
        """
        with open(filepath, "rb") as fp:
            return fp.read()

    def get_ocr_data(self, filepath):
        """
        This method is used to identify local images
        :param filepath:
        :return:
        """
        img = self.get_file_content(filepath)
        data = self.client.basicAccurate(img)
        # print(data["words_result"])
        res_data = ""
        # 将识别到的每行文字进行拼接
        for x in data["words_result"]:
            res_data+="{}\n".format(x["words"])
        print(res_data.strip())
        return res_data.strip()


if __name__ == '__main__':
    path = "d:\\55.jpg"
    BaiduOcr().get_ocr_data(path)
