#encoding=utf8
##爬虫 抓取头条新闻上的内容
'''
Created on 2017.8.30

@author: huke
'''
import requests
from bs4 import BeautifulSoup
import lxml

Default_Header = {
    'Host':'m.toutiao.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
    }

BASE_URL = 'http://m.toutiao.com/profile'
_session = requests.session()
_session.headers.update(Default_Header)


def getPage(uid):
    pageUrl = BASE_URL +'/' + uid + '/'
    soup = BeautifulSoup(_session.get(pageUrl).content,"lxml")#建立一个soup，用lxml来解析
    userName =getUsername(soup)
    print('用户名是:%s'%(userName))
    followingNum = getFollowingNum(soup) #获取关注数
    print('关注数是:%s'%(followingNum))
    followernum = getFollowernum(soup)  #获取粉丝数
    print('粉丝数是:%s'%(followernum))
##    f = open('list.txt','w',encoding='utf8')
##    f.write(soup.prettify())
##    f.close()


    
def getUsername(soup):#用户名
    return soup.select('#username')[0].string

def getFollowingNum(soup):#获取关注数
    return soup.select('#followingnum')[0].string

def getFollowernum(soup):#获取关注数
    return soup.select('#followernum')[0].string

if __name__ == '__main__':
    uid = '4492956276'
    getPage(uid)
