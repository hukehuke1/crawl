# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     pycurl
   Description :
   Author :       huke
   date：          2018/3/20
-------------------------------------------------
   Change Activity:
                   2018/3/20:
-------------------------------------------------
"""


import pycurl
import io

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


def toString():
    b = joincontents()
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://httpbin.org/get')
    c.setopt(c.WRITEDATA, b)
    #c.setopt(pycurl.PROXY, 'http://116.55.77.81:61202')  # 设置代理
    c.setopt(pycurl.CONNECTTIMEOUT, 5)  # 超时时间
    c.perform()
    print(c.getinfo(pycurl.HTTP_CODE)) #  正常访问的话应该返回值是200
    print("----header-----")
    # print(b.getvalue())
    b.display()
    if b.findproxy('116.55.77.81') > 0:
        print('代理验证成功')
    elif (b.findproxy('111.204.125.218')) > 0:
        print('代理失败')
    else:
        print('连接失败')
    print(b.findproxy('116.55.77.81'))
    print(b.findproxy('111.204.125.218'))


def toCallBack():
    content = joincontents()
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://httpbin.org/get')
    c.setopt(c.WRITEFUNCTION, content.callback)
    c.perform()
    content.display()
    c.close()


if __name__ == "__main__":
    toString()
    # toCallBack()

