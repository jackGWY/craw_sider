import requests
import os

def getProxyList(target_url=TARGET_URL, pages='1'):
    """
    爬取代理IP地址
    :param target_url: 爬取的代理IP网址
    :return:
    """
    proxyFile = open(FILE_NAME, "a+", newline="")
    writer = csv.writer(proxyFile)

    r = requests.get(target_url + pages, headers=headers, timeout=2.5)
    document_tree = lxml.html.fromstring(r.text)
    rows = document_tree.cssselect("#ip_list tr")
    rows.pop(0)
    for row in rows:
        tds = row.cssselect("td")
        proxy_ip = tds[1].text_content()
        proxy_port = tds[2].text_content()
        proxy_addr = tds[3].text_content().strip()
        writer.writerow([proxy_ip, proxy_port, proxy_addr])

    proxyFile.close()

def verifyProxies(verify_url, file_path=FILE_NAME):
    session = requests.session()
    proxyFile = open(FILE_NAME, "r+")
    csv_reader = csv.reader(proxyFile)
    p = Pool(10)
    for row in csv_reader:
        proxies = {"http": "http://" + row[0] + ":" + row[1]}
        p.apply_async(verifyProxy, args=(verify_url, proxies, session))
    p.close()
    p.join()
    proxyFile.close()