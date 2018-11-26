# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     zhengwu.py
   Description :
   Author :       huke
   date：          2018/5/16
-------------------------------------------------
   Change Activity:
                   2018/5/16:
-------------------------------------------------
"""
import requests
from bs4 import BeautifulSoup
import lxml


Header = {
    'Referer':'http://http://zhengwutoutiao.com',
    'Host':'zhengwutoutiao.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    }

_session = requests.session()
_session.headers.update(Header)


def getPage():
    pageUrl = 'http://zhengwutoutiao.com/ght/files?id=d1b8b6d9bf04461396267adca2c21f54'
    #cookies = dict(JSESSIONID='540F8D20FCBA21659385C2E06F9CA8AE')
    soup = BeautifulSoup(_session.get(pageUrl).content, "lxml")
    urlList = []




if __name__ == '__main__':
    getPage()