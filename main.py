#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/2/4 15:28
# @Author  : wsx
# @Site    : 
# @File    : main.py
# @Software: PyCharm
from crawl_movies import Get
from save_to_database import Save
import pprint
from multiprocessing import Pool


def update_movie(page, cls_id):
    g = Get()
    s = Save()
    print('updating page', page)
    for each in s.save_many_to_mongo(g.get_mov_info(cls_id, page), collection_name='class_' + cls_id, ins=True):
        print(each)
    print('类别更新完成.\n')


def update_cate():
    g = Get()
    s = Save()
    cates = g.get_cate()
    for cate in s.save_many_to_mongo(cates, collection_name='classes', ins=False):
        pass


def test(a):
    print('page', a)


if __name__ == '__main__':
    g = Get()
    s = Save()
    pool = Pool(10)
    update_cate()
    # for each in s.find('classes', {'clsid': {'$gt': 1}}, 'clsid'):
    #     pprint.pprint(each)
    cls_id = input('请输入类别id:')
    page_num = g.get_page_num(cls_id)
    print('共%s页.' % page_num)
    for page in range(page_num):
        update_movie(page+1, cls_id)

