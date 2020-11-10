import sqlite3
import pandas as pd
import json
import flask as flask


class SQL_Wineoffer:
    def __init__(self, wine_id, supplierName, supplierEmail, linkedWineLwin, originalOfferText, producer, wineName, quantity, year, price, currency, isOWC, isOC, isIB, bottlesPerCase, bottleSize, bottleSizeNumerical, region, subRegion, colour, createdAt, vendorId):
        self.id = wine_id
        self.supplierName = supplierName
        self.supplierEmail = supplierEmail
        self.linkedWineLwin = linkedWineLwin
        self.originalOfferText = originalOfferText
        self.producer = producer
        self.wineName = wineName
        self.quantity = quantity
        self.year = year
        self.price = price
        self.currency = currency
        self.isOWC = isOWC
        self.isOC = isOC
        self.isIB = isIB
        self.bottlesPerCase = bottlesPerCase
        self.bottleSize = bottleSize
        self.bottleSizeNumerical = bottleSizeNumerical
        self.region = region
        self.subRegion = subRegion
        self.colour = colour
        self.createdAt = createdAt
        self.vendorId = vendorId


class wine_db:
    def __init__(self, filename="wine.db"):
        self.columns_transactions = ['purchasorId', 'vendorId', 'type', 'lwin',
                                     'wineName', 'volume', 'quantity', 'pricePrUnit', 'variantCode']
        self.columns_offers = ['id', 'supplierName', 'supplierEmail', 'linkedWineLwin',
                               'originalOfferText', 'producer', 'wineName',  'quantity',
                               'year', 'price', 'currency', 'isOWC', 'isOC', 'isIB', 'bottlesPerCase',
                               'bottleSize', 'bottleSizeNumerical', 'region', 'subRegion', 'colour', 'createdAt', 'vendorId', 'pr', 'cbr']

        self.open_connection()

        self.connection.execute('''CREATE TABLE IF NOT EXISTS transactions
                                    (vendorId INT NOT NULL,
                                    postingGroup VARCHAR(20) NOT NULL,
                                    number VARCHAR(20) NOT NULL,
                                    lwinnumber VARCHAR(20),
                                    description VARCHAR(20),
                                    measurementunit VARCHAR(20),
                                    quantity REAL,
                                    directunitcost REAL,
                                    amount REAL,
                                    variantcode INT,
                                    postingdate DATETIME,
                                    purchaseinitials VARCHAR(5))''')

        self.connection.execute('''CREATE TABLE IF NOT EXISTS offers
                                    (id VARCHAR(50),
                                    supplierName VARCHAR(30),
                                    supplierEmail VARCHAR(100),
                                    linkedWineLwin VARCHAR(50),
                                    originalOfferText VARCHAR(100),
                                    producer VARCHAR(30),
                                    wineName VARCHAR(100),
                                    quantity INT,
                                    year INT,
                                    price REAL,
                                    currency VARCHAR(10),
                                    isOWC BOOL,
                                    isOC BOOL,
                                    isIB BOOL,
                                    bottlesPerCase INT,
                                    bottleSize VARCHAR(30),
                                    bottleSizeNumerical INT,
                                    region VARCHAR(30),
                                    subRegion VARCHAR(30),
                                    colour VARCHAR(30),
                                    createdAt DATETIME,
                                    vendorId VARCHAR(50))''')
        self.connection.commit()
        self.close()

    def __del__(self):
        if (self.connection != None):
            self.connection.close()

    # Re-opens database connection.
    def open_connection(self, filename="wine.db"):
        self.connection = sqlite3.connect(filename)

    # Closes database.
    def close(self):
        if (self.connection != None):
            self.connection.close()

    # Checks whether database is empty.
    def empty(self):
        self.open_connection()
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM offers")
        row = cursor.fetchone()
        self.close()

        return row == None

    # Retrieves all entries from the offers table.
    def get_all_offers(self):
        if (self.connection == None):
            raise Exception("Wine database is closed.")

        self.open_connection()

        self.connection.row_factory = sqlite3.Row
        c = self.connection.cursor()
        rows = c.execute('select * from offers').fetchall()

        self.connection.commit()
        self.connection.close()

        return json.dumps([dict(ix) for ix in rows])

    # Retrieves all entries from the transactions table.
    def get_all_transactions(self):
        if (self.connection == None):
            raise Exception("Wine database is closed.")

        self.open_connection()

        self.connection.row_factory = sqlite3.Row
        c = self.connection.cursor()
        rows = c.execute('select * from transactions').fetchall()

        return json.dumps([dict(ix) for ix in rows])

    # Retrieves offers after a given timestamp.
    def get_offers_from_timestamp(self, timestamp):
        if (self.connection == None):
            raise Exception("Wine database is closed.")

        self.open_connection()

        self.connection.row_factory = sqlite3.Row
        c = self.connection.cursor()
        rows = c.execute(
            "SELECT * FROM offers WHERE createdAt>=?;", [timestamp]).fetchall()

        return flask.jsonify([dict(ix) for ix in rows])

    def clear_offers_table(self):
        self.open_connection()
        self.connection.execute("DELETE FROM * offers")
        self.connection.commit()
        self.close()

    def add_wineoffers(self, sql_wineoffers):
        if (self.connection == None):
            raise Exception("Wine database is closed.")

        self.open_connection()

        for wine in sql_wineoffers:
            print("Inserting wine: " + wine.originalOfferText +
                  " with ID: " + wine.id)
            cursor = self.connection.cursor()
            cursor.execute('''INSERT OR IGNORE INTO offers(
                                              id,
                                              supplierName,
                                              supplierEmail,
                                              linkedWineLwin,
                                              originalOfferText,
                                              producer,
                                              wineName,
                                              quantity,
                                              year,
                                              price,
                                              currency,
                                              isOWC,
                                              isOC,
                                              isIB,
                                              bottlesPerCase,
                                              bottleSize,
                                              bottleSizeNumerical,
                                              region,
                                              subRegion,
                                              colour,
                                              createdAt,
                                              vendorId)
                                              VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (wine.id, wine.supplierName, wine.supplierEmail, wine.linkedWineLwin, wine.originalOfferText, wine.producer, wine.wineName, wine.quantity, wine.year, wine.price, wine.currency, wine.isOWC, wine.isOC, wine.isIB, wine.bottlesPerCase, wine.bottleSize, wine.bottleSizeNumerical, wine.region, wine.subRegion, wine.colour, wine.createdAt, wine.vendorId))

        self.connection.commit()
        self.close()

    def add_transactions_data(self, transactions):
        if (self.connection == None):
            raise Exception("Wine database is closed.")

        self.open_connection()

        for transaction in transactions:
            print("Inserting transaction with description: " +
                  transaction['Description'])
            cursor = self.connection.cursor()
            cursor.execute('''INSERT OR IGNORE INTO transactions(
                                              vendorId,
                                              postingGroup,
                                              number,
                                              lwinnumber,
                                              description,
                                              measurementunit,
                                              quantity,
                                              directunitcost,
                                              amount,
                                              variantcode,
                                              postingdate,
                                              purchaseinitials
                                              )
                                              VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''', (transaction['Vendor Id'], transaction['Posting Group'], transaction['No_'], transaction['LWIN No_'], transaction['Description'], transaction['Unit of Measure'], transaction['Quantity'], transaction['Direct Unit Cost'], transaction['Amount'], transaction['Variant Code'], transaction['Posting Date'], transaction['Purchase Initials']))

        self.connection.commit()
        self.close()

    def clean_offers_data(self, offer):
        returnOffer = None

        if offer['wineName'] is None or offer['wineName'] == "":
            return returnOffer

        if offer['year'] is None or offer['year'] == "":
            return returnOffer

        if offer['linkedWineLwin'] is None or offer['linkedWineLwin'] == "":
            return returnOffer

        returnOffer = offer
        return returnOffer

    def clean_transactions_data(self, transactions):
        return [i for i in transactions if i['LWIN No_'] != ""]


def main():
    def load_offers_data():
        with open('test_offers.json', encoding="utf-8") as offers_data:
            return json.load(offers_data, strict=False)

    def load_transactions_data():
        csv_data_df = pd.read_csv('test_trans.csv')
        return csv_data_df.to_dict(orient='record')

    def create_sqlwine(offer):
        return SQL_Wineoffer(offer['offer']['id'], offer['offer']['supplierName'], offer['offer']['supplierEmail'], offer['linkedWineLwin'], offer['originalOfferText'], offer['producer'], offer['wineName'], offer['quantity'], offer['year'], offer['price'], offer['currency'], offer['isOWC'], offer['isOC'], offer['isIB'], offer['bottlesPerCase'], offer['bottleSize'], offer['bottleSizeNumerical'], offer['region'], offer['subRegion'], offer['colour'], offer['createdAt'], offer['id'])

    db = wine_db()
    wines = []
    offers_data = load_offers_data()

    # Inserting offers
    for offer in offers_data:
        current_offer = db.clean_offers_data(offer)
        if current_offer is not None:
            wines.append(create_sqlwine(current_offer))

    db.add_wineoffers(wines)

    # Inserting transcations
    transactions_data = load_transactions_data()
    db.add_transactions_data(
        db.clean_transactions_data(transactions_data))

    # Pretty print get all offers
    json_object = json.loads(db.get_all_offers())
    offers_formated_json = json.dumps(json_object, indent=2)
    print(offers_formated_json)

    # Pretty print get all offers from timestamp
    json_object = json.loads(
        db.get_offers_from_timestamp('2020-02-01'))

    offers_from_timestamp_formated_json = json.dumps(json_object, indent=2)
    print(offers_from_timestamp_formated_json)


if __name__ == '__main__':
    main()
