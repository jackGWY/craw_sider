import pymysql
import time
f=open('sideeffect_link.txt',"r")
conn = pymysql.Connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='paindatabase', charset='utf8')

for line in f.readlines():
    line=line.split(",")
    sideeffect_link=line[0]
    sideeffect_name=line[1]
    sider_drug_name=line[2]
    sider_drug_link=line[3]
    print("sideeffect_link:",sideeffect_link)
    print("sideeffect_name:", sideeffect_name)
    print("sider_drug_name:", sider_drug_name)
    print("sider_drug_link:", sider_drug_link)

    value={
        "sideeffect_link":sideeffect_link,
        "sideeffect_name": sideeffect_name,
        "sider_drug_name": sider_drug_name,
        "sider_drug_link": sider_drug_link
    }
    cursor = conn.cursor()
    sql = "replace INTO sideeffect_of_sider_drug(sideeffect_link,sideeffect_name,sider_drug_name,sider_drug_link)VALUES " \
                     "(%(sideeffect_link)s,%(sideeffect_name)s,%(sider_drug_name)s,%(sider_drug_link)s)"
    try:
        cursor.execute(sql, value)
        conn.commit()
        cursor.close()
    except Exception as e:
        print("???????????????????????????????????????")
        print(e)
        conn.rollback()
        time.sleep(10)

conn.close()