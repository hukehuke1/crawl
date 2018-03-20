#encoding=utf8
##按照一定频率访问特定网站
'''
Created on 2018.3.06

@author: huke
'''
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

def getpage(url,x):
    pageUrl = url;
#soup = BeautifulSoup(_session.get(pageUrl).content, "lxml")#考虑默认py环境没有BS4
    try:
        req = urllib.request.Request(url, headers=Default_Header)
        res = urllib.request.urlopen(req,timeout=10)  # 用urllib.request发post请求
        print("访问网站的URL:", url)
    except urllib.request.URLError as e:
    #except Exception as e:
        print(type(e))
        print(e)

    # f = open('%s.txt'%(str(x)), 'w', encoding='utf8')
    # f.write(soup.prettify())
    # f.close()  #把post结果输出文件，检测是否请求成功

def main(url,times,sec):
    print('starting at:', ctime())
    threads = []
    for x in range(0, int(times)):
        t = threading.Thread(target=getpage, args=(url, x))
        threads.append(t)
    for t in threads:
        t.setDaemon(True)
        t.start()
        time.sleep(int(sec))
        print(t , ctime())
    t.join()#在子线程完成运行之前，这个子线程的父线程将一直被阻塞。
    print("访问结束")


if __name__ == '__main__':
    times = input("想要执行的次数（默认为10次）:")
    if not times.strip():
        times = int(10)#默认值10
    sec = input("想要延迟的时间（默认为3秒）:")
    if not sec.strip():
        sec = int(3)#默认3次
    print("执行:"+str(times)+"次，延迟"+str(sec)+"秒")
    url = 'http://192.168.29.100/bbs/forum.php'#URL
    main(url,times,sec)
    #getpage(BASE_URL,10)
#    for i in range(1,38):
#        getPage(str(i*35))

#f = open('s.txt','w')
#f.open('s.txt','w',encoding='utf8')
#f.write(soup.prettify())
#f.close()
