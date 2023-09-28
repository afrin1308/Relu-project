## Installing Necessary Packages


pip install xlrd

pip install pandas


pip install selenium

pip install webdriver-manager

pip install lxml


import pandas as pd
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup, SoupStrainer
import re


## Read excel files with pandas

sheet_id='1BZSPhk1LDrx8ytywMHWVpCqbm8URTxTJrIRkD7PnGTM'
df=pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
df      

## Creating a dataframe for product details

#https://www.amazon.{country}/dp/{asin}
asin=df['Asin']
code=df['country']
column=['product_name','product_price','product_detail','product_url']
Product=pd.DataFrame(columns=column)





## Scraping webpages from the url's, which are extracted through the given google spreadsheet

for i in range(105):
    url="https://www.amazon.{}/dp/{}".format(code[i],asin[i])
    try:
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(url)
        soup = BeautifulSoup(driver.page_source,"html.parser")
        #print(soup.prettify())
        #dict_from_json = json.loads(soup.find("body").text)
        name= driver.find_element(By.XPATH,"//span[contains(@id,'productTitle')]")
        price= driver.find_element(By.XPATH,"//span[contains(@class,'a-size-base a-color-price a-color-price')] | //span[contains(@class,'a-price-whole')]" )
        img_url=WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//span[@class='a-list-item']/span[@class='a-declarative']/div[@class='imgTagWrapper']/img[@class='a-dynamic-image a-stretch-horizontal'] | //div[@class='a-row a-spacing-mini a-spacing-top-micro']/span[@class='a-declarative']/div[contains(@class,'a-column a-span3 a-spacing-micro imageThumb thumb')]/img"))).get_attribute("src")
        detail= driver.find_element(By.XPATH,"//span[contains(@class,'a-list-item')] | //div[contains(@class,'a-section a-spacing-small a-padding-base')] ")
        Product=Product.append({'product_name':name.text,'product_price':price.text,'product_detail':detail.text,'product_url':img_url },ignore_index=True)
        
                
                

        
    except:
        Product=Product.append({'product_name' : "url not available"},ignore_index=True)
        continue
        
Product       
        
        



top_product=Product.head(30)
top_product



Product.dropna()

df2 = Product.to_json(orient = 'columns')
print(df2)









