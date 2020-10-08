import wine
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd
import pathlib

wines = {
        "Name": [],
        "Price": [],
        "Region": [],
        "Year": [],
        "CriticsScore": [],
        "Producer": [],
        "Type": [],
        "Volume": [],
        "Lwin": []
        }

# Adds wine to record.
def add_wine(wine_obj):
    wines["Name"].append(wine_obj.name)
    wines["Price"].append(wine_obj.price)
    wines["Region"].append(wine_obj.region)
    wines["Year"].append(wine_obj.year)
    wines["CriticsScore"].append(wine_obj.critics_score)
    wines["Producer"].append(wine_obj.producer)
    wines["Type"].append(wine_obj.type)
    wines["Volume"].append(wine_obj.volume)
    wines["Lwin"].append(wine_obj.linkedWineLwin)

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
