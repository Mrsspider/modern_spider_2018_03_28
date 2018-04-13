
import pymysql

conn = pymysql.connect(host='127.0.0.1',port=3306,user ='root',passwd='mingkun001',db='modern',use_unicode=True,charset='utf8')
cur = conn.cursor()
sql = 'select * from modern_product'
cur.execute(sql)
t_l = cur.fetchall()
with open('../result/product.csv','a',encoding='utf8') as f:
    for t in t_l:
        id,level1,level2,level3,level4,p_br,p_name,price,old_price,url,img,c_time,u_time=t
        f.write(str(id)+'^'+level1+'^'+level2+'^'+level3+'^'+level4+'^'+p_br+'^'+p_name+'^'+str(price)+'^'+str(old_price)+'^'+url+'^'+img+'\n')
        print(id,level1,level2,level3,level4,p_br,p_name,price,old_price,url,img)
    # print(type(t))
conn.commit()
cur.close()
conn.close()

