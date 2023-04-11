import requests, time, math, threading
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
print('總體時間>>> ', datetime.now()-start)    
print(all_datas)


