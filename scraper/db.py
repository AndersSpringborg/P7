import wine
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd
import pathlib

wines = {
        "name": [],
        "original_name": [],
        "lwin":[],
        "original_year" : [],
        "year": [],
        "wine_offer_price":[],
        "price": []
        }


# Adds wine to record.
def add_wine(extracted_wine_obj):
    wines["name"].append(extracted_wine_obj.name)
    wines["original_name"].append(extracted_wine_obj.original_name)
    wines["lwin"].append(extracted_wine_obj.lwin)
    wines["original_year"].append(extracted_wine_obj.original_year)
    wines["year"].append(extracted_wine_obj.year)
    wines["wine_offer_price"].append(extracted_wine_obj.wine_offer_price)
    wines["price"].append(extracted_wine_obj.price)

# Stores record in .cvs file and clears wine record.
def save():
    df = pd.DataFrame(wines, columns = list(wines.keys()))

    if (pathlib.Path("wine_data").exists()):
        df.to_csv("wine_data", mode = 'a', index = False, header = False)

    else:
        df.to_csv("wine_data", index = False, header = False)

    key_list = list(wines.keys())
    wines.clear()

    for k in key_list:
        wines[k] = []
