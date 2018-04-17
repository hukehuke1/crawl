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
import http.cookiejar

Header = {
    'Referer':'http://192.168.20.21/index',
    'Host':'192.168.20.21',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Content-Type':'application/json',
    }

HeaderLogin8187 = {
    # 'Referer':'http://192.168.8.187/login',
    'Host':'192.168.8.187',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Content-Type':'application/x-www-form-urlencoded',
    'Content-Length': '77',
    }

HeaderLogin2021 = {
    'Host':'192.168.20.21',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Content-Type':'application/x-www-form-urlencoded',
    'Content-Length': '77',
    }


# postdata = {
#     'username': 'exhooker', #填写帐号
#     'password': 'Jowto1234',  #填写密码
# }

postdata = {
    'username': 'exhooker', #填写帐号
    'password': 'Jowto1234',  #填写密码
}

def newNetControl1():       #使用既有的cookie来发送一条请求
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



def getNewCookie2021():     #使用用户名密码登录，得到cookie 保存到cookie文件中
    _session = requests.session()
    _session.cookies = http.cookiejar.LWPCookieJar("cookie")  #登录之后把cookie存到cookie文件中
    _session.headers.update(HeaderLogin2021)
    url = "http://192.168.20.21/login"
    #cookies = dict(menuIndex='0')
    #payload = {"username":"CFHQwNCXVI6hAzw3sk8Fmg%3D%3D","password":"ETtrJvYFVGNbEMlm%2F3Dz5w%3D%3D"}
    soup = BeautifulSoup(_session.post(url,data=postdata).content, "lxml") 
    #cookie = http.cookiejar.CookieJar()
    _session.cookies.save(ignore_discard=True, ignore_expires=True)  #忽略关闭浏览器丢失，忽略失效
    f = open('s.txt','w',encoding='utf8')
    f.write(soup.prettify())
    f.close()
    print(soup.prettify())


def newNetControl2021():       #使用保存好的cookie来发送一条请求
    _session = requests.session()
    _session.headers.update(Header)
    url = "http://192.168.20.21/networkAccessControl/add"
    cookies = http.cookiejar.LWPCookieJar('cookie')   #读取文件中保存的cookie
    print("--------------")
    print(cookies)
    payload = {"accessType":"出站","strategyName":"out test29.100","srcAddresses":[{"addressDirection":0,"addressInfo":"192.168.29.100","addressType":0}],"destAddresses":[{"addressDirection":1,"addressInfo":"192.168.1.103","addressType":0}],"destPort":"80","srcRole":{},"destRole":{},"srcTags":[],"destTags":[]}
    #r = requests.post(url, cookies=cookies,data=json.dumps(payload))
    soup = BeautifulSoup(_session.post(url, cookies=cookies,data=json.dumps(payload)).content, "lxml")
    f = open('s.txt','w',encoding='utf8')
    f.write(soup.prettify())
    f.close()
    print(os.getcwd())
    print(soup.prettify())

def getNewCookie8187():     #使用用户名密码登录，得到cookie 保存到cookie文件中
    _session = requests.session()
    _session.cookies = http.cookiejar.LWPCookieJar("cookie")  #登录之后把cookie存到cookie文件中
    _session.headers.update(HeaderLogin8187)
    url = "http://192.168.8.187/login"
    cookies = dict(menuIndex='0',JSESSIONID='108F29124C4248447732A7F77C6FC49D')
    #payload = {"username":"CFHQwNCXVI6hAzw3sk8Fmg%3D%3D","password":"ETtrJvYFVGNbEMlm%2F3Dz5w%3D%3D"}
    soup = BeautifulSoup(_session.post(url,cookies=cookies,data=postdata).content, "lxml") 
    #cookie = http.cookiejar.CookieJar()
    _session.cookies.save(ignore_discard=True, ignore_expires=True)  #忽略关闭浏览器丢失，忽略失效
    # f = open('s.txt','w',encoding='utf8')
    # f.write(soup.prettify())
    # f.close()
    print(soup.prettify())


def newNetControl(url,payload):       #使用保存好的cookie来发送一条请求
    _session = requests.session()
    _session.headers.update(Header)
    _session.cookies = http.cookiejar.LWPCookieJar("cookie")
    _session.cookies.load(filename='cookie',ignore_discard=True,ignore_expires=True)   #读取文件中保存的cookie
    cookies = dict(menuIndex='2-0', JSESSIONID='108F29124C4248447732A7F77C6FC49D')
    for i in _session.cookies:
        if i.name == 'y':
            cookies['y']=i.value
        print(cookies)
    # _session.cookies["y"]
    #cookies = dict(menuIndex='2-0', JSESSIONID='108F29124C4248447732A7F77C6FC49D',y='18C7A058A059C63EB0C8C89059EE2A21D16083E06358090031ED052737F6ED0C3AC01FB151DA0CE6')
    print("--------------")
    soup = BeautifulSoup(_session.post(url, cookies=cookies,data=json.dumps(payload)).content, "lxml")
    f = open('s.txt','w',encoding='utf8')
    f.write(soup.prettify())
    f.close()
    print(os.getcwd())
    print(soup.prettify())


def getJsessionID():
    s=requests.session()
    centerUrl="http://192.168.8.187/login"
    s.headers.update(HeaderLogin8187)
    r=s.get(centerUrl,verify=False)
    jsession = r.headers  #获取需要的headers
    #jsession = r.headers['Set-Cookie']   #从cookies里读取jsessionid
    print(jsession)
    #logUrl='https://www.haoyisoft.com:8443/CustomerCenter/login.do'+';jsessionid='+jid
    #l=s.post(logUrl,verify=False,data=d)


if __name__ == '__main__':
    #getJsessionID()
    #getNewCookie8187()
    url = "http://192.168.8.187/networkAccessControl/add"
    f = open('netcontrol.txt','r',encoding='utf8')
    line = f.readline
    while line:
        print(line,end='')
        line = f.readline()
        try:
            payload = eval(line.strip())
            newNetControl(url,payload)
        except Exception as ex:
            print(ex)
    f.close()
    payload = {"accessType":"出站","strategyName":"out python29.100","srcAddresses":[{"addressDirection":0,"addressInfo":"192.168.29.100","addressType":0}],"destAddresses":[{"addressDirection":1,"addressInfo":"192.168.1.103","addressType":0}],"destPort":"80","srcRole":{},"destRole":{},"srcTags":[],"destTags":[]}
    print(payload)
    #newNetControl(url,payload)
    print('添加完成，请查看网络访问控制规则')