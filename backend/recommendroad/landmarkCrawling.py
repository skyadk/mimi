from selenium import webdriver
from bs4 import BeautifulSoup as soups
import json
import pandas as pd
import os
import shutil
from datetime import date
import urllib.request
from urllib.parse import quote

DATA_DIR = "../data"
DATA_FILE = os.path.join(DATA_DIR, "landname.json")
DUMP_FILE = os.path.join(DATA_DIR, "landname.pkl")

def search_selenium(data_path=DATA_FILE) :
    try:
        with open(data_path, encoding="utf-8") as f:
            data = json.loads(f.read())
    except FileNotFoundError as e:
        print(f"`{data_path}` 가 존재하지 않습니다.")
        exit(1)

    for d in data:
        if d['lid'] < 'l364':
             continue

        search_name = d['landmark_name']
        search_url = "https://www.google.com/search?q=" + str(search_name) + "&hl=ko&tbm=isch"
        
        browser = webdriver.Chrome('c:/chromedriver.exe')
        browser.get(search_url)
        
        #image_count = len(browser.find_elements_by_tag_name("img"))
        #print("로드된 이미지 개수 : ", image_count)
    
        browser.implicitly_wait(2)
    
        image = browser.find_elements_by_tag_name("img")[1]
        #image.screenshot("C:/Users/multicampus/Documents/s04p23d108/backend/recommendroad/landimg" + str(d['lid'])+ ".png")
        image.screenshot("c:/expression/" + str(d['lid'])+ ".png")
        print("찰칵" + d['lid'] + "저장")
        browser.close()

def main():

    print("[*] googleCrawling...")
    search_selenium()
    print("[+] Done")

if __name__ == "__main__" :
 
    # search_name = input("검색하고 싶은 키워드 : ")
    # search_limit = int(input("원하는 이미지 수집 개수 : "))
    # search_path = "Your Path"
    # search_maybe(search_name, search_limit, search_path)
    search_selenium()