# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     netcontrol
   Description :
   Author :       huke
   date：          2018/3/20
-------------------------------------------------
   Change Activity:
                   2018/3/20:
-------------------------------------------------
"""
import sys
import requests
from bs4 import BeautifulSoup
import lxml
import json
import os

Header = {
    'Referer':'http://192.168.8.187/index?37f520900f4d69a380e53b785b22d463',
    'Host':'192.168.8.187',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Content-Type':'application/json',

    }

BCOOKIES = {
    "menuIndex": "2-0",
    "JSESSIONID": "EDB04212BB71688FFE8C4EC5FE2CE10F",
    "y": "BA2A3304ECAD3B24F74E1B4DF8ECE399FFB3563B351389C03C4EAAAA7D430E5AB86B63E299B3C7E6"
}


if __name__ == '__main__':
    _session = requests.session()
    _session.headers.update(Header)
    url = "http://192.168.8.187/networkAccessControl/add"
    cookies = dict(menuIndex='2-0', JSESSIONID='EDB04212BB71688FFE8C4EC5FE2CE10F',y='B920F1E29B783E091030E2AAA2FF66E2C8DFBE897F574611864028FF14ECBEF09333D7EBA5902DDA')
    payload = {"accessType":"出站","strategyName":"out test29.100","srcAddresses":[{"addressDirection":0,"addressInfo":"192.168.29.100","addressType":0}],"destAddresses":[{"addressDirection":1,"addressInfo":"192.168.1.103","addressType":0}],"destPort":"80","srcRole":{},"destRole":{},"srcTags":[],"destTags":[]}
    #r = requests.post(url, cookies=cookies,data=json.dumps(payload))
    soup = BeautifulSoup(_session.post(url, cookies=cookies,data=json.dumps(payload)).content, "lxml")
    f = open('s.txt','w',encoding='utf8')
    f.write(soup.prettify())
    f.close()
    print(os.getcwd())
    print(soup.prettify())