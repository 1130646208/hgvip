#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/2/4 15:28
# @Author  : wsx
# @desc    : 交互式, 先显示数据库信息, 再接受用户选择, 根据用户选择的影片ID返回链接
# @File    : main.py
# @Software: PyCharm

from find_in_database import *


def start_enjoy(key, clsid, inwhat, sortby):
    finder = Find('hgvip', 'class_'+clsid)
    for each in finder.find_in_what(key, inwhat=inwhat, sortby=sortby):
        try:
            print(' [<%s>电影名称]: %s\n [描述]: %s\n [喜欢: %s, 评分: %s, 时长: %s]\n [大小(720P): %s, (480P): %s, (360P): %s]\n [标签]: %s'
                  % (each['_id'], each['movName'], each['movDesc'], each['loveCnt'], each['movScore'], each['mins'], each['movSize']['720P'], each['movSize']['480P'], each['movSize']['360P'],\
                     each['tags']))
            print('---------------------------------------------------------------------------------------------------')
        except KeyError as e:
            if each['movSize'].keys():
                size_key = list(each['movSize'].keys())[0]
            print('*[<%s>电影名称]: %s\n [描述]: %s\n [喜欢: %s, 评分: %s, 时长: %s]\n [大小(%s): %s]\n [标签]: %s'
                  % (each['_id'], each['movName'], each['movDesc'], each['loveCnt'], each['movScore'], each['mins'], size_key, each['movSize'][size_key], each['tags']))
            print('---------------------------------------------------------------------------------------------------')
    print('#搜索完成, 共找到数据[%s]条' % finder.result_num)


if __name__ == '__main__':
    finder0 = Find('hgvip', 'classes')
    finder0.look_classes()
    while True:
        clsid = input('要查询哪个类别ID?\nID:')
        finder1 = Find('hgvip', 'class_'+clsid)
        """
        搜索域和排序方式可以选以下项目:
        名称, 描述, 喜欢, 评分, 时长, 大小
        """
        key = input('请输入搜索关键词:')
        """     关键词↓   搜索域↓    ↓排序方式(由大到小)"""
        start_enjoy(key, clsid, '描述', '评分')
        _id = int(input('请输入要下载的影片ID:'))
        _solution = input('请输入要下载的影片清晰度(默认480P):')
        if _solution:
            url = finder1.raise_m3u8(_id, _solution)
        else:
            url = finder1.raise_m3u8(_id)
        if _id and url:
            print(url)
        else:
            print('找不到影片...')
        a = input('\n****************\n*按任意键继续...*\n****************\n')
        if a:
            print('正在退出...')
            break

