import os
from lxml import etree
import requests
import urllib
import time
import pymysql

# def get_host_list():
#     f_host = open("proxy.txt", "r")
#     host_list = []
#     for line in f_host.readlines():
#         # print(line.strip())
#         host_list.append(line.strip())
#     return host_list
# host_list=get_host_list()
#
# host_count=0
def getSider_drug_link():
    drug_link_list=[]
    f=open("sider_drug_link_to_drugbankId.txt","r")
    for line in f.readlines():
        line=line.split(",")
        sider_drug_link=line[0]
        drug_link_list.append(sider_drug_link)
    return drug_link_list
headers={'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
drug_link_list=getSider_drug_link()
for sider_drug_link in drug_link_list:
    html = requests.get(sider_drug_link, headers=headers)
    data = html.text
    s = etree.HTML(data)
    drug_name = s.xpath('//*[@id="drugInfoMain"]/h1/text()')
    if drug_name == []:
        drug_name = "None"
    else:
        drug_name = drug_name[0].strip()
    print("drug_name:", drug_name)
    f = open("sideeffect_link.txt", "a")
    has_sideeffect = "None"
    #爬取sidereffect 的name和链接
    for i in range(3, 45):
        sideeffect_name = s.xpath('//*[@id="drugInfoTable"]/table/tr[' + str(i) + ']/td[1]/a/text()')
        if sideeffect_name == []:
            continue
        else:
            sideeffect_name = sideeffect_name[0].strip()
            print("sideeffect_name:", sideeffect_name)

        sideeffect_link = s.xpath('//*[@id="drugInfoTable"]/table/tr[' + str(i) + ']/td[1]/a/@href')
        if sideeffect_link == []:
            continue
        else:
            sideeffect_link = sideeffect_link[0].strip()
            sideeffect_link = 'http://sideeffects.embl.de' + sideeffect_link
            print("sideeffect_link:", sideeffect_link)
        f.writelines(sideeffect_link + "," + sideeffect_name + "," + drug_name + "," + sider_drug_link+"\n")
    f.close()


