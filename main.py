#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/2/4 15:28
# @Author  : wsx
# @desc    : 在数据库中搜索
# @File    : main.py
# @Software: PyCharm

from find_in_database import *


def start_enjoy(key, inwhat, sortby):
    finder = Find('hgvip', 'class_10')
    for each in finder.find_in_what(key, inwhat=inwhat, sortby=sortby):
        try:
            print(' [<%s>电影名称]: %s\n [描述]: %s\n [👍: %s, 评分: %s, 时长: %s]\n [大小(720P): %s, (480P): %s, (360P): %s]\n [标签]: %s'
                  % (each['_id'], each['movName'], each['movDesc'], each['loveCnt'], each['movScore'], each['mins'], each['movSize']['720P'], each['movSize']['480P'], each['movSize']['360P'],\
                     each['tags']))
            print('---------------------------------------------------------------------------------------------------')
        except KeyError as e:
            if each['movSize'].keys():
                size_key = list(each['movSize'].keys())[0]
            print('*[<%s>电影名称]: %s\n [描述]: %s\n [👍: %s, 评分: %s, 时长: %s]\n [大小(%s): %s]\n [标签]: %s'
                  % (each['_id'], each['movName'], each['movDesc'], each['loveCnt'], each['movScore'], each['mins'], size_key, each['movSize'][size_key], each['tags']))
            print('---------------------------------------------------------------------------------------------------')
    print('#搜索完成, 共找到数据[%s]条' % finder.result_num)


def main2():
    finder = Find('hgvip', 'class_10')
    for each in finder.find_tags('', sortby=''):
        print(each)


if __name__ == '__main__':
    """
    搜索域和排序方式可以选以下项目:
    名称, 描述, 喜欢, 评分, 时长, 大小
    """
    word = input('请输入搜索关键词:')
    """     关键词↓   搜索域↓    ↓排序方式(由大到小)"""
    start_enjoy(word, '描述', '评分')

