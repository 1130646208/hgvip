#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/2/1 21:24
# @Author  : wsx
# @Site    : 
# @File    : crawl_movies.py
# @Software: PyCharm
import requests
import json
from urllib.parse import urlencode
from requests.exceptions import RequestException
import random

class Get:
    def __init__(self):
        self.start_url = 'https://api888.jiadao.info/home/cls/query2'
        self.cate_detail_url = 'https://api888.jiadao.info/home/clsmov/query?'
        self.m3u8_url = 'https://api888.jiadao.info/mov/browse2?'

    @staticmethod
    def get_page(url):
        """请求url,得到响应文本"""
        headers = {
            'Host': 'api888.jiadao.info',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Referer': 'https://hgvip.app/?pkg=cukepay0001',
            'pkg': 'cukepay0001',
            'Seq': '8f966d17ae1749699c124e1f1ca89662C30mC30mCJ8sC3G',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0',
            'terminal': '4',
            'release': '200',
        }
        ip = ['39.106.223.207:80', '112.195.121.250:9999', '124.239.216.14:8060']
        proxies = {
            "http": "http://" + ip[0],
        }
        try:
            response = requests.get(url, headers=headers, timeout=30, proxies=proxies)
            if response.status_code == 200:
                print('请求成功,耗时:[%s]秒.' % response.elapsed.seconds)
                return response.text
            else:
                print('请求出错啦.代码:[%s]' % response.status_code)
                return None
        except RequestException as e:
            print('请求出错啦.信息:[%s]' % e)
            return None

    def get_cate(self):
        """得到类别名称和类别id"""
        cate_html = self.get_page(self.start_url)
        if cate_html:
            data = json.loads(cate_html)
        else:
            data = None
        if data and 'data' in data.keys():
            cls_info = data['data']
            for each in cls_info:
                yield {
                    '类别': each['clsName'],
                    'clsid': each['id']
                }
        else:
            print('Error in :get_cate')
            yield None

    def get_cate_detail(self, cls_id, pageNo=1, _filter=2, pageSize=13):
        """返回某个类别,某一页的影片json数据"""
        data = {
            'filter': _filter,
            'clsId': cls_id,
            'pageSize': pageSize,
            'pageNo': pageNo,
        }
        para = urlencode(data)
        cate_detail = self.get_page(self.cate_detail_url + para)
        if cate_detail:
            return cate_detail
        else:
            print('Error in :get_cate_detail')
            return None

    def get_page_num(self, cls_id):
        html = self.get_cate_detail(cls_id)
        if html:
            data = json.loads(html)
            return data['pageCount']
        else:
            print('Error in : get_page_num')
            return None

    def get_mov_info(self, cls_id, pageNo):
        """提取某个类别某一页的影片信息"""
        cate_detail = self.get_cate_detail(cls_id, pageNo)
        if cate_detail:
            data = json.loads(cate_detail)
        else:
            data = None
        if data and 'data' in data.keys():
            mov_info = data['data']
            # pageCount = data['pageCount']
            #
            for mov in mov_info:
                _id = mov['id']
                m3u8 = self.get_m3u8(int(_id))
                if m3u8:
                    yield {
                        'count': data['count'],
                        'pageCount': data['pageCount'],
                        'pageSize': data['pageSize'],
                        '_id': _id,
                        'movName': mov['movName'],
                        'actor': m3u8['actor'],
                        'address': m3u8['address'],
                        'gmtCreat': m3u8['gmtCreat'],
                        'loveCnt': m3u8['loveCnt'],
                        'movDesc': m3u8['movDesc'],
                        'movScore': m3u8['movScore'],
                        'movSize': m3u8['movSize'],
                        'strPlayCnt': m3u8['strPlayCnt'],
                        'tags': m3u8['tags'],
                        'mins': mov['mins'],
                        'cover': mov['cover'],
                        # 'playCnt': mov['playCnt'],
                        # 'movSize': mov['movSize'],
                    }
                else:
                    yield None
        else:
            print('Error in :get_mov_info')
            print('Error in cls [%s], page [%s]' % (cls_id, pageNo))
            yield None

    def get_m3u8(self, movId, version='v2'):
        """得到某一影片的m3u8文件"""
        form = {
            'version': version,
            'movId': movId,
        }
        para = urlencode(form)
        html = self.get_page(self.m3u8_url + para)
        if html:
            mov_info = json.loads(html)
            data = mov_info['data']
        else:
            data = None
        if data:
            for each in data[0]['address']:
                data[0]['address'][each] = 'https://h5v.891227.com' + data[0]['address'][each]
            all_info = {
                'actor': data[0]['actor'],
                'address': data[0]['address'],
                'gmtCreat': data[0]['gmtCreate'],
                'loveCnt': data[0]['loveCnt'],
                'movDesc': data[0]['movDesc'],
                'movScore': data[0]['movScore'],
                'movSize': data[0]['movSize'],
                'strPlayCnt': data[0]['strPlayCnt'],
                'tags': data[0]['tags'],
            }
            return all_info
        else:
            print('Error in :get_m3u8')
            print('Error movid:[%s] at[%s]' % (movId, self.m3u8_url + para))
            return None
