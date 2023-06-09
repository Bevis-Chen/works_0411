import requests, time, math, threading
import sqlite3, os
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from queue import Queue
from tools import get_chrome, find_element, get_soup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

def get_104_data(url):
#     只有一頁資料
    global q
    try:
        soup= get_soup(url_104.format(keys, page))
        soup_datas= soup.find("div", id="js-job-list").find_all('article')
        datas= []
        for data in soup_datas:
            title= data.find("h2", class_="b-tit").find("a").text
            salarys= data.find("div", class_="job-list-tag b-content").text.split()[0]
            city= data.find("ul", class_="b-list-inline b-clearfix job-list-intro b-content").text.split()[0]
            name= data.find('ul', class_="b-list-inline b-clearfix").find(target="_blank").text.strip()
            job_url= "https:"+data.find("h2", class_="b-tit").find("a").get('href')
            datas.append([title, salarys, city, name, job_url])
        q.put(datas)
        return datas
    except Exception as e:
        print(e, '\n  Ooooo!!!')

# url_104= "https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword={}&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=14&asc=0&page={}&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob=1"   
url= 'https://www.104.com.tw/jobs/main/'
chrome= get_chrome(url, hide =True)
keys= input("找工作>>> ")
time.sleep(1)
# 輸入框
xpath1= "/html/body/article[1]/div/div/div[4]/div/input"
element= find_element(chrome, xpath1)
element.clear()
element.click()
time.sleep(.5)    
element.send_keys(keys+ "\n")
time.sleep(.3)
pagemax= eval(BeautifulSoup(chrome.page_source, "lxml").find_all("option")[-1].get("value"))
chrome.quit()
threads= []
all_datas=[]
q= Queue()
start= datetime.now()
url_104= "https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword={}&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=14&asc=0&page={}&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob=1"   
for page in range(pagemax):
    print(url_104.format(keys, page+1))
    t= threading.Thread(target= get_104_data, args= (url_104.format(keys, page+1), ))
    t.start()
    threads.append(t)
    time.sleep(0.5)
#     all_datas.extend(get_104_data(url_104.format(keys, page+1)))
for thread in threads:
    thread.join()
for i in range(q.qsize()):
    all_datas+=q.get() 
print()
# print(all_datas)
print('總體時間>>> ', datetime.now()-start)    
df= pd.DataFrame(all_datas)
# print(df)

# 建立資料庫
create_table_sqlstr= """CREATE TABLE "try2_sheet1" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"title"	TEXT NOT NULL,
	"salarys"	TEXT NOT NULL,
	"company_city"	TEXT NOT NULL,
	"company_name"	TEXT NOT NULL,
	"job_url"	TEXT NOT NULL );"""
sqlstr1= '''create table if not exists tablename CREATE TABLE'''

conn= None
nowtime= datetime.now().strftime("%Y/%m/%d %H:%M:%S")
db_name= "project001.db"

try:
    # 第一次為建立資料表
    if not os.path.exists(db_name):
        print('資料庫跟資料表建立中...')
        # 開啟資料庫    
        conn= sqlite3.connect(db_name)
        # count 是代表寫入行數
        count= df.to_sql(keys,con=conn,if_exists='append',index=False)
        print(count)
except Exception as e:
    print(e, "\n = =???")        
finally:
    if conn is not None:
        conn.close()            
        conn=None
        print('資料庫關閉.')  


