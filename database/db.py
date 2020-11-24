import sqlite3
import pandas as pd
import json
import flask as flask


class SQL_Wineoffer:
    def __init__(self, offerId, supplierName, supplierEmail, linkedWineLwin, originalOfferText, producer, wineName, quantity, year, price, currency, isOWC, isOC, isIB, bottlesPerCase, bottleSize, bottleSizeNumerical, region, subRegion, colour, createdAt, wine_id):
        self.offerId = offerId
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
        self.id = wine_id


class Transaction_Class:
    def __init__(self, vendorId, postingGroup, number, lwinnumber, description, measurementunit, quantity, directunitcost, amount, variantcode, postingdate, purchaseinitials):
        self.vendorId = vendorId
        self.postingGroup = postingGroup
        self.number = number
        self.lwinnumber = lwinnumber
        self.description = description
        self.measurementunit = measurementunit
        self.quantity = quantity
        self.directunitcost = directunitcost
        self.amount = amount
        self.variantcode = variantcode
        self.postingdate = postingdate
        self.purchaseinitials = purchaseinitials


class wine_db:
    def __init__(self, filename="wine.db"):

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
                                    (offerId VARCHAR(50),
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
                                    id VARCHAR(50))''')
        self.connection.commit()
        self.connection.close()

    def __del__(self):
        if (self.connection != None):
            self.connection.close()

    def open_connection(self, filename="wine.db"):
        self.connection = sqlite3.connect(filename)

    def empty(self):
        self.open_connection()
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM offers")
        row = cursor.fetchone()
        self.connection.close()

        return row == None

    def get_all_offers(self):
        if (self.connection == None):
            raise Exception("Wine database is closed.")

        self.open_connection()

        self.connection.row_factory = sqlite3.Row
        c = self.connection.cursor()
        rows = c.execute('select * from offers').fetchall()

        self.connection.close()

        return flask.jsonify([dict(ix) for ix in rows])

    def get_all_transactions(self):
        if (self.connection == None):
            raise Exception("Wine database is closed.")

        self.open_connection()

        self.connection.row_factory = sqlite3.Row
        c = self.connection.cursor()
        rows = c.execute('select * from transactions').fetchall()

        self.connection.close()

        return flask.jsonify([dict(ix) for ix in rows])

    def get_offers_from_timestamp(self, timestamp):
        if (self.connection == None):
            raise Exception("Wine database is closed.")

        self.open_connection()

        self.connection.row_factory = sqlite3.Row
        c = self.connection.cursor()
        rows = c.execute(
            "SELECT * FROM offers WHERE createdAt>=?;", [timestamp]).fetchall()

        self.connection.close()

        return flask.jsonify([dict(ix) for ix in rows])

    def get_offer_by_id(self, id):
        if (self.connection == None):
            raise Exception("Wine database is closed.")

        self.open_connection()

        self.connection.row_factory = sqlite3.Row
        c = self.connection.cursor()
        rows = c.execute(
            "SELECT * FROM offers WHERE id=?;", [id]).fetchall()

        self.connection.close()

        return flask.jsonify([dict(ix) for ix in rows])

    def add_wineoffers(self, sql_wineoffers):
        if (self.connection == None):
            raise Exception("Wine database is closed.")

        self.open_connection()

        for wine in sql_wineoffers:
            print("Inserting wine: " + wine.originalOfferText +
                  " with ID: " + wine.offerId)
            cursor = self.connection.cursor()
            cursor.execute('''INSERT OR IGNORE INTO offers(
                                              offerId,
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
                                              id)
                                              VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (wine.offerId, wine.supplierName, wine.supplierEmail, wine.linkedWineLwin, wine.originalOfferText, wine.producer, wine.wineName, wine.quantity, wine.year, wine.price, wine.currency, wine.isOWC, wine.isOC, wine.isIB, wine.bottlesPerCase, wine.bottleSize, wine.bottleSizeNumerical, wine.region, wine.subRegion, wine.colour, wine.createdAt, wine.id))
            self.connection.commit()

        self.connection.close()

    def add_transactions_data(self, transactions):
        if (self.connection == None):
            raise Exception("Wine database is closed.")

        self.open_connection()

        for transaction in transactions:
            print("Inserting Transaction with description: " +
                  transaction.description)

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
                                              VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''', (transaction.vendorId, transaction.postingGroup, transaction.number, transaction.lwinnumber, transaction.description, transaction.measurementunit, transaction.quantity, transaction.directunitcost, transaction.amount, transaction.variantcode, transaction.postingdate, transaction.purchaseinitials))
            self.connection.commit()

        self.connection.close()

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

    def clean_transactions_data(self, transaction):
        returnTransaction = None

        if transaction['LWIN No_'] is None or transaction['LWIN No_'] == "":
            return returnTransaction

        returnTransaction = transaction
        return returnTransaction


def main():
    def load_offers_data():
        with open('test_offers.json', encoding="utf-8") as offers_data:
            return json.load(offers_data, strict=False)

    def load_transactions_data():
        csv_data_df = pd.read_csv('test_trans.csv')
        return csv_data_df.to_dict(orient='record')

    def create_sqlwine(offer):
        return SQL_Wineoffer(offer['offer']['id'], offer['offer']['supplierName'], offer['offer']['supplierEmail'], offer['linkedWineLwin'], offer['originalOfferText'], offer['producer'], offer['wineName'], offer['quantity'], offer['year'], offer['price'], offer['currency'], offer['isOWC'], offer['isOC'], offer['isIB'], offer['bottlesPerCase'], offer['bottleSize'], offer['bottleSizeNumerical'], offer['region'], offer['subRegion'], offer['colour'], offer['createdAt'], offer['id'])

    def create_transactionobj(transaction):
        return Transaction_Class(transaction['Vendor Id'], transaction['Posting Group'], transaction['No_'], transaction['LWIN No_'], transaction['Description'], transaction['Unit of Measure'],
                                 transaction['Quantity'], transaction['Direct Unit Cost'], transaction['Amount'], transaction['Variant Code'], transaction['Posting Date'], transaction['Purchase Initials'])

    db = wine_db()

    offers_data = load_offers_data()
    transactions_data = load_transactions_data()

    wines = []
    for offer in offers_data:
        current_offer = db.clean_offers_data(offer)
        if current_offer is not None:
            wines.append(create_sqlwine(current_offer))

    transactions = []
    for transaction in transactions_data:
        current_transaction = db.clean_transactions_data(transaction)
        if current_transaction is not None:
            transactions.append(create_transactionobj(transaction))

    db.add_wineoffers(wines)
    db.add_transactions_data(transactions)


if __name__ == '__main__':
    main()
