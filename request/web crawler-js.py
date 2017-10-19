#encoding=utf8
'''
Created on 2017.9.11

@author: huke
'''

import sys
from PyQt4.QtGui import *
from PyQt4.Qtcore import *
from PyQt4.QtWebKit import *

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

class Render(QWebPage):
def __init__(self, url):
    self.app = QApplication(sys.argv)
    QWebPage.__init__(self)
    self.loadFinished.connect(self._loadFinished)
    self.mainFrame().load(QUrl(url))
    self.app.exec_()
def _loadFinished(self, result):
    self.frame = self.mainFrame()
    self.app.quit()



if __name__ == '__main__':
    url = 'http://m.toutiao.com/profile/4492956276/'
    # This does the magic.Loads everything
    r = Render(url)
    # Result is a QString.
    result = r.frame.toHtml()
    # QString should be converted to string before processed by lxml
    formatted_result = str(result.toAscii())
    # Next build lxml tree from formatted_result
    tree = html.fromstring(formatted_result)
    # Now using correct Xpath we are fetching URL of archives
    archive_links = tree.xpath('//p[@class='body-text']')
    print(archive_links)
