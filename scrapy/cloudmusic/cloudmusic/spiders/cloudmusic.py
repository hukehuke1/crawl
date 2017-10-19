#encoding=utf8
'''
Created on 2017.9.13

@author: huke
'''

import scrapy
from cloudmusic.items import CloudmusicItem
from asn1crypto.ocsp import Request
from wsgiref.headers import Headers

class CloudmusicSpider(scrapy.spiders.Spider):
    name = "cloudmusic"  # 爬虫的名字，执行时使用
    allowed_domains = ["music.163.com"]  # 允许爬取的域名，非此域名的网页不会爬取
    start_urls = [
        "http://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset=1"  # 起始url，此例只爬这一个页面   
    ]
    cookies = {}
    headers = {
    'Referer':'http://music.163.com/',
    'Host':'music.163.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    #'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
    }
    

    def parse(self, response):  # 真正的爬虫方法
        html = response.body  # response是获取到的来自网站的返回
        table = response.xpath('//div[@class="u-cover u-cover-1"]')
        # 以下四行将html存入文件
        i = response.xpath('//a[@class="zpgi"]/text()')
        maxoffset = i[-1].extract() #取出最大页面数
        for each in table:
            item = CloudmusicItem() # 实例化一个Item对象
            item['songID'] = each.xpath('a/@href').extract()
            item['songName'] = each.xpath('a/@title').extract()
            item['songCount'] = each.xpath('div/span[2]/text()').extract()  #获取songID
            yield item
        newUrl = get_next_url(self,response.url,maxoffset)
        
        filename = "index.html"
        file = open(filename, "w",encoding='utf8') 
        file.write(html.decode('utf8')) #TypeError: must be str, not bytes 的时候加decode
        file.close()  # 将创建并赋值好的Item对象传递到PipeLine当中进行处理
       
    def start_requests(self):
#         这是一个重载函数，作用是发出第一个Request请求
        # 带着headers、cookies去请求self.start_urls[0],返回的response会被送到
        # 回调函数parse中
        yield Request(self.start_urls[0],callback=self.parse,headers=self.headers)
        
    def get_next_url(self,oldUrl, maxoffset):
        #返回下次迭代的URL
        #param oldUrl:上一个爬去国的URL
        #return 下次要爬去的URL
        # 传入的url格式：http://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset=1
        l = oldUrl.split('=')
        #global maxOffset #最大页码数
        if l[-1] + 35 >= maxOffset:
            return
        newUrl = ''
        for x in range(0,len(l)-1):
            newUrl = str(newUrl)+'='+str(l[x])
        newUrl = newUrl +'=' + str(int(l[-1]) + 34)
        return str(newUrl)#返回心得URL