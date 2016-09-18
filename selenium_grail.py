import time
import sqlite3
from selenium import webdriver
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
from numpy import nan as NA
from pandas.io import sql
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import telepot
from pprint import pprint


class Grailed:
    def __init__(self, host, target_brand):
        self.host = host
        self.target_brand = target_brand
        self.driver = webdriver.Chrome() 
        self.df = DataFrame(columns=['brand', 'category', 'desc', 'size', 'price', 'img', 'link'])
        self.token = "283346046:AAECp_TRKwCUJ1E6Xf9sVSBRHtDVzM7aHjE"
        self.dodo = 118931446
        self.bot = telepot.Bot(self.token)

    def set_db(self, db):
        self.db = db

    def categorize(self, size):
        tee = ['xs', 's', 'm', 'l', 'xl', 'xxl']
        try:
            int(size)
        except ValueError:
            if size in tee:
                return "Tee"
            if size == 'os':
                return "Others"
        else:
            if 5 < int(size) < 18:
                return "Shoes"
            else:
                return "Pants"

    def num_pages(self, pages):
        for i in range(pages):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5) # Let the user actually see something!

    def load_page(self, pages):
        self.driver.get(self.host)
        time.sleep(1) 
        self.num_pages(pages)

    def parse_data(self):
        temp_df = DataFrame(columns=['brand', 'category', 'desc', 'size', 'price', 'img', 'link'])
        res = self.driver.page_source
        soup = BeautifulSoup(res, 'lxml')

        items = soup.find_all('div', attrs={'class':'feed-item'})
        i = 0
        for item in items:
            brand = item.find_all('h2', attrs={'class':'listing-designer'})
            img = item.find_all('img')
            listing_title = item.find_all('h3', attrs={'class':'listing-title'})
            listing_size = item.find_all('h2', attrs={'class':'listing-size'})
            price = item.find_all('h2', attrs={'class':'original-price'})
            link = item.find_all('a')
            if not len(brand):                # or brand[0].text not in target_brand:
                continue
            if int(price[0].span.text[1:]) >= 200:
                continue
            temp_df.loc[i] = [brand[0].text, self.categorize(listing_size[0].text),  listing_title[0].text, listing_size[0].text, int(price[0].span.text[1:]), img[0]['src'], link[0]['href']]
            i += 1

            # print(brand[0].text)
            # print(listing_title[0].text)
            # print(listing_size[0].text)
            # print(int(price[0].span.text[1:]))
            # print(img[0]['src'])
            # print()
        self.df = self.df.append(temp_df)

    def print_df(self):
        print(self.df)

    def db_update(self):
        sql.to_sql(self.df, name='Items', con=self.db.con, if_exists='append')

    def search(self, brand, low=0, high=200):
        results = self.df[self.df['brand'] == brand]
        for text in results['link']:
            self.sendMsg(self.host + text)
        # self.sendMsg(text for text in results['price']) #and self.df['price'] < high])
        # print(self.df.query('brand == "{0}".format(brand)'))# & price > 0 & price < 200'))#

    def sendMsg(self, message):
        self.bot.sendMessage(self.dodo, message)

    def run(self, pages):
        self.load_page(pages)
        self.parse_data()
        self.driver.quit()
        self.print_df()
        self.search('Supreme')
        # self.db_update()
        # self.print_df()
        
class Database:
    def __init__(self, name):
        self.con = sqlite3.connect(name)

    def db_print(self):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM Items")
        for i in cur:
            print(i)

    

db_name = "database.db"
host = 'https://www.grailed.com'
target_brand = ["Supreme", "Y-3"]
pages = 4
    
# db = Database(db_name)
grailed = Grailed(host, target_brand)
grailed.run(pages)
# db.db_print()
