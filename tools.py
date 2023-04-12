import requests, time, copy
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent

def get_chrome(url, chromeDriver= r'C:\webdriver\chromedriver.exe', hide=False):    
    try:        
        service=Service(chromeDriver)
        options=webdriver.ChromeOptions()  
        userAgent = UserAgent().random   # 為了搞定反爬蟲
        # print(userAgent )
        options.add_argument(f'user-agent= {userAgent}')
        if hide:
            options.add_argument('--headless')
        chrome= webdriver.Chrome(service= service, options=options)
        chrome.implicitly_wait(15)
        chrome.get(url)
        return chrome
    except Exception as e:
        print(e, "是出了什麼問題...?")    
    return "Nothing"

def find_element(chrome, xpath):
    try:
        return chrome.find_element(By.XPATH,xpath)
    except Exception as e:
        print(e, "xpath怪怪的@@")
    return "Nothing"

def get_time(hhmmss=False):
    if hhmmss:
        now_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        now_time=datetime.now().strftime('%Y-%m-%d')
        
    return now_time

def get_soup(url, post_data=None, get_data= None):
    try:
        if post_data is not None:
            resp= requests.post(url, post_data)
        elif get_data is not None:
            resp= requests.get(url, get_data)
        else:
            resp=requests.get(url)
        resp.encoding='utf-8'
        print(resp.status_code)
        if resp.status_code==200:
            return BeautifulSoup(resp.text,'lxml')        
    except Exception as e:
        print(e)
    
    return "Nothing"   
    

if __name__=='__main__':
    url='https://movies.yahoo.com.tw/chart.html'
    print(get_time(True))
    #print(get_soup(url)) 
    # print(get_chrome(url)) 


