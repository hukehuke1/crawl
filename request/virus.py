# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     virus.py
   Description : curl提交病毒信息，收集返回值
   Author :       huke
   date：          2018/11/15
-------------------------------------------------
   Change Activity:
                   2018/11/15:
-------------------------------------------------
"""


import pycurl
import os
import json


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


def toString(sh256):
    b = joincontents()
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://192.168.29.112/result?hash='+ sh256)
    c.setopt(c.WRITEDATA, b)
    #c.setopt(pycurl.PROXY, 'http://116.55.77.81:61202')  # 设置代理
    c.setopt(pycurl.CONNECTTIMEOUT, 5)  # 超时时间
    c.perform()
    print(c.getinfo(pycurl.HTTP_CODE)) #  正常访问的话应该返回值是200
    print("----header-----")
    # print(b.getvalue())
    b.display()
    j = json.loads(b.contents)  # 将json对象转换成python对象
    virusName = j['result']['virus_info']['virus_name']
    status = j['result']['status']
    verdict = j['result']['verdict']

    return (virusName,status,verdict)


def file_name(file_dir):   
    fnames = []
    for root, dirs, files in os.walk(file_dir):  
        fnames = fnames + files
        print(root) #当前目录路径  
        print(dirs) #当前路径下所有子目录  
        print(files) #当前路径下所有非目录子文件 
    return fnames


if __name__ == "__main__":
    #获取文件夹下所有文件名
    os.chdir('E:/working/virus')
    print(os.getcwd())
    flist = []  #文件名list 
    flist = file_name('E:/working/virus/virus')

    with open('E:/working/virus/result.txt','w') as fr: # 把输出结果写入文件
        for i in flist:
            virusName,status,verdict = toString(i)
            fr.write('文件hash是%s病毒种类是%s,status是%s,verdict是%s\n'%(i,virusName,status,verdict))
    # sh256 = '421a1592930a07dfe805131d023240fc51b44aa345ab41f72a3ca9360ecadc1e'
    # print('文件hash是%s病毒种类是%s'%(sh256,toString(sh256)))
