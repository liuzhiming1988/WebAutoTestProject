#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : my_exception.py
@Author  : liuzhiming
@Time    : 2021/11/9 11:56
"""


class TooLongStringError(Exception):

    def __init__(self, length):
        self.length = length

    def __str__(self):
        message = "长度为{},已超过最大限制".format(self.length)
        return message


if __name__ == '__main__':
    def verfiy_length(words):
        if len(words) > 10:
            raise TooLongStringError(len(words))
        else:
            print(words)

    try:
        verfiy_length("fdshakhfksdffdsfasdf")
    except Exception as ec:
        print("{}: {}".format(repr(ec), ec.__str__()))
