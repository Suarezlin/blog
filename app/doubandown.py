__author__ = 'Suarezlin'
import requests
import re
import time

url='http://vdisk.weibo.com/s/crTpa6lcVQCDd'
cookie ='SINAGLOBAL=3479448692858.8486.1473233972969; saeut=1.85.33.67.1474290374137196; un=17791652478; wvr=6; CNZZDATA5168491=cnzz_eid%3D194655509-1479357871-http%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1479702835; SCF=AvoFo14RjNTm8Z1FSaPUILUgGeBQL6Z35MfFGF8mvXEyIh9q2VEmlBrfD-cb2SPMSyJzwGlblJE6e4Y4PBUOaks.; SUB=_2A251MFkJDeTxGeNG6VAT8yvMyzyIHXVWRM3BrDV8PUNbmtBeLRPBkW8W46Rec-5Hw5JBDgZs4CCqsAVKFw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5wW94pEZ-lTeiMLIPNw4ke5JpX5KMhUgL.Fo-ReozEe0-7eh52dJLoIEiKUg8E9PQ_i--ciKL8iK.Ni--fi-82iK.7i--NiKn4iKLF; SUHB=0jBIt3G1SEVKVF; ALF=1511349464; SSOLoginState=1479813465; _s_tentry=login.sina.com.cn; Apache=1802937096019.4968.1479813480598; ULV=1479813480833:42:11:3:1802937096019.4968.1479813480598:1479706317052; CNZZDATA3212592=cnzz_eid%3D1797183396-1474290189-null%26ntime%3D1479823901; UOR=www.baidu.com,weibo.com,www.baidu.com; WBStorage=2c466cc84b6dda21|undefined'
headers = {
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36',
    'cookie': cookie
}