__author__ = 'Suarezlin'
import requests
import re
import time
book=["安徽省居民阶梯电价表及计算方法"]
cookie ='SINAGLOBAL=3479448692858.8486.1473233972969; saeut=1.85.33.67.1474290374137196; CNZZDATA5168491=cnzz_eid%3D194655509-1479357871-http%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1479702835; un=17791652478; SCF=AvoFo14RjNTm8Z1FSaPUILUgGeBQL6Z35MfFGF8mvXEyKEn5ilU_IzO48g5SgU0QjVF5pye_wXqKkbCnSMbsGZE.; SUB=_2A251XmUQDeRxGeNG6VAT8yvMyzyIHXVWKtHYrDV8PUJbmtBeLWrXkW8CfmJR4lLzTDBB9dsvchPYW9pjJA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5wW94pEZ-lTeiMLIPNw4ke5JpX5o2p5NHD95Qf1hzEeoefeh57Ws4Dqcjb-NHyMJHATCH8Sb-4xC-4SEH8SCHWxF-4eFH8SE-R1C-4Bntt; SUHB=0G0uzJWxv3C9Sv; ALF=1513834685; SSOLoginState=1482298688; _s_tentry=login.sina.com.cn; UOR=www.baidu.com,weibo.com,cn.ui.vmall.com; CNZZDATA3212592=cnzz_eid%3D1797183396-1474290189-null%26ntime%3D1482323922; Apache=818343593401.6559.1482326308130; ULV=1482326308153:53:9:2:818343593401.6559.1482326308130:1482234937922; WBStorage=2c466cc84b6dda21|undefined'
headers = {
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36',
    'cookie': cookie
}
url='http://www.baidu.com/s?ie=UTF-8&wd={}%20pdf%20site%3Avdisk.weibo.com'
getd='http://vdisk.weibo.com/wap/api/weipan/fileopsStatCount?link={}&ops=download&_={}'
item=[]
fail=[]
for it in book:
    book_url=url.format(it)
    text=requests.get(book_url).text
    pattern=re.compile('data-tools=\'\{"title":"(.*?)","url":"(.*?)"}',re.S)
    x=re.findall(pattern,text)[0]
    t=requests.get(x[1],allow_redirects=False).headers["location"]
    t=t[:23]+'wap/'+t[23:]
    co=t[29:]
    down=getd.format(co,str(int(round(time.time() * 1000))))
    headers["Referer"]=t
    try:
        down_url=requests.get(down,headers=headers).json()["url"]
        item.append(x[0])
        pdf=requests.get(down_url)
        filename=it+'.pdf'
        with open(filename, 'wb') as f:
            f.write(pdf.content)
        print(it)
    except:
        print('失败')
        fail.append(it)

