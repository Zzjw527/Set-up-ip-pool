from bs4 import BeautifulSoup
import requests
import random
import time 
import parsel
import pymysql
def get_ip_list(url,headers):
    web_data = requests.get(url,headers=headers)
    soup = BeautifulSoup(web_data.text,'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    #第一个tr是列名
    for i in range(1,len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text+":"+tds[2].text)
    return ip_list
def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://'+ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http':proxy_ip}
    return proxies

def check_ip(proxies_list):
    headers = {
'Referer':'https://www.liepin.com/',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}
    can_use=[]
    for proxy in proxies_list:
        try:
            proxy1={'http':proxy}
            response=requests.get('https://baidu.com',headers=headers,proxies=proxy1,timeout=0.1)
            if response.status_code==200:
                can_use.append(proxy)
            else:
                print('不可使用')
        except Exception as e:
            print(e)
        finally:
            print('当前IP'+proxy+'通过')
    print(can_use)
    return can_use

if __name__=='__main__':
    url = "http://www.xicidaili.com/nn/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    ip_list = get_ip_list(url,headers=headers)
    proxies = get_random_ip(ip_list)
    canuseIP=check_ip(ip_list)
    print (canuseIP)
    db = pymysql.connect(
                  host="****",#数据库
                  port=3306,
                  user="****",#用户
                  passwd="****",#密码
                  db="****",#表名
                  charset='utf8'
                  )
    for ip in canuseIP:
        print(ip)
        cursor= db.cursor()    
        sql='INSERT INTO IP地址(IP地址,是否可用) values(%s,%s)'
        cursor.execute(sql,(ip,'可用'))
        db.commit()              
                        

    db.close()
