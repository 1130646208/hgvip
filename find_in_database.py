#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/2/10 15:43
# @Author  : wsx
# @Site    : 
# @File    : find_in_database.py
# @Software: PyCharm

from pymongo import MongoClient
from config import *
import re


class Find:
    def __init__(self, db_name, collection_name, host=MONGO_CLIENT_HOST, port=MONGO_CLIENT_PORT):
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.result_num = 0
        self.map = {
            '名称': 'movName',
            '描述': 'movDesc',
            '喜欢': 'loveCnt',
            '评分': 'movScore',
            '时长': 'mins',
            '大小': 'movSize.720P',
            '演员': 'actor'
        }

    def find_in_what(self, keyword, inwhat='名称', sortby='评分',exact=False):
        csr = self.collection.find({self.map[inwhat]: re.compile(keyword)}, \
                                   {'count': 0, 'pageCount': 0, 'pageSize': 0, 'cover': 0}).sort(self.map[sortby], -1)
        result = []
        if csr:
            for each in csr:
                result.append(each)
            self.result_num = csr.retrieved
            return result
        else:
            return None

    def find_tags(self, keyword, sortby='评分'):
        csr = self.collection.find({'$or': [{'tags.0.name': keyword}, {'tags.1.name': keyword}, {'tags.2.name': keyword},\
                                            {'tags.3.name': keyword}, {'tags.4.name': keyword}, {'tags.5.name': keyword},\
                                            {'tags.6.name': keyword}, {'tags.7.name': keyword}, {'tags.8.name': keyword}]},\
                                   {'count': 0, 'pageCount': 0, 'pageSize': 0, 'cover': 0}).sort(self.map[sortby], -1)
        result = []
        if csr:
            for each in csr:
                result.append(each)
            self.result_num = csr.retrieved
            return result
        else:
            return None

    # 返回数据库类别id和类别名称
    def look_classes(self):
        print('类别信息:')
        print('---------------------------------------------------')
        classes = self.db['classes']
        for each in classes.find({}, {'_id': 0}):
            print(each)
        print('---------------------------------------------------')

    def raise_m3u8(self, mov_id, mov_solution='480P'):
        if self.collection.find_one({'_id': mov_id}):
            return self.collection.find_one({'_id': mov_id})['address'][mov_solution]
        else:
            return None
