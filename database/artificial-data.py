import json
import pandas as pd

def main():
    def load_offers_data():
        with open('test_offers.json', encoding="utf-8") as offers_data:
            return pd.read_json(offers_data)

    def load_transactions_data():
        return pd.read_csv('test_trans.csv')

    offers_df = load_offers_data()
    offers_df = offers_df.drop(offers_df[offers_df.linkedWineLwin.isnull()].index)
    print(offers_df)
    transa_df = load_transactions_data()

    df = pd.merge(offers_df, transa_df, how="inner", on='linkedWineLwin')

    print(df)
    

if __name__ == '__main__':
    main()