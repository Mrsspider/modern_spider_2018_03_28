

import pymysql

conn = pymysql.connect(host='127.0.0.1',port=3306,user ='root',passwd='mingkun001',db='modern',use_unicode=True,charset='utf8')
cur = conn.cursor()
sql = 'select * from p_c_z'
cur.execute(sql)
t_l = cur.fetchall()
with open('../result/product_c_or_s.csv','a',encoding='utf8') as f:
    for t in t_l:
        id,c_s,p_id=t
        f.write(str(id)+'^'+c_s+'^'+str(p_id)+'\n')
        print(id,c_s,p_id)
    # print(type(t))
conn.commit()
cur.close()
conn.close()