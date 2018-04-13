from random import choice
from random import choice
import requests
import re
# 随机user-agent


User_Agents = [
    'Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)'
               ]

headers  = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Encoding':'gzip, deflate',
               'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
               'Cache-Control':'max-age=0',
               'Connection':'keep-alive',
               'Upgrade-Insecure-Requests':'1',
               'Cookie':'PHPSESSID=2tomv9cli4jhkg7up9fdfemqd3; UM_distinctid=1614504facd14-03dcb4716888248-4d594130-13c680-1614504face2e9; CNZZDATA1254842228=822391355-1517280745-https%253A%252F%252Fwww.baidu.com%252F%7C1517544881; zg_did=%7B%22did%22%3A%20%221614505022c140-044f957cddf5688-4d594130-13c680-1614505022dc2%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201517549496842%2C%22updated%22%3A%201517549774159%2C%22info%22%3A%201517281411642%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%22626cf9a77c3c1cfef5a22ba9b68bd3d4%22%7D; _uab_collina=151728141513953394158378; _umdata=2BA477700510A7DF755BE2C10E442FE13AD004F9AABEEECFED5D966336193A3B7EC1CC65605A4EFDCD43AD3E795C914C7B1296C5B9F2F66FB9BFFA9828E872D4; acw_tc=AQAAAD7Ye0jT7woAdmvIfMKmjB8qhQYa; hasShow=1',
               'User-Agent': choice(User_Agents)
               }


# 该函数用来提取文档proxy.txt中的所有ip作为列表输出
def getip():
    with open('../settings/proxy.txt','r',encoding='utf8') as f:
        iplist = f.read()
    iplist = iplist.split(',')
    return iplist

# myip = choice(getip())
# print(myip)
