import os
from lxml import etree
import requests
import urllib
import time
import pymysql

conn = pymysql.Connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='paindatabase', charset='utf8')
# headers={'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) '
#                        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

headers = {
    'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
def getSideeffect_link_list():
    sideeffect_link_list=[]
    f=open('sideeffect_link.txt',"r")
    for line in f.readlines():
        line=line.split(",")
        sideeffect_link=line[0]
        sideeffect_link_list.append(sideeffect_link)
    return sideeffect_link_list
sideeffect_link_list=getSideeffect_link_list()

for sideeffect_link in sideeffect_link_list:
    sideeffect_dict={
        "sideeffect_link":sideeffect_link,
        "sideeffect_name": "None",
        "Definition": "None",
        "Synonyms": "None"
    }
    time.sleep(20)
    html = requests.get(sideeffect_link, headers=headers)
    data = html.text
    s = etree.HTML(data)
    sideeffect_name = s.xpath('/html/body/div/h1/text()')
    if sideeffect_name == []:
        sideeffect_name = "None"
    else:
        sideeffect_name = sideeffect_name[0].strip()
    print("sideeffect_name:", sideeffect_name)
    sideeffect_dict["sideeffect_name"]=sideeffect_name
    Definition = s.xpath('/html/body/div/div[1]/p[1]/text()')
    if Definition == []:
        Definition = "None"
    else:
        Definition = Definition[0].strip()
    print("Definition:", Definition)
    sideeffect_dict["Definition"]=Definition
    Synonyms = s.xpath('/html/body/div/div[1]/p[2]/text()')
    if Synonyms == []:
        Synonyms = "None"
    else:
        Synonyms = Synonyms[0].strip()
    print("Synonyms:", Synonyms)
    sideeffect_dict["Synonyms"] = Synonyms

    sideeffect_cursor = conn.cursor()
    sql_sideEffect="replace INTO SiderEffect(sideeffect_link,sideeffect_name,Definition,Synonyms)VALUES " \
             "(%(sideeffect_link)s,%(sideeffect_name)s,%(Definition)s,%(Synonyms)s)"
    try:
        sideeffect_cursor.execute(sql_sideEffect,sideeffect_dict)
        conn.commit()
        sideeffect_cursor.close()
    except Exception as e:
        print("???????????????????????????????????????")
        print(e)
        conn.rollback()
        time.sleep(10)
    for i in range(1, 51):
        drug_with_sideeffect_dict={
            "drug_with_sideeffect":"",
            "drug_with_sideeffect_link":"",
            "sideeffect_link":sideeffect_link
        }
        drug_with_sideeffect = s.xpath('/html/body/div[3]/div[2]/table/tr/td[1]/ul/li[' + str(i) + ']/a/text()')
        if drug_with_sideeffect == []:
            continue
        else:
            drug_with_sideeffect = drug_with_sideeffect[0].strip()
            print("drug_with_sideeffect:", drug_with_sideeffect)
            drug_with_sideeffect_dict["drug_with_sideeffect"]=drug_with_sideeffect

        drug_with_sideeffect_link = s.xpath('/html/body/div[3]/div[2]/table/tr/td[1]/ul/li[' + str(i) + ']/a/@href')
        if drug_with_sideeffect_link == []:
            continue
        else:
            drug_with_sideeffect_link = drug_with_sideeffect_link[0].strip()
            drug_with_sideeffect_link = 'http://sideeffects.embl.de' + drug_with_sideeffect_link
            print("drug_with_sideeffect_link:", drug_with_sideeffect_link)
            drug_with_sideeffect_dict["drug_with_sideeffect_link"]=drug_with_sideeffect_link
        drug_with_sideeffect_cursor=conn.cursor()
        sql_drug="replace INTO Sider_to_drug(drug_with_sideeffect,drug_with_sideeffect_link,sideeffect_link) VALUES " \
                 "(%(drug_with_sideeffect)s,%(drug_with_sideeffect_link)s,%(sideeffect_link)s)"
        try:
            drug_with_sideeffect_cursor.execute(sql_drug,drug_with_sideeffect_dict)
            conn.commit()
            drug_with_sideeffect_cursor.close()
        except Exception as e:
            print("???????????????????????????????????????")
            print(e)
            conn.rollback()
            time.sleep(10)

conn.close()

