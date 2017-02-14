__author__ = 'Suarezlin'
import requests
import re
import random
from bs4 import BeautifulSoup
import urllib
import prettytable
import sys
from .decorators import async
class DEAN:
    def __init__(self):
        self.username=''
        self.password=''
        self.login = 'https://cas.xjtu.edu.cn/login'
        self.posturl = 'http://ssfw.xjtu.edu.cn/index.portal'
        self.classurl = 'http://ssfw.xjtu.edu.cn/index.portal?.pn=p1142_p1145_p1542'
        self.gradeurl = 'http://ssfw.xjtu.edu.cn/index.portal?.pn=p1142_p1144_p1156'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'Host': 'ssfw.xjtu.edu.cn',
            'Referer': 'http://ssfw.xjtu.edu.cn/',
            'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1'
        }
        self.session = requests.session()

    def getLt(self):
        request = self.session.get(self.posturl)
        request = request.text
        str = 'name="lt" value="(.*?)"'
        pattern = re.compile(str, re.S)
        lt = re.findall(pattern, request)
        return lt[0]
    def logIn(self):
        str = '登录'
        str = str.encode('utf-8')
        postdata = {
            'username': self.username,
            'password': self.password,
            'code': '',
            'lt': self.getLt(),
            'execution': 'e1s1',
            '_eventId': 'submit',
            'submit': str
        }
        self.session.post(self.login, postdata)
        r = self.session.get(self.posturl)
        soup = BeautifulSoup(r.text, 'html.parser').find('meta').get('content')[6:]
        self.session.get(soup)

    def ins(self, a):
        if len(a) < 6:
            number = []
            for it in a:
                search = '~'
                start = 0
                index = it.find(search, start)
                if index > 0:
                    number.append(it[index - 1])
            if '1' not in number:
                a.insert(0, '')
            if '3' not in number:
                a.insert(1, '')
            if '5' not in number:
                a.insert(2, '')
            if '7' not in number:
                a.insert(3, '')
    def saveImg(self,pic_url,filename):
        u=self.session.get(pic_url,headers=self.header)
        data=u.content
        f=open('/home/suarezlin/PycharmProjects/web/app/static/pic/'+filename,"wb")
        f.write(data)
        f.close()
    def getGI(self):
        s=self.session.get(self.posturl)
        text=s.text
        pic=[]
        pattern_2=re.compile('pen=(.*?)&.*?f=(.*?)&',re.S)
        a=re.findall(pattern_2,text)
        pattern=re.compile('span_unedit">(.*?)</span>',re.S)
        pic_path='/home/suarezlin/图片/pic'
        item = re.findall(pattern, text)
        print(a,item)
        pic_url='http://ssfw.xjtu.edu.cn/w5ssfw/srvlet/showimage.jsp?.pen={}&.f={}&action=download&notUseCache=true&id={}&field=xjzp&s={}'.format(a[0][0],a[0][1],item[0][0:len(item[0])-1],str(random.random()))
        self.saveImg(pic_url,item[0][0:len(item[0])-1]+'.jpg')
        return [pic,item[0:10]]
    def getClassTable(self):
        r = self.session.get(self.classurl)
        pattern = re.compile('class="fcSpanDiv"></div></div>(.*?)</td><td colspan=1 rowspan=".*?">', re.S)
        trs = re.findall(pattern, r.text)
        replaceBR = re.compile('<br>')
        replaceNBSP = re.compile('&nbsp;')
        text = []
        classinfo = []
        for it in trs:
            text.append(re.sub(replaceBR, "\n", it))
        for it in text:
            classinfo.append(re.sub(replaceNBSP, " ", it))
        i = 0
        mon = []
        tue = []
        wen = []
        thr = []
        fry = []
        for it in classinfo:
            if '周一' in it:
                mon.append(it)
            elif '周二' in it:
                tue.append(it)
            elif '周三' in it:
                wen.append(it)
            elif '周四' in it:
                thr.append(it)
            elif '周五' in it:
                fry.append(it)
        self.ins(mon)
        self.ins(tue)
        self.ins(wen)
        self.ins(thr)
        self.ins(fry)
        return [mon,tue,wen,thr,fry]
    def getGrade(self):
        r = self.session.get(self.gradeurl)
        text = r.text
        # print(text)
        pattern = re.compile(
            '<td class="">(.*?)</td>.*?<td class="">(.*?)</td>.*?<td class="">(.*?)</td>.*?<td class="">(.*?)</td>.*?<td class="">(.*?)</td>.*?<td class="">.*?">(.*?)</a>.*?<td class="">(.*?)</td>.*?<td class="">(.*?)</td>.*?<td class="">(.*?)</td>.*?<td class="">(.*?)</td>',
            re.S)
        s = re.findall(pattern, text)
        a = []
        for it in s:
            ss = list(it)
            aa = []
            for ch in ss:
                ch = ch.lstrip()
                ch = ch.rstrip()
                aa.append(ch)
            a.append(aa)
        return a
