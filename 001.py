# -*- coding: utf-8 -*-
import re
import urllib
import urllib.request

from bs4 import BeautifulSoup

root='https://www.bookbao99.net'
book_root = root+"/book/201611/01/id_XNTQ2NjYx.html"
book_base='/views/201611/01/id_XNTQ2NjYx_'

# 伪造浏览器
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) ' \
                         'AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/62.0.3202.62 Safari/537.36'}

req = urllib.request.Request(url=book_root, headers=headers)

with urllib.request.urlopen(req, timeout=1) as response:
    # 大部分的涉及小说的网页都有charset='gbk'，所以使用gbk编码
    htmls = response.read().decode('utf-8')


dir_req = re.compile(r'<a href="'+book_base+'(.*)" target="_blank">(.*)</a></li>')
dirs = dir_req.findall(htmls)
fp = open('国色天香.txt', 'a')
#总循环数
i=1

#章数
num=1

for item in dirs:
    url=root+'/'+book_base+item[0]
    chap_name=item[1]
    print(url,chap_name)
    if i > 6:
        fp.write('\r\n'+'第'+str(num)+"章:"+chap_name+'\r\n')
        tmp_chap=urllib.request.Request(url=url, headers=headers)
        # with urllib.request.urlopen(tmp_chap, timeout=0.6) as response:
        with urllib.request.urlopen(tmp_chap) as response:
            tmp_chap_html = response.read().decode('utf-8')
        soup2 = BeautifulSoup(tmp_chap_html, 'html.parser')
        content = soup2.find('dd',id="contents")
        cont=content.text.strip().replace('\n','').replace('\t','').replace('\r','')
        fp.write(cont)
        num+=1
    i+=1

fp.close()

