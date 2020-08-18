# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 17:27:04 2020

@author: hp
"""
from lxml import etree
import requests
import random
import time 
import parsel
import pymysql
proxies_list=[]
def check_ip(proxies_list):
    headers = {
'Referer':'https://www.liepin.com/',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}
    can_use=[]
    for proxy in proxies_list:
        try:
            
            response=requests.get('https://baidu.com',headers=headers,proxies=proxy,timeout=0.1)
            if response.status_code==200:
                can_use.append(proxy)
            else:
                print('不可使用')
        except Exception as e:
            print(e)
        finally:
            print('当前IP',proxy,'通过')
    print(can_use)
    return can_use

for page in range(91,150):
    print('==========正在获取第{}页数据============'.format(str(page)))
    base_url='https://www.kuaidaili.com/free/inha/{}/'.format(str(page))
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    response=requests.get(base_url,headers=headers)
    data=response.text
    html_data = etree.HTML(data)
    
    parse_list=html_data.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')
    
    for tr in parse_list:
        dict_proxies={}
        http_type=tr.xpath('./td[4]/text()')
        
        ip_num=tr.xpath('./td[1]/text()')
       
        ip_port=tr.xpath('./td[2]/text()')
        
        dict_proxies[http_type[0]]=ip_num[0]+':'+ip_port[0] 
        print(dict_proxies)
        proxies_list.append(dict_proxies)
        time.sleep(0.5)

can_use=check_ip(proxies_list)

db = pymysql.connect(
                  host="****",#数据库
                  port=3306,
                  user="****",#用户
                  passwd="****",#密码
                  db="****",#表名
                  charset='utf8'
                  )
for ip in can_use:
    
    for realip in ip:  
        cursor= db.cursor()    
        sql='INSERT INTO IP地址(IP地址,是否可用) values(%s,%s)'
        cursor.execute(sql,(ip[realip],'可用'))
        db.commit()              
                    

db.close()