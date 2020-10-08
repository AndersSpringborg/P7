import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
import pandas as pd
from wine import Wine
import sys

#need more filtering on what good wine data is
def get_wines_from_rare_wine():
    list_of_wine = []
    data_df = pd.read_json("https://rarewinestorage.blob.core.windows.net/rare-wine-public/wine_data.json", encoding='utf-8')
    data_df = data_df.drop(data_df[data_df.wineName == ''].index)
    data_df = data_df.dropna(axis=0, subset=['linkedWineLwin'])
    count = 0
    for index, row in data_df.iterrows():
        #name, region, year, producer, type
        print('wineName ' +str(row['wineName']))
        print('linkedWineLwin ' +str(row['linkedWineLwin']))
        print('producer ' +str(row['producer']))
        print('year ' +str(row['year']))
        print('region ' +str(row['region']))
        print('subRegion ' +str(row['subRegion']))
        print('colour ' +str(row['colour']))
        print(' ')
        print(' ')
        if count > 2:
            sys.exit(-1)
        count = count +1
        list_of_wine.append(Wine(row['wineName'], row['region'], row['year'], row['producer'], row['type']))
    return list_of_wine



class Webscaper:
    def __init__(self, wines):
        self.wines = wines
    
    def crawl_enabled(url):
        rp=RobotFileParser()
        rp.set_url(url)
        rp.read()
        return rp.can_fetch("*",url)

class ZachyScaper(Webscaper):

    def __init__(self):
        super().__init__()
    
    def crawl(self):
        for wine in self.wines:
            query = str(wine.region) + '%20' + str(wine.type)
            link_to_crawl = 'https://www.zachys.com/instantsearchplus/result/?q='+query
            r = requests.get(link_to_crawl)

class WineOwnerScraper(Webscaper):
    def __init__(self):
        super.__init__()

    def crawl(self):
        for wine in self.wines:
            wine_name = wine.name
            vintage = wine.year
            link_to_crawl = 'https://www.wineowners.com/wine-list-search.aspx?st=AW&reset=Y&name='+wine_name+'&vintage=' + str(vintage)
            r = requests.get(link_to_crawl)
            r_parse = BeatifulSoup(r.text,'html.parser')
            for a in r_parse.find_all('tbody'):
                pass
                #a is the only table in the list travers this to get data and link for further information.

