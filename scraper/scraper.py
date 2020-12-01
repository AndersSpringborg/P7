import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
import pandas as pd
from wine import Wine, ExtractedWine
import sys
import db
import time
import sys
#retrieves relevant wine data from RareWines server
def get_wines_from_rare_wine():
    list_of_wine = []
    data_df = pd.read_json("https://rarewinestorage.blob.core.windows.net/rare-wine-public/wine_data.json", encoding='utf-8')
    data_df = data_df.drop(data_df[data_df.wineName == ''].index)
    data_df = data_df.dropna(axis=0, subset=['linkedWineLwin'])
    #We are only interested in the wine info and not info regarding the offer itself. By doing this we reduce the amount from 18638 to 4207.
    data_df = data_df.drop_duplicates(subset='linkedWineLwin', keep = "first")
    data_df = data_df.iloc[4000:] #will give new dataframe without first 500
    count = 0
    for index, row in data_df.iterrows():
        list_of_wine.append(Wine(row['wineName'], row['price'], row['year'], str(row['linkedWineLwin'])))
    return list_of_wine


#General webscaper class which specifies methods applicable for a generic page
class Webscaper:
    def __init__(self, wines):
        self.wines = wines
    
    #checks whether it is polite to crawl the a given url string.
    def crawl_enabled(url):
        rp=RobotFileParser()
        rp.set_url(url)
        rp.read()
        return rp.can_fetch("*",url)

#Scraper for Zachy webshop
###NOTE: has not been completed as it is no longer relevant ###
class ZachyScaper(Webscaper):

    def __init__(self, wines):
        super().__init__(wines)
    
    def crawl(self):
        for wine in self.wines:
            query = str(wine.region) + '%20' + str(wine.type)
            link_to_crawl = 'https://www.zachys.com/instantsearchplus/result/?q='+query
            r = requests.get(link_to_crawl)

#Scraper for the Wine Owners trading platform
class WineOwnerScraper(Webscaper):
    def __init__(self, wines):
        super().__init__(wines)

    #retrieves the relevant wine price information from the Wine Owners.
    def crawl(self):
        for wine in self.wines:
            wine_name = wine.name
            vintage = wine.year
            link_to_crawl = 'https://www.wineowners.com/wine-list-search.aspx?st=AW&reset=Y&name='+wine_name+'&vintage=' + str(vintage)
            r = requests.get(link_to_crawl)
            r_parse = BeautifulSoup(r.text,'html.parser')

            rows = r_parse.find_all('tbody')
            if len (rows) > 0:
             rows = rows[0].find_all('tr')
            else:
                continue
            if len(rows) > 0:
             for row in rows:
                 name_of_wine = row.find_all('a')[1].text
                 wine_year = row.find_all('td', {"class": "hidden-xs"})[0].text
                 price = row.find_all('td')[3].text
                 extracted_wine = ExtractedWine(name_of_wine, wine.name, wine.lwin, wine.year,wine_year, wine.price, price)
                 db.add_wine(extracted_wine)
            time.sleep(0.5)
        db.save()
wine_lst = get_wines_from_rare_wine()
winescrape = WineOwnerScraper(wine_lst)
winescrape.crawl()

