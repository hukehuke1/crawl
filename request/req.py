#-*- coding:utf-8 -*-

import requests
import os
url = 'http://192.168.29.99:8080/yunsuo-back/login'
data = {"user":"user","password":"jowto2307","vertify":"666666"}
headers = { "Accept":"text/html,application/xhtml+xml,application/xml;", "Accept-Encoding":"gzip", "Accept-Language":"zh-CN,zh;q=0.8", "Referer":"http://192.168.29.99:8080/yunsuo-back/login/", "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36" }
res1 = requests.post(url, data=data , headers=headers)
#res2 = requests.get(url2, cookies=res1.cookies, headers=headers)
f = open('s.txt','w')
#f.write(str(res1.status_code))
f.write(str(res1.content))
f.close()
