#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/2/4 15:28
# @Author  : wsx
# @Site    : 
# @File    : main.py
# @Software: PyCharm
from find_in_database import *


def main1():
    finder = Find('hgvip', 'class_10')
    for each in finder.find_in_what('自拍', what='描述', sortby='评分'):
        print(each)


def main2():
    finder = Find('hgvip', 'class_10')
    for each in finder.find_tags('性爱自拍'):
        print(each)


if __name__ == '__main__':
    main2()

