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


class Save:

    def __init__(self, host=MONGO_CLIENT_HOST, port=MONGO_CLIENT_PORT):
        self.host = host
        self.port = port
        self.client = MongoClient(self.host, self.port)

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
                        print('[%s] [%s]' % (result.inserted_id, each))
                    elif each:
                        result = collection.update_one(each, {'$set': each}, True)
                        print(r'success update:[%s], %s\n' % (result.acknowledged, each))
                    yield each
            else:
                print('data is not Generator.')
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
