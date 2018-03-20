# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     post提交网络访问控制
   Description :
   Author :       huke
   date：          2018/3/9
-------------------------------------------------
   Change Activity:
                   2018/3/9:
-------------------------------------------------
"""


import requests
#from bs4 import BeautifulSoup
import urllib.request
import threading
from time import ctime, sleep
import lxml
import time
import socket


Default_Header = {
    'Referer':'http://192.168.29.100/bbs/forum.php',
    'Host':'192.168.29.100',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    #'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
    }

#BASE_URL = 'http://192.168.29.100/bbs/forum.php'
_session = requests.session()
_session.headers.update(Default_Header)


if __name__ == '__main__':
    pass