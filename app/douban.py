__author__ = 'Suarezlin'
import requests
import re
import threading
import time
def rere(douban,pattern,text_book,pic):
    #time.sleep(5)
    book_in=re.findall(pattern,text_book)
    b=list(book_in[0])
    douban.book_.append(b.append(pic))
    print(book_in[0])
    #time.sleep(4)
    #print('end')
class Douban():
    def __init__(self):
        self.url='https://book.douban.com/top250?'
        self.book_url='https://book.douban.com/subject/{}/'
        self.book_=[]
    def getBook(self):
        text_1=requests.get(self.url+'icn=index-book250-all').text
        pattern=re.compile('<a class="nbg" href="https://book.*?douban.*?com/subject/(.*?)/".*?<img src="(.*?)" width=',re.S)
        book=re.findall(pattern,text_1)
        print('end')
        for i in range(1,10):
            page_num='start='+str(i*25)
            text_i=requests.get(self.url+page_num).text
            pattern=re.compile('<a class="nbg" href="https://book.*?douban.*?com/subject/(.*?)/".*?<img src="(.*?)" width=',re.S)
            book=re.findall(pattern,text_i)
            for booka in book:
                bookurl=self.book_url.format(booka[0])
                text_book=requests.get(bookurl).text
                pattern=re.compile('<span property="v:itemreviewed">(.*?)</span>.*?<span class="pl"> 作者</span>:.*?">(.*?)</a>.*?div class="intro">.*?<p>(.*?)</p>',re.S)
                book_in=re.findall(pattern,text_book)
                try:
                    self.book_.append(book_in[0])
                except:
                    pass
        return self.book_


douban=Douban()
book=douban.getBook()

