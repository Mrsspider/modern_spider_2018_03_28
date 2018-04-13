import re
import requests
from lxml import etree
import json
from random import choice
import random
from time import sleep
from functings.spider_function import *
from settings.spider_setting import *
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

x = random.randint(1,3)

# 存档
def mywith(filename,result):
    try:
        with open(filename,'a',encoding='utf8') as f:
            f.writelines(result)
    except Exception as e:
        logbook = {'errorFunc':'mywrith','mywrith':e}
        with open('../logbook/logbook.txt','a',encoding='utf8') as f:
            f.writelines((str(logbook)+'\n'))


def product_with(*args):
    s = ''
    for i in args:
        s+= '^'+str(i)
    s = s[1:]
    with open('../result/product.csv','a',encoding='utf8') as f:
        f.write(s+'\n')



# 提取html页面
def gethtml(url):
    '''输入url,输出字符串respons.text'''
    try:
        respons = requests.get(url,choice(getip()),headers=headers)
        print(choice(getip()))
    except Exception as e:
        print(e)
        respons = gethtml(url)
        # sleep(x)
    respons = respons.content.decode('utf8')
    return respons
    # except Exception as e:
    #     logbook = {'errorFunc':'gethtml','errorType':e,'errorUrl':url,'errorHeaders':headers}
    #     mywith('../logbook/logbook.txt', str(logbook) + '\n')
    #     return None

# 使用xpath解析网页
def htmlparser(html):
    try:
        html = etree.HTML(html,parser=etree.HTMLParser())
        return html
    except Exception as e:
        logbook = {'errorFunc':'htmlparser','htmlparser':e}
        mywith('../logbook/logbook.txt', str(logbook) + '\n')


def get_maxpage(url):
    '''此函数用于获取每个分类的最大页数'''
    html = gethtml(url)
    result = htmlparser(html)
    try:
        max_page = result.xpath('//div[@id="page-theme1"]/a[last()-2]/text()')[0]
    except Exception:
        max_page = 0
    max_page = int(max_page)
    return max_page

def get_fashion_detail_url(cur):
    '''获取数据库中所有时装二级分类界面url'''
    sql = 'SELECT id,product_url from modern_product WHERE level3="时装"'
    cur.execute(sql)
    print(cur.execute(sql))
    product_details_url_t = cur.fetchall()
    for i in product_details_url_t:
        product_details_url = 'http://www.modernavenue.com/' + i[1]
        yield i

def get_chuncai_detail_url(cur):
    '''获取数据库中所有唇彩二级分类界面url'''
    sql = 'SELECT id,product_url from modern_product WHERE level4="唇膏/唇彩"'
    cur.execute(sql)
    product_details_url_t = cur.fetchall()
    for i in product_details_url_t:
        product_details_url = 'http://www.modernavenue.com/' + i[1]
        id = i[0]
        yield (id,product_details_url)

def parse_fashion_details(html):
    '''此函数用于解析所有衣服界面,传入driver对象,传出生成器'''
    result = htmlparser(html)
    all_L = result.xpath('//div[@class="shop_chose clear_fix"]')
    all_L = all_L[0]
    color_list = all_L.xpath('.//div[@id="color"]//img/@title')
    color_list = [x for x in color_list if x]
    size_list = all_L.xpath('.//div[@id="size"]//span/text()')
    return color_list,size_list

def parse_chuncai_details(html):
    '''此函数用于解析唇彩详情页面,传入driver对象,传出该产品对应的所有列表'''
    color_l = re.findall('{\"color\":\"(.*?)\"',html)
    return color_l

def get_driver():
    desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
    headers = {'Accept': '*/*',
               'Accept-Language': 'en-US,en;q=0.8',
               'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
               # 这种修改 UA 也有效
               'Connection': 'keep-alive'
               }

    for key, value in headers.items():
        desired_capabilities['phantomjs.page.customHeaders.{}'.format(key)] = value

    # 修改请求头
    desired_capabilities[
        'phantomjs.page.customHeaders.User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    # 设置缓存
    # service_args = [
    #     '--proxy=%s' % ip_html,  # 代理 IP：prot    （eg：192.168.0.28:808）
    # ‘--load - images = no’,  # 关闭图片加载（可选）
    # '--disk-cache=yes’,            # 开启缓存（可选）
    # '--ignore-ssl-errors=true’    # 忽略https错误（可选）
    # ]
    SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
    driver = webdriver.PhantomJS(desired_capabilities=desired_capabilities, service_args=SERVICE_ARGS)
    print(driver.session_id)
    return driver


def get_driverhtml(url,driver):
    '''此函数获取driver对象,传入url，传出该页面的文本信息'''
    driver.get(url)
    #给浏览器时间加载
    sleep(1+random.random())
    html = driver.page_source
    # print(html)
    # driver.close()
    return html

def parser_md_index(url):
    '''此函数用于解析摩登大道一级页面,传入url,传出商品信息字典的列表'''
    html = gethtml(url)
    result = htmlparser(html)
    product_L = []
    product_list = result.xpath('//ul[@class="clear_fix"]//li')

    for product in product_list:
        product_url = product.xpath('./a[@target="_blank"]/@href')[0]
        img = product.xpath('.//img/@data-src')[0]
        p_br = product.xpath('.//label[@class="p_br p_hover"]/text()')[0]
        p_name = product.xpath('.//label[@class="p_name"]/text()')[0]
        p_price = product.xpath('.//label[@class="p_br"]/text()')[0]
        p_price = re.sub('[^\d+]','',p_price)
        old_price = product.xpath('.//del/text()')
        if old_price:
            old_price = re.sub('[^\d+]', '', old_price[0])
        else:
            old_price = 0
        d = {'product_url': product_url, 'img': img, 'p_br': p_br, 'p_name': p_name, 'p_price': p_price,
             'old_price': old_price}
        yield d


def get_md_url(url):
    '''此函数用户获取摩登大道所有分类的url,返回含有品类name,level1,2,3的字典信息列表'''
    html = gethtml(url)
    # cls_list = re.findall('"link":"(.*?)",\s+"name":"(.*?)"',html)
    # html = re.sub('\s+','',html)

    cls_dic = json.loads(html)['data']
    moder_man_fashion_list = []
    moder_man_shoes_list = []
    moder_man_bag_list = []
    moder_woman_fashion_list = []
    moder_woman_bag_list = []
    moder_woman_shoes_list = []
    makeup_skincare_list = []
    makeup_cmakeup_list = []
    makeup_perfume_list = []
    fine_ornament_list = []
    tech_listen_list = []
    tech_digital_list = []
    for L in cls_dic:
        for L in L['childs']:
            for L in L['childs']:
                # print(L)
                if '1310-1312-1439' in L['levelPath']:
                    d = {'link': L['link'], 'name': L['name'], 'level1': '精品', 'level2': '耳机/音箱','level3':'null'}
                    tech_listen_list.append(d)
                if '1310-1312-1440' in L['levelPath']:
                    d = {'link': L['link'], 'name': L['name'], 'level1': '科技', 'level2': '数码','level3':'null'}
                    tech_digital_list.append(d)
                if '121-1393' in L['levelPath']:
                    d = {'link': L['link'], 'name': L['name'], 'level1': '妆容', 'level2': '护肤','level3':'null'}
                    makeup_skincare_list.append(d)
                if '121-1404' in L['levelPath']:
                    d = {'link': L['link'], 'name': L['name'], 'level1': '妆容', 'level2': '护肤','level3':'null'}
                    makeup_cmakeup_list.append(d)
                if '121-1417' in L['levelPath']:
                    d = {'link': L['link'], 'name': L['name'], 'level1': '妆容', 'level2': '香水','level3':'null'}
                    makeup_perfume_list.append(d)
                if '1310-1311' in L['levelPath']:
                    d = {'link': L['link'], 'name': L['name'], 'level1': '精品', 'level2': '配饰','level3':'null'}
                    fine_ornament_list.append(d)

                for L in L['childs']:
                    if '122-1304-1316' in L['levelPath']:
                        d = {'link':L['link'],'name':L['name'],'level1':'摩登','level2':'男士','level3':'时装'}
                        moder_man_fashion_list.append(d)
                    if '122-1304-1339' in L['levelPath']:
                        d = {'link':L['link'],'name':L['name'],'level1':'摩登','level2':'男士','level3':'鞋履'}
                        moder_man_shoes_list.append(d)
                    if '122-1304-1345' in L['levelPath']:
                        d = {'link':L['link'],'name':L['name'],'level1':'摩登','level2':'男士','level3':'男包'}
                        moder_man_bag_list.append(d)
                    if '123-1304-1355' in L['levelPath']:
                        d = {'link':L['link'],'name':L['name'],'level1':'摩登','level2':'女士','level3':'时装'}
                        moder_woman_fashion_list.append(d)
                    if '123-1304-1368' in L['levelPath']:
                        d = {'link':L['link'],'name':L['name'],'level1':'摩登','level2':'女士','level3':'包袋'}
                        moder_woman_bag_list.append(d)
                    if '123-1304-1380' in L['levelPath']:
                        d = {'link':L['link'],'name':L['name'],'level1':'摩登','level2':'女士','level3':'鞋履'}
                        moder_woman_shoes_list.append(d)
    product_list = moder_man_fashion_list +moder_man_shoes_list+moder_man_bag_list+moder_woman_fashion_list+moder_woman_bag_list+moder_woman_shoes_list+makeup_skincare_list+makeup_cmakeup_list+makeup_perfume_list+fine_ornament_list+tech_listen_list+tech_digital_list
    return product_list



# 该函数测试ip是否可用，可用的ip作为列表输出
def test_ip(iplist):
    '''没有参数，输出可用[ip:port,...]列表'''
    print(len(iplist))
    prolist = []
    n = 0

    for ip in iplist:
        try:
            url = 'https://www.baidu.com/'
            pro = {'http':ip,'https':ip,}
            head = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
            response = requests.get(url,proxies=pro,headers=head)
            test_num = response.status_code
            if test_num == 200:
                prolist.append(ip+',')
                n+=1
                print(n)
            with open('../settings/proxy.txt','a',encoding='utf8') as f:
                f.writelines(prolist)
        except Exception as e:
            e = {'test_ip':e}
            print(e)
            with open('../logbook/logbook.txt','a',encoding='utf-8') as f:
                f.writelines(str(e))
            continue

# 该函数爬取速度小于3s的ip并写入proxy.text
def get_ip(num):
    '''输入爬取页数，把ip以逗号间隔写入proxy.txt首行'''
    url = 'https://www.kuaidaili.com/free/inha/'
    try:
        iplist = []
        for i in range(1,num):
            url = url + str(i)
            respons = requests.get(url).text
            pat = '<td data-title="IP">(.*?)</td>\s+<.*?>(\d+)</td>\s+<.*?>高匿名</td>\s+<.*?>.*?</td>\s+<.*?>.*?<.*?>\s+<.*?>(.*?)秒<'
            pattern = re.compile(pat)
            prolist = re.findall(pattern,respons)
            for pro in prolist:
                print(pro)
                if float(pro[2]) < 2:
                    pro = pro[0]+':'+pro[1]
                    iplist.append(pro)
        print('正在测试爬取到的ip',iplist)
        test_ip(iplist)
    except Exception as e:
        e = {'getip':e}
        with open('../logbook/logbook.txt','a',encoding='utf-8') as f:
            f.writelines(str(e))

def write_log(d):
    with open('../logbook/logbook.txt', 'a', encoding='utf-8') as f:
        f.writelines(str(d))


if __name__ == '__main__':
    get_ip(50)

