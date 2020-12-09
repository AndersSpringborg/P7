import json
import pandas as pd
import db as database
import uuid

def main():
    db = database.wine_db()

    def load_offers_data():
        with open('test_offers.json', encoding="utf-8") as offers_data:
            return pd.read_json(offers_data)

    def load_transactions_data():
        return pd.read_csv('test_trans.csv')

    offers_df = load_offers_data()
    offers_df.rename(columns={'linkedWineLwin': 'LWIN No_'}, inplace=True)

    offers_df = offers_df.drop(
        offers_df[offers_df['LWIN No_'].isnull()].index)
    offers_df = offers_df.drop(
        offers_df[offers_df['wineName'] == ""].index)
    offers_df = offers_df.drop(
        offers_df[offers_df['region'].isnull()].index)

    transa_df = load_transactions_data()
    transa_df = transa_df.drop(transa_df[transa_df['LWIN No_'].isnull()].index)
    

    trans_offer_df = pd.merge(offers_df, transa_df, how="left", on='LWIN No_')
    trans_offer_df = trans_offer_df.drop_duplicates(subset=['No_', 'Amount'])

    artificial_offers = []
    artificial_trans = []

    for index, row in trans_offer_df.iterrows():
        row['id'] = uuid.uuid4()

        artificial_offers.append(db.create_artificial_offer_obj(row))
        artificial_trans.append(db.create_transaction_obj(row))

    db.add_wineoffers(artificial_offers)
    db.add_transactions_data(artificial_trans)

if __name__ == '__main__':
    main()