# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     crawlproxy
   Description :   从抓取高匿代理IP
   Author :       huke
   date：          2018/3/16
-------------------------------------------------
   Change Activity:
                   2018/3/19:
-------------------------------------------------
"""


import requests
from bs4 import BeautifulSoup
import lxml
import time
import io
import pycurl
import threading
from time import ctime, sleep

class joincontents:
    def __init__(self):
        self.contents = ''

    def callback(self, curl):
        self.contents = self.contents + curl.decode('utf-8')

    def display(self):
        print(self.contents)

    def write(self, s):
        self.contents = self.contents + s.decode('utf-8')


Default_Header = {
    'Referer':'http://www.xicidaili.com/',
    'Host':'www.xicidaili.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Accept':'text/css,*/*;q=0.1',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
    }


GAONI_URL = 'http://www.xicidaili.com/nn/'  #国内高匿代理的ip网址
_session = requests.session()
_session.headers.update(Default_Header)
ipList = []  # 用来存放所有ip端口
validipList = []  # 存放验证好的IP
BASE_IP = "111.204.125.218"  # jowto外网IP
validUrl = 'http://httpbin.org/get'  # 验证代理是否可用的外网小网页


def getDomesticIp(url):  # 抓取网页内容
    print(url)
    soup = BeautifulSoup(_session.get(url).content, "lxml")  # 建立一个soup，用lxml来解析
    strip = soup.find_all('tr', 'odd')
    for i in strip:
        analyse(i)
    global ipList
    print(ipList)
    # print(soup.prettify())
    # f = open('s.txt','w',encoding='utf8')
    # f.write(soup.prettify())
    # f.close()


def analyse(soup):  # 解析IP和地址
    # ip= soup.find('td','country').next_element.next_element.next_element.next_element#通过迭代下一个元素，解析出IP地址
    # port = soup.find('td','country').next_element.next_element.next_element.next_element.next_element.next_element.next_element
    global ipList
    s1 = soup.find('td', 'country')  # 定位特定元素
    ip = nextElement(s1, 4)  # ip=迭代4次.next_element
    port = nextElement(s1, 7)  # port=迭代4次.next_element
    # print(ip)
    # print(port)
    ipList.append(str(ip)+":"+str(port))


def nextElement(soup, n):  # 强迫症看n个next_element不顺眼，写一个迭代方法n次执行.next_element
    if n > 1:
        return nextElement(soup.next_element, n-1)
    if n == 1:
        return soup.next_element


def curlValidation(ipList):  # 调用curl验证代理是否可用
    for i in ipList:
        proxyIp = str(i).split(':')[0]  # 把ip+端口截取出IP
        global validipList
        b = joincontents()
        c = pycurl.Curl()
        c.setopt(c.URL, validUrl)
        c.setopt(c.WRITEDATA, b)
        c.setopt(pycurl.PROXY, 'http://116.55.77.81:61202')  # 设置代理
        c.setopt(pycurl.CONNECTTIMEOUT, 10)  # 超时时间
        c.perform()
        print(c.getinfo(pycurl.HTTP_CODE))  # 正常访问的话应该返回值是200
        print("----header-----")
        # print(b.getvalue())
        b.display()
        if b.findproxy(proxyIp) > 0:
            validipList.append(i)  # 把验证过的好用的代理加入到新的list中
            print('代理验证成功')
        elif (b.findproxy(BASE_IP)) > 0:
            print('代理失败,仍然是本机IP')
        else:
            print('连接失败')
        # b = joincontents()
        # c = pycurl.Curl()
        # c.setopt(c.URL, 'http://httpbin.org/get')
        # c.setopt(c.PROXY, i)  # 设置代理
        # c.setopt(c.WRITEFUNCTION, b.callback)
        # c.perform()
        # b.display()


def curlValidationThread(ipList):
    

def curl(desturl, proxyurl):  # curl通过proxyurl代理访问desturl
        b = joincontents()
        c = pycurl.Curl()
        c.setopt(c.URL, desturl)
        c.setopt(c.WRITEDATA, b)
        c.setopt(pycurl.PROXY, proxyurl)  # 设置代理
        c.setopt(pycurl.CONNECTTIMEOUT, 10)  # 超时时间
        c.perform()


if __name__ == '__main__':
    desturl = ''  # 这里输入要测试机器的URL，就是那个放在外网的机器+端口。例如 111.155.116.236:8123
    getDomesticIp(GAONI_URL)  # 抓取IP
    curlValidation(ipList)  # 验证代理是否可用
    for i in validipList:
        curl(i, desturl)   # 利用可用代理列表，执行测试
