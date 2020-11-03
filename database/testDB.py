import sqlite3
from sqlite3 import Error
import json
import urllib.request
from os import path


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_transaction(conn, transaction):
    sql = ''' INSERT INTO transactions(purchasorId, vendorId, type, lwin, wineName, volume, quantity, pricePrUnit, variantCode)
              VALUES(?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, transaction)
    conn.commit()
    return cur.lastrowid


def create_offer(conn, offer):
    sql = ''' INSERT INTO offers(id, supplierName, supplierEmail, linkedWineLwin, originalOfferText, producer, wineName, quantity, year,  price, currency, isOWC, isOC, isIB, bottlesPerCase, bottleSize, bottleSizeNumerical, region, subRegion, colour, createdAt, vendorId, pr, cbr)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    
    offer['supplierName'] = offer['offer'].supplierName
    
    cur = conn.cursor()
    cur.execute(sql, offer)
    conn.commit()
    return cur.lastrowid


def main():
    database = r"database/WineDB.db"

    sql_create_transactions_table = '''CREATE TABLE IF NOT EXISTS transactions
                                    (purchasorId VARCHAR(5),
                                    vendorId INT NOT NULL,
                                    type VARCHAR(20) NOT NULL,
                                    lwin INT NOT NULL,
                                    wineName VARCHAR(100) NOT NULL,
                                    volume VARCHAR(10),
                                    quantity INT NOT NULL,
                                    pricePrUnit REAL NOT NULL,
                                    variantCode INT NOT NULL)'''

    sql_create_offers_table = '''CREATE TABLE IF NOT EXISTS offers 
                                    (id INT NOT NULL PRIMARY KEY,
                                    supplierName VARCHAR(30),
                                    supplierEmail VARCHAR(100),
                                    linkedWineLwin INT NOT NULL,
                                    originalOfferText VARCHAR(100) NOT NULL,
                                    producer VARCHAR(30),
                                    wineName VARCHAR(100) NOT NULL,
                                    quantity INT,
                                    year INT,
                                    price REAL,
                                    currency VARCHAR(10),
                                    isOWC BOOLEAN,
                                    isOC BOOLEAN ,
                                    isIB BOOLEAN,
                                    bottlesPerCase INT,
                                    bottleSize VARCHAR(30),
                                    bottleSizeNumerical INT,
                                    region VARCHAR(30),
                                    subRegion VARCHAR(30),
                                    colour VARCHAR(30),
                                    createdAt VARCHAR(30),
                                    vendorId INT, 
                                    pr INT,
                                    cbr INT)'''

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_transactions_table)

        # create tasks table
        create_table(conn, sql_create_offers_table)

        with open('C:\Development\P7\database\wine_data.json', encoding="utf8") as offers_data:
            data = json.load(offers_data)

            for offer in data:
                if((offer['linkedWineLwin']!=None) and (offer['wineName']!=None)):
                    create_offer(conn, offer)
            # create a new project
            #offer = ('123', 'hello', '1919', '43', '32', '1')
            #create_offer(conn, offer)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()