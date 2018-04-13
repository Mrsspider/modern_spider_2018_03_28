
import json
import re
import pymysql
from functings.spider_function import *

def main():
    conn = pymysql.connect(host='127.0.0.1',port=3306,user ='root',passwd='mingkun001',db='modern',use_unicode=True,charset='utf8')
    cur = conn.cursor()

    #获取所有分类url和分类
    url = 'http://www.modernavenue.com/portal-web/columnsInfo/findLeftColumn?data={%22pageNo%22:2}'
    product_url_list = get_md_url(url)
    for allproduct in product_url_list:
        #获取第一页的所有商品
        product_list = parser_md_index(url)
        url = allproduct['link']
        # print(url)
        name = allproduct['name']
        level1 = allproduct['level1']
        level2 = allproduct['level2']
        level3 = allproduct['level3']
        print('正在爬取%s,%s,%s,%s的第1页'%(level1,level2,level3,name))
        #获取所有商品信息并处理第一页
        maxpage = get_maxpage(url)
        p_getor = parser_md_index(url)
        for p in p_getor:
            product_url, img, p_br, p_name, p_price, old_price = p['product_url'], p['img'], p['p_br'], p['p_name'], p['p_price'], p['old_price']
            # print(level1,level2,level3,name,product_url,img,p_br,p_name,p_price,old_price)
            product_with(level1,level2,level3,name,p_br,p_name,p_price,old_price,product_url,img)
            name = re.sub('\"','\'',name)
            p_name = re.sub('\"', '\'', p_name)
            sql = 'INSERT INTO modern_product (level1,level2,level3,level4,p_br,p_name,p_price,old_price,product_url,img) VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'.format(level1, level2, level3, name, p_br, p_name, p_price, old_price, product_url, img)
            # print(sql)
            cur.execute(sql)

        #处理只有一页的商品类型,有多页才进行持续爬取
        if maxpage:
            for page in range(2,maxpage+1):
                print('正在爬取%s,%s,%s,%s的第%s页' % (level1, level2, level3, name,page))
                pageurl = url+'&page=%s#mSearch'%page
                # print(pageurl)
                p_list = parser_md_index(pageurl)
                for p in p_list:
                    product_url, img, p_br, p_name, p_price, old_price = p['product_url'], p['img'], p['p_br'], p['p_name'],p['p_price'], p['old_price']
                    product_with(level1, level2, level3, name, p_br, p_name, p_price, old_price, product_url, img)
                    name = re.sub('\"','\'',name)
                    p_name = re.sub('\"','\'',p_name)
                    sql = 'INSERT INTO modern_product (level1,level2,level3,level4,p_br,p_name,p_price,old_price,product_url,img) VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'.format(level1, level2, level3, name, p_br, p_name, p_price, old_price, product_url, img)
                    cur.execute(sql)
    #爬取二级界面
    driver = get_driver()
    sleep(2)
#爬取衣服二级界面
    url_getor = get_fashion_detail_url(cur)
    n = 0
    s = 0
    for t in url_getor:
        try:
            id = t[0]
            url = t[1]
            url = 'http://www.modernavenue.com' + url
            html = get_driverhtml(url, driver)
            color_l, size_l = parse_fashion_details(html)
            while not color_l:
                html = get_driverhtml(url)
                color_l, size_l = parse_fashion_details(html)
            n += 1
            s += 1
            if s % 100 == 0:
                sleep(10)
                driver.close()
                driver = get_driver()
                sleep(2)
            print('爬取衣服二级界面第{}页'.format(n))
            for i in color_l:
                sql = 'INSERT INTO p_c_z (c_z,p_id) VALUES ("{}","{}")'.format(i, id)
                cur.execute(sql)
            for i in size_l:
                sql = 'INSERT INTO p_c_z (c_z,p_id) VALUES ("{}","{}")'.format(i, id)
                cur.execute(sql)
            conn.commit()
            print('over')
        except Exception as e:
            s = 0
            driver.close()
            print(e)
            print('衣服二级界面第{}页爬取失败'.format(n))
            driver = get_driver()
            sleep(2)
            continue
    driver.close()
    #爬取唇彩二级界面
    driver = get_driver()
    chuncai_url = get_chuncai_detail_url(cur)
    n = 0
    s = 0
    for t in chuncai_url:
        id = t[0]
        url = t[1]
        try:
            html = get_driverhtml(url, driver)
            chuncai_L = parse_chuncai_details(html)
            n += 1
            s += 1
            if s % 100 == 0:
                sleep(10)
                driver.close()
                driver = get_driver()
                sleep(2)
            print('爬取唇彩二级界面第{}页'.format(n))
            while not chuncai_L:
                html = get_driverhtml(url, driver)
                chuncai_L = parse_chuncai_details(html)
            for i in chuncai_L:
                sql = 'INSERT INTO p_c_z (c_z,p_id) VALUES ("{}","{}")'.format(i, id)
                cur.execute(sql)
                conn.commit()
            print('over')
        except Exception as e:
            s = 0
            driver.close()
            print(e)
            print('唇彩二级界面第{}页爬取失败'.format(n))
            driver = get_driver()
            sleep(2)
            continue

    conn.commit()
    cur.close()
    conn.close()
    driver.close()

if __name__ == '__main__':
    main()
