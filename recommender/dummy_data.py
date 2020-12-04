import pandas as pd
import random as rand

# random value of 1 or 0 for each wine deals.
def expected_offer_row(row):
    i = rand.randint(0, 100)
    if i >= 50:
        return 1
    else:
        return 0

# a static way of creating dummy global wine price data
def static_profit(row):
    return 100

# dummy data for testing while database has not been created.
def get_dummy_data():
    df = pd.read_json("offers.json", encoding='utf-8')
    df = df.drop(df[df.wineName == ''].index)
    df = df.dropna(axis=0, subset=['linkedWineLwin'])
    df = df.drop_duplicates(subset='linkedWineLwin', keep="first")
    df['outcome'] = df.apply(lambda row: expected_offer_row(row), axis=1)
    df['globalPrice'] = df.apply(lambda row: static_profit(row), axis=1)
    return df
