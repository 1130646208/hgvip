#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/2/4 12:39
# @Author  : wsx
# @Site    : 
# @File    : save_to_database.py
# @Software: PyCharm

from config import *
from pymongo import MongoClient
import types
from threading import Thread
from crawl_movies import *


class Save:

    def __init__(self, host=MONGO_CLIENT_HOST, port=MONGO_CLIENT_PORT):
        self.client = MongoClient(host, port)

    def check_classes(self):
        db = self.client['hgvip']
        return db.collection_names()

    def save_many_to_mongo(self, data, collection_name='classes', ins=True, db_name='hgvip'):
        # ins为真, 则不判断是否重复, 否则判断是否重复
        try:
            db = self.client[db_name]
            collection = db[collection_name]
            if isinstance(data, types.GeneratorType):
                for each in data:
                    # 如果非空就插入数据库
                    if ins and each:
                        result = collection.insert_one(each)
                        print('Success saved to mongo [%s] [%s]\n' % (result.inserted_id, each))
                    elif each:
                        result = collection.update_one(each, {'$set': each}, True)
                        print(r'Success update:[%s] [%s]' % (result.acknowledged, each))
                    yield each
            else:
                print('Data is not Generator.')
        except Exception as e:
            print(e)
        finally:
            self.client.close()

    def find(self, collection_name, _filter, sort_key, db_name='hgvip'):
        db = self.client[db_name]
        collection = db[collection_name]
        result = collection.find(_filter).sort(sort_key)
        if result:
            return result
        else:
            return None


class Update(Thread):
    def __init__(self, cls_id=10, page=1, queue=None):
        Thread.__init__(self)
        self.queue = queue
        self.cls_id = cls_id
        self.page = page
        self.g = Get()
        self.s = Save()
        self.succeed = 0
        self.failed = 0

    def update_cate(self):
        cates = self.g.get_cate()
        for each in self.s.save_many_to_mongo(cates, collection_name='classes', ins=False):
            print(each)

    def update_class(self):
        success = 0
        fail = 0
        cls_id = self.cls_id
        page = self.page
        print('Updating page %s.\n' % page)
        for each in self.s.save_many_to_mongo(self.g.get_mov_info(cls_id, page), collection_name='class_' + cls_id, ins=True):
            if each:
                success += 1
            else:
                fail += 1
        print('Page %s update ok.\n' % page)
        self.failed = fail
        self.succeed = success
        # 完成后再取出元素
        self.queue.task_done()
        self.queue.get()

    def run(self):
        self.update_class()
