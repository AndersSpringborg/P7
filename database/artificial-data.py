import json
import pandas as pd
import db


def main():
    def load_offers_data():
        with open('test_offers.json', encoding="utf-8") as offers_data:
            return pd.read_json(offers_data)

    def load_transactions_data():
        return pd.read_csv('test_trans.csv')

    offers_df = load_offers_data()
    offers_df = offers_df.drop(
        offers_df[offers_df.linkedWineLwin.isnull()].index)

    transa_df = load_transactions_data()
    transa_df = transa_df.drop(transa_df[transa_df.linkedWineLwin.isnull()].index)

    df_merge = pd.merge(offers_df, transa_df, how="right", on='linkedWineLwin')
    df_offers = offers_df[offers_df.linkedWineLwin.isin(transa_df.linkedWineLwin)]
    df_transactions = transa_df[transa_df.linkedWineLwin.isin(offers_df.linkedWineLwin)]

    df_merge = df_merge.drop_duplicates(subset=['No_', 'Amount'])

    print(df_merge)
    #print(df_offers)
    #print(df_transactions)

if __name__ == '__main__':
    main()
