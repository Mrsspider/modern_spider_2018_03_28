from pprint import pprint
from random import choice

import pymysql
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from functings.spider_function import *

headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9',
'Connection':'keep-alive',
'Cookie':'pgv_pvi=9445054464; ASPSESSIONIDQCQCTSDB=PHGNEGPBIHLGGNDCMJALBBIG; pgv_si=s3086349312',
'Host':'2017.ip138.com',
'Referer':'http://www.ip138.com/',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}
proxies = {'http':'117.90.5.65:9000'}
url = 'http://2017.ip138.com/ic.asp'
response = requests.get(url,proxies=proxies,headers=headers)
print(response.content.decode('gb2312'))







