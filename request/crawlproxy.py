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
import sys
import os


class joincontents:
    def __init__(self):
        self.contents = ''

    def callback(self, curl):
        self.contents = self.contents + curl.decode('utf-8')

    def display(self):
        print(self.contents)

    def write(self, s):
        self.contents = self.contents + s.decode('utf-8')

    def findproxy(self, proxy):
        return self.contents.find(proxy)


Default_Header = {
    'Referer':'http://www.xicidaili.com/',
    'Host':'www.xicidaili.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Accept':'text/css,*/*;q=0.1',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
    }
Foreign_Header = {
    'Referer':'http://www.data5u.com/free/gwpt/index.shtml',
    'Host':'www.data5u.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Accept':'text/css,*/*;q=0.1',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
    }
Foreign_Header2 = {
    'Referer':'www.yun-daili.com/free.asp?stype=3&page=',
    'Host':'www.yun-daili.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Accept':'text/css,*/*;q=0.1',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
    }

GAONI_URL = 'http://www.xicidaili.com/nn/'  # 国内高匿代理的ip网址
GuowaiGaoni_URL = "http://www.data5u.com/free/gwgn/index.shtml"  # 国外高匿
GuowaiGaoni_URL2 = "http://www.yun-daili.com/free.asp?stype=3&page="   # 国外高匿

_session = requests.session()
_session.headers.update(Default_Header)
ipList = []  # 用来存放所有ip端口
validipList = []  # 存放验证好的IP
BASE_IP = "111.204.125.218"  # jowto外网IP
validUrl = 'http://httpbin.org/get'  # 验证代理是否可用的外网小网页


def getDomesticIp(url):  # 抓取国内代理ip网页内容
    print(url)
    soup = BeautifulSoup(_session.get(url).content, "lxml")  # 建立一个soup，用lxml来解析
    strip = soup.find_all('tr', 'odd')
    for i in strip:
        analyse(i)
    #global ipList
    # print("------全部代理列表--------")
    # print(ipList)
    # print(len(ipList))
    # print(soup.prettify())
    # f = open('s.txt','w',encoding='utf8')
    # f.write(soup.prettify())
    # f.close()


def getForeignIp(url):  # 抓取国外代理ip网页内容
    print(url)
    _session2 = requests.session()
    _session2.headers.update(Foreign_Header2)
    soup = BeautifulSoup(_session2.get(url).content, "lxml")  # 建立一个soup，用lxml来解析
    try:
        soup = BeautifulSoup(_session2.get("http://www.yun-daili.com/free.asp?stype=3&page=1").content, "lxml")
    except e:
        print(e)
    strip = soup.find_all("ul", class_='l2')
    for i in strip:
        analyseForeign(i)


def analyseForeign(soup):  # 解析国外ip和端口
    global ipList
    ip = soup.find('li').string  # 定位国外ip地址
    port = soup.find(class_="port").string  # 定位国外端口位置
    print(ip)
    print(port)
    ipList.append(str(ip) + ":" + str(port))
    ipList = list(set(ipList))


def getForeignIp2(url):  # 抓取国外代理ip网页内容
    print(url)
    _session2 = requests.session()
    _session2.headers.update(Foreign_Header2)
    soup = BeautifulSoup(_session2.get(url).content, "lxml")  # 建立一个soup，用lxml来解析
    strip = soup.find_all('tr', 'odd')
    for i in strip:
        analyseForeign2(i)


def analyseForeign2(soup):  # 解析国外ip和端口
    global ipList
    ip = soup.find(class_="style1").string  # 定位国外ip地址
    port = soup.find(class_="style2").string   # 定位国外端口位置
    print(ip)
    print(port)
    ipList.append(str(ip) + ":" + str(port))
    ipList = list(set(ipList))


# def analyseForeign(soup):  # 解析国外ip和端口
#     global ipList
#     ip = soup.find('li').string  # 定位国外ip地址
#     port = soup.find(class_="port").string  # 定位国外端口位置
#     print(ip)
#     print(port)
#     ipList.append(str(ip) + ":" + str(port))



def analyse(soup):  # 解析国内IP和端口
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
        c.setopt(pycurl.PROXY, str(i))  # 设置代理
        #c.setopt(pycurl.PROXY, 'http://116.55.77.81:61202')  # 测试用设置代理
        c.setopt(pycurl.CONNECTTIMEOUT, 10)  # 超时时间
        c.perform()
        print(c.getinfo(pycurl.HTTP_CODE))  # 正常访问的话应该返回值是200
        print("----WRITEDATA-----")
        print(proxyIp)
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


def curlValid(desturl, proxyurl):  # 单条调用curl验证代理是否可用
    proxyIp = proxyurl.split(':')[0]  # 把ip+端口截取出IP
    global validipList
    b = joincontents()
    c = pycurl.Curl()
    c.setopt(c.URL, desturl)
    c.setopt(c.WRITEDATA, b)
    c.setopt(pycurl.PROXY, proxyurl)  # 设置代理
    # c.setopt(pycurl.PROXY, 'http://116.55.77.81:61202')  # 测试用设置代理
    c.setopt(pycurl.CONNECTTIMEOUT, 10)  # 超时时间
    # c.perform()  # 直接访问，不try except
    print("————代理验证")
    print(proxyurl)
    try:
        c.perform()
        print(proxyurl+"代理连接成功")
        if b.findproxy(proxyIp) > 0:
            validipList.append(proxyurl)  # 把验证过的好用的代理url加入到新的list中
            b.display()
            print('代理验证成功')
        elif (b.findproxy(BASE_IP)) > 0:
            print('代理失败,仍然是本机IP')
        else:
            print('连接失败')
    except pycurl.error:
        print(proxyurl+"代理连接失败")
    # print(c.getinfo(pycurl.HTTP_CODE))  # 正常访问的话应该返回值是200
    # print("--------HTTP请求返回内容----------")
    # b.display()



def curlValidationThread(ipList):
    threads = []
    for i in ipList:
        ti = threading.Thread(target=curlValid, args=(validUrl, str(i)))
        threads.append(ti)
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()#在子线程完成运行之前，这个子线程的父线程将一直被阻塞。
    print("验证完毕")


def curl(desturl, proxyurl):  # 单条curl通过proxyurl代理访问desturl

    b = joincontents()
    c = pycurl.Curl()
    c.setopt(c.URL, desturl)
    c.setopt(c.WRITEDATA, b)
    c.setopt(pycurl.PROXY, proxyurl)  # 设置代理
    c.setopt(pycurl.CONNECTTIMEOUT, 10)  # 超时时间
    try:
        c.perform()
    except pycurl.error:
        print(desturl)
        print(proxyurl)
        print("连接失败")
        return
    print(desturl)
    print(proxyurl)
    print("测试成功")
    b.display()
    c.close()


def curlTest(desturl, validipList):  # curl通过validipList代理访问destPort
    threads = []
    for i in validipList:
        ti = threading.Thread(target=curl, args=(desturl, str(i)))
        threads.append(ti)
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()  # 在子线程完成运行之前，这个子线程的父线程将一直被阻塞。


def writeiptofile(name):  # 把可用的代理ip存到txt文件中
    global validipList
    f = open(name, 'w+')
    for i in validipList:
        f.write(i+'\n')
    f.close()
    print("验证好的ip地址已保存,地址为"+os.getcwd()+name)


def setdefault():  # 执行脚本的时候不带参数时用默认值。
    if len(sys.argv) == 4:  # 带参数
        if sys.argv[3] != "1" and sys.argv[3] != "2" and sys.argv[3] != "3" and code != "4" and code != "5" and code != "6":
            print("模式输入错误，请重新执行")
            sys.exit()
        return sys.argv[1], sys.argv[2], sys.argv[3]
    else:   # 不带参数
        code = input("请输入想要执行的类型\n"
                  " 1 只执行国内网站爬虫脚本\n"
                  " 2 执行国内网站爬虫脚本+单次运行网络访问控制脚本\n"
                  " 3 每隔10分钟执行国内网站爬虫脚本，一直循环运行网络访问控制脚本\n"
                  " 4 只执行国外网站爬虫脚本\n"
                  " 5 执行国外网站爬虫脚本+单次运行网络访问控制脚本\n"
                  " 6 每隔10分钟执行国外网站爬虫脚本，一直循环运行网络访问控制脚本\n"
                  )
        if code != "1" and code != "2" and code != "3" and code != "4" and code != "5" and code != "6":
            print("模式输入错误，请重新执行")
            sys.exit()
        return "http://httpbin.org/get", "http://httpbin.org/get", code  # 这里输入外网机器的默认值  前面为ip ，后面为 ip:端口


if __name__ == '__main__':
    destUrl, destPort, code = setdefault()  # 被测网站ip 被测网站ip:端口 测试类型
    if code =="1":  # 只执行国内网站爬虫脚本
        for i in range(1, 11):  # 抓取前11页的代理IP地址
            getDomesticIp(GAONI_URL+str(i))
        #  getDomesticIp(GAONI_URL)  # 抓取IP
        curlValidationThread(ipList)  # 验证代理是否可用
        print("------可用代理列表--------")
        print(validipList)
        writeiptofile("validGuoneiProxy.txt")
    elif code == "2":  # 执行国内网站爬虫脚本+单次运行网络访问控制脚本
        for i in range(1, 11):  # 抓取前11页的代理IP地址
            getDomesticIp(GAONI_URL+str(i))
        #  getDomesticIp(GAONI_URL)  # 抓取IP
        curlValidationThread(ipList)  # 验证代理是否可用
        print("------可用代理列表--------")
        print(validipList)
        writeiptofile("validGuoneiProxy.txt")
        curlTest(destPort, validipList)
    elif code == "3":  # 每隔10分钟执行国内网站爬虫脚本，一直循环运行网络访问控制脚本
        pass
    elif code == "4":
        for i in range(1, 5):  # 抓取前5页的代理IP地址
            getForeignIp2(GuowaiGaoni_URL2 + str(i))
        print(ipList)
        curlValidationThread(ipList)  # 验证代理是否可用
        print("------可用代理列表--------")
        print(validipList)
        writeiptofile("validGuowaiProxy.txt")
    elif code == "5":
        pass
    elif code == "6":
        pass
    sys.exit()


    # print(sys.argv[0])
    # print(sys.argv[1])
    # for i in validipList:
    #     curl(i, desturl)   # 利用可用代理列表，执行测试
