#encoding=utf8
##爬虫 抓取网易云音乐上所有歌单，然后按照播放次数排序，并输出到文件
'''
Created on 2017.8.30

@author: huke
'''
import requests
from bs4 import BeautifulSoup
import lxml
import time

Default_Header = {
    'Referer':'http://music.163.com/',
    'Host':'music.163.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    #'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
    }

BASE_URL = 'http://music.163.com'
_session = requests.session()
_session.headers.update(Default_Header)
dic = {}
dicSong = {}
dicCount = {}
maxOffset = None

def getPage(pageIndex):
    pageUrl = 'http://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset='+pageIndex
    print('正在获取第%s页的数据'%(pageIndex))
    time.sleep(3)
    soup = BeautifulSoup(_session.get(pageUrl).content, "lxml")
    songList = soup.findAll('a',attrs = {'class':'tit f-thide s-fc0'})
    global maxOffset
    if maxOffset is None:
        getMaxList(soup)#第一次抓取歌单的时候，获取总页数
    else:
        print('已经获得maxOffset')
    #else:
    #    for x in range(35,maxOffset+1,35):
    #        getPage(x)#根据总页数，遍历所有歌单
    
    #f = open('s.txt','w',encoding='utf8')
    #f.write(soup.prettify())
    #f.close()
    for i in songList:
        #print(i['href']) #取到的是playListid
        getPlayList(i['href'])
        #print(i['title']) #取到的是歌单名

def getPlayList(playListId): #用取到的歌单ID搜索歌单播放次数
    playListUrl = BASE_URL + playListId
    #playListUrl = BASE_URL +"/playlist?id=875778492"
    soup = BeautifulSoup(_session.get(playListUrl).content, "lxml")#建立一个soup，用lxml来解析
    songList = soup.find('h2',attrs = {'class':'f-ff2 f-brk'})#检索到歌单名对应行
    print('歌单名是：%s'%(songList.string))
    songCount = soup.find('strong')
    print('播放次数是：%s'%(songCount.string))
    global dic
    dic[songList.string] = songCount.string #按照歌单名+歌单播放次数保存
    global dicSong
    dicSong[playListId] = songList.string #按照歌单ID+歌单名
    global dicCount
    dicCount[playListId] = songCount.string #按照歌单ID+歌单播放次数

def getMaxList(soup):
    maxList = soup.findAll('a',attrs = {'zpgi'})
    page = maxList[len(maxList)-1].string #获取页数
    global maxOffset
    maxOffset = (int(page)-1)*35
    return maxOffset
##    f = open('list.txt','w',encoding='utf8')
##    f.write(soup.prettify())
##    f.close()
    
    

if __name__ == '__main__':
    getPage(str(1))
    print('maxOffset是:%s'%(maxOffset))
    for x in range(35,maxOffset+1,35):
        getPage(str(x))#根据总页数，遍历所有歌单
    #getPlayList("/playlist?id=875778492")
    #getPlayList('/playlist?id=798022381')
    #print(sorted(dic.items(),key=lambda d:int(d[1]), reverse=True))#按照value的降序排序
    
    f = open('sort.txt','w',encoding = 'utf8')
    for key,value in sorted(dicCount.items(),key=lambda d:int(d[1]), reverse=True):
        print('歌曲链接是：http://music.163.com%s'%(key),'播放次数是：%s'%(value),'歌单名是:%s'%(dicSong[key]))
        f.writelines('歌曲链接是：http://music.163.com%s'%(key)+'播放次数是：%s'%(value)+'歌单名是:%s'%(dicSong[key])+'\n')
    f.close()
    
    
        
    
#    for i in range(1,38):
#        getPage(str(i*35))

#f = open('s.txt','w')
#f.open('s.txt','w',encoding='utf8')
#f.write(soup.prettify())
#f.close()
