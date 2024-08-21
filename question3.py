from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import mysql.connector
import getpass
# from sqlalchemy import create_engine

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)

url = "https://www.ccilindia.com/web/ccil/security-wise-repo-market-summary?p_l_back_url=https%3A%2F%2Fwww.ccilindia.com%2Fweb%2Fccil%2Fsecurity-wise-repo-market-summary%3Fp_l_back_url%3D%252Fweb%252Fccil%252Fsearchresult%253Fq%253Dsecurity%252Bwise"

driver = webdriver.Chrome(options=chrome_options)

driver.get(url)

table = driver.find_element(By.ID, "securityWiseRepoTable")
title_objects = driver.find_elements(By.CSS_SELECTOR, "#securityWiseRepoTable thead tr th")
titles = list(map(lambda obj : obj.text, title_objects))

last_page = driver.find_elements(By.CSS_SELECTOR, "#securityWiseRepoTable_paginate span a")[-1].text
next_page_button = driver.find_element(By.CSS_SELECTOR, "#securityWiseRepoTable_next")

data = []

for page in range(1): # change 1 to last_page
    rows = driver.find_elements(By.CSS_SELECTOR, "#securityWiseRepoTable tbody tr")
    for row in rows:
        values = list(map(lambda obj : obj.text, row.find_elements(By.CSS_SELECTOR, "*")))
        data.append(values)
    next_page_button.click()

df = pd.DataFrame(data=data, columns=titles)

mydb = mysql.connector.connect(user='root',password='password',host='localhost')

print(mydb)