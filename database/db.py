import sqlite3
import pandas as pd
import json
import flask

class System_Object:
    def tostring():
        return None

class Global_Price(System_Object):
    def __init__(self, lwin_fk, price, date):
        self.lwin = lwin_fk
        self.price = price
        self.date = date

    @staticmethod
    def from_json(jstr):
        return Global_Price(jstr['lwin_fk'], jstr['price'], jstr['date'])

    def tostring(self):
        return '[' + str(self.lwin) + ', ' + str(self.price) + ', ' + str(self.date) + ']'

class Offer_Class(System_Object):
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

    def tostring():
        return "Not implemented"


class Transaction_Class(System_Object):
    def __init__(self, vendorId, postingGroup, number, lwinnumber, description, measurementunit, quantity, directunitcost, amount, variantcode, postingdate, purchaseinitials, offers_FK):
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
        self.offers_FK = offers_FK

    def tostring():
        return "Not implemented"

class wine_db:
    def __init__(self, filename="wine.db"):

        self.open_connection()

        self.connection.execute('''CREATE TABLE IF NOT EXISTS transactions
                                    (transactions_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    vendorId INT NOT NULL,
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
                                    purchaseinitials VARCHAR(5),
                                    offers_FK VARCHAR(36) UNIQUE NOT NULL,
                                    FOREIGN KEY(offers_FK) REFERENCES offers(id)
                                    )''')

        self.connection.execute('''CREATE TABLE IF NOT EXISTS offers
                                    (offerId VARCHAR(36),
                                    supplierName VARCHAR(30),
                                    supplierEmail VARCHAR(50),
                                    linkedWineLwin VARCHAR(36),
                                    originalOfferText VARCHAR(100),
                                    producer VARCHAR(50),
                                    wineName VARCHAR(50),
                                    quantity INT,
                                    year INT,
                                    price REAL,
                                    currency VARCHAR(5),
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
                                    id VARCHAR(36) PRIMARY KEY)''')

        self.connection.execute('''CREATE TABLE IF NOT EXISTS svm
                                    (offers_FK VARCHAR(36) UNIQUE NOT NULL,
                                    FOREIGN KEY(offers_FK) REFERENCES offers(id)
                                    )''')

        self.connection.execute('''CREATE TABLE IF NOT EXISTS nb
                                    (offers_FK VARCHAR(36) UNIQUE NOT NULL,
                                    FOREIGN KEY(offers_FK) REFERENCES offers(id)
                                    )''')

        self.connection.execute('''CREATE TABLE IF NOT EXISTS logit
                                    (offers_FK VARCHAR(36) UNIQUE NOT NULL,
                                    FOREIGN KEY(offers_FK) REFERENCES offers(id)
                                    )''')

        self.connection.execute('''CREATE TABLE IF NOT EXISTS price_difference
                                    (offers_FK VARCHAR(36) UNIQUE NOT NULL,
                                    price_difference REAL(50) NOT NULL,
                                    FOREIGN KEY(offers_FK) REFERENCES offers(id)
                                    )''')

        self.connection.execute('''CREATE TABLE IF NOT EXISTS global_price
                                    (LWIN_FK VARCHAR(36),
                                    global_price REAL(50),
                                    date DATETIME,
                                    PRIMARY KEY(LWIN_FK, date)
                                    )''')

        self.connection.commit()
        self.connection.close()

    def __del__(self):
        if (self.connection != None):
            self.connection.close()

    # Open a connection.
    # Should be used whenever we operate on the database.
    def open_connection(self, filename="wine.db"):
        self.connection = sqlite3.connect(filename)

    # Check offers for being empty.
    # This is deprecated, since we need to check transactions for being empty as well.
    def empty(self):
        self.open_connection()
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM offers")
        row = cursor.fetchone()
        self.connection.close()

        return row == None

    # All offers left outer joined with global_price on their LWIN (we don't want offers.price to match global_price.price).
    def get_all_offers(self):
        if (self.connection == None):
            raise Exception("Wine database is closed.")

        self.open_connection()

        self.connection.row_factory = sqlite3.Row
        c = self.connection.cursor()
        rows = c.execute('''SELECT *
                            FROM offers LEFT OUTER JOIN global_price ON offers.linkedWineLwin=global_price.LWIN_FK''').fetchall()
        self.connection.close()
        return flask.jsonify([dict(ix) for ix in rows])

    # Returns all stored transactions.
    def get_all_transactions(self):
        if (self.connection == None):
            raise Exception("Wine database is closed.")

        self.open_connection()

        self.connection.row_factory = sqlite3.Row
        c = self.connection.cursor()
        rows = c.execute('SELECT * FROM transactions').fetchall()

        self.connection.close()

        return flask.jsonify([dict(ix) for ix in rows])

    # Finds all offers in offers created at a latter timestamp than given argument.
    # Offers are left outer joined with these transactions to make sure every offer is returned.
    def get_offers_from_timestamp(self, timestamp):
        if (self.connection == None):
            raise Exception("Wine database is closed.")

        self.open_connection()

        self.connection.row_factory = sqlite3.Row
        c = self.connection.cursor()
        rows = c.execute('''SELECT *
                            FROM offers LEFT OUTER JOIN (
                                SELECT transactions_id, offers_FK
                                FROM transactions
                            ) AS transactions ON offers.id=transactions.offers_FK
                            WHERE offers.createdAt>=?''', [timestamp]).fetchall()

        self.connection.close()

        return flask.jsonify([dict(ix) for ix in rows])

    # Finds speficic offer entity given ID in offers.
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

    # JSON object containing recommendations from each recommender algorithm.
    def get_recommendation(self):
        return flask.jsonify({
            "svm": self.__get_svm_recommendation(),
            "nb": self.__get_nb_recommendation(),
            "logit": self.__get_lr_recommendation()
        })

    # Right outer joins relation SVM with relation offers.
    # This makes sure every entity in SVM is joined. If an entity in SVM can't be joined, its attributes from offers are None.
    def __get_svm_recommendation(self):
        if (self.connection == None):
            raise Exception("Wine database is closed.")

        self.open_connection()

        self.connection.row_factory = sqlite3.Row
        c = self.connection.cursor()
        rows = c.execute('''SELECT *
                            FROM (offers LEFT OUTER JOIN svm ON svm.offers_FK=offers.id) AS o
                                        LEFT OUTER JOIN price_difference ON o.id=price_difference.offers_FK''').fetchall()

        self.connection.close()
        return [dict(ix) for ix in rows]

    # Right outer joins relation NB with relation offers.
    # This makes sure every entity in NB is joined. If an entity in NB can't be joined, its attributes from offers are None.
    def __get_nb_recommendation(self):
        if (self.connection == None):
            raise Exception("Wine database is closed.")

        self.open_connection()

        self.connection.row_factory = sqlite3.Row
        c = self.connection.cursor()
        rows = c.execute('''SELECT *
                            FROM (offers LEFT OUTER JOIN nb ON nb.offers_FK=offers.id) AS o
                                        LEFT OUTER JOIN price_difference ON o.id=price_difference.offers_FK''').fetchall()

        self.connection.close()
        return [dict(ix) for ix in rows]

    # Right outer joins relation LR with relation offers.
    # This makes sure every entity in LR is joined. If an entity in LR can't be joined, its attributes from offers are None.
    def __get_lr_recommendation(self):
        if (self.connection == None):
            raise Exception("Wine database is closed.")

        self.open_connection()

        self.connection.row_factory = sqlite3.Row
        c = self.connection.cursor()
        rows = c.execute('''SELECT *
                            FROM (offers LEFT OUTER JOIN logit ON logit.offers_FK=offers.id) AS o
                                        LEFT OUTER JOIN price_difference ON o.id=price_difference.offers_FK''').fetchall()

        self.connection.close()
        return [dict(ix) for ix in rows]

    # TODO: Test this!
    # Adds wine offer IDs into appropriate recommender relation.
    # Adds price difference.
    def add_recommendations(self, json_result):
        if (self.connection == None):
            raise Exception("Wine database is closed.")

        self.open_connection()

        for result in json_result['Results']:
            print("Inserting recommendation for wine " + str(result['id']))
            cursor = self.connection.cursor()

            if (int(result['cb_outcome']) > 0):
                cursor.execute('INSERT OR IGNORE INTO ' + json_result['model_type'] + '''(
                                offers_FK)
                                VALUES(?)''', [str(result['id'])])

            cursor.execute('''INSERT OR IGNORE INTO price_difference(
                                offers_FK,
                                price_difference)
                                VALUES(?,?)''', (str(result['id']), result['price_diff']))

        self.connection.commit()
        self.connection.close()

    # Adds global prices into its relation.
    def add_global_prices(self, prices):
        if (self.connection == None):
            raise Exception("Wine database is closed.")

        self.open_connection()

        for price in prices:
            print("Inserting global price: " + price.tostring())
            cursor = self.connection.cursor()
            cursor.execute('''INSERT OR IGNORE INTO global_price(
                                            LWIN_FK,
                                            global_price,
                                            date)
                                            VALUES(?,?,?)''', (price.lwin, price.price, price.date))

        self.connection.commit()
        self.connection.close()

    # Adds wine offers into its relation.
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

    # Add transactions into its relation.
    def add_transactions_data(self, transactions):
        if (self.connection == None):
            raise Exception("Wine database is closed.")

        self.open_connection()

        for transaction in transactions:
            print("Inserting Transaction with description: " +
                  str(transaction.description))

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
                                              purchaseinitials,
                                              offers_FK
                                              )
                                              VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', (transaction.vendorId, transaction.postingGroup, transaction.number, transaction.lwinnumber, transaction.description, transaction.measurementunit, transaction.quantity, transaction.directunitcost, transaction.amount, transaction.variantcode, transaction.postingdate, transaction.purchaseinitials, transaction.offers_FK))
        
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

    # Initializer of Offer_class given JSON instance.
    def create_offer_obj(self, offer):
        return Offer_Class(offer['offer']['id'], offer['offer']['supplierName'], offer['offer']['supplierEmail'], offer['linkedWineLwin'], offer['originalOfferText'], offer['producer'], offer['wineName'], offer['quantity'], offer['year'], offer['price'], offer['currency'], offer['isOWC'], offer['isOC'], offer['isIB'], offer['bottlesPerCase'], offer['bottleSize'], offer['bottleSizeNumerical'], offer['region'], offer['subRegion'], offer['colour'], offer['createdAt'], offer['id'])

    # Initializer of Transaction_Class given JSON instance.
    def create_transaction_obj(self, transaction):
        return Transaction_Class(transaction['Vendor Id'], transaction['Posting Group'], transaction['No_'], transaction['LWIN No_'], transaction['Description'], transaction['Unit of Measure'],
                                 transaction['Quantity'], transaction['Direct Unit Cost'], transaction['Amount'], transaction['Variant Code'], transaction['Posting Date'], transaction['Purchase Initials'], transaction['id'])
    
    def create_artificial_offer_obj(self, offer_df_row):
        return Offer_Class(str(offer_df_row['id']), 'supplierNameArtificial', 'supplier@articial.com', offer_df_row['LWIN No_'], offer_df_row['originalOfferText'], offer_df_row['producer'], offer_df_row['wineName'], offer_df_row['quantity'], offer_df_row['year'], offer_df_row['price'], offer_df_row['currency'], offer_df_row['isOWC'], offer_df_row['isOC'], offer_df_row['isIB'], offer_df_row['bottlesPerCase'], offer_df_row['bottleSize'], offer_df_row['bottleSizeNumerical'], offer_df_row['region'], offer_df_row['subRegion'], offer_df_row['colour'], offer_df_row['createdAt'], str(offer_df_row['offer']['id']))