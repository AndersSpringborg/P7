import sqlite3
import pandas as pd

# Wine database class.
class wine_db:
    def __init__(self, filename = "wine.db"):
        self.columns_transactions = ['purchasorId', 'vendorId', 'type', 'wineName', 'volume', 'quantity', 'pricePrUnit', 'variantCode']
        self.columns_offers = ['id', 'name', 'lwin', 'vendorId', 'pr', 'cbr']

        self.reopen()

        self.connection.execute('''CREATE TABLE IF NOT EXISTS transactions
                            (purchasorId VARCHAR(5),
                            vendorId INT NOT NULL,
                            type VARCHAR(20) NOT NULL,
                            wineName VARCHAR(100) NOT NULL,
                            volume VARCHAR(10),
                            quantity INT NOT NULL,
                            pricePrUnit REAL NOT NULL,
                            variantCode INT NOT NULL)''')
        
        self.connection.execute('''CREATE TABLE IF NOT EXISTS offers 
                            (id INT NOT NULL PRIMARY KEY,
                            name VARCHAR(100) NOT NULL, 
                            lwin INT NOT NULL,
                            vendorId INT NOT NULL, 
                            pr INT,
                            cbr INT)''')
        self.connection.commit()
        self.close()
    
    def __del__(self):
        if (self.connection != None):
            self.connection.close()

    # Re-opens database connection.
    def reopen(self, filename = "wine.db"):
        self.connection = sqlite3.connect(filename)

    # Closes database.
    def close(self):
        if (self.connection != None):
            self.connection.close()

    # Checks whether database is empty.
    def empty(self):
        self.reopen()
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM offers")
        row = cursor.fetchone()
        self.close()

        return row == None

    # Adds wine.
    def add_wine(self, name, lwin, rank, bought, pr, cbr):
        if (self.connection == None):
            raise Exception("Wine database is closed.")

        t = (name, lwin, rank, bought, pr, cbr)
        self.reopen()
        self.connection.execute("INSERT INTO offers (id, name, lwin, vendorId, pr, cbr) VALUES (" + self.__sql_str_insert(t) + ")")
        self.connection.commit()
        self.close()

    # Adds several wines.
    # wines is a pandas dataframe.
    def add_wines(self, wines):
        if (self.connection == None):
            raise Exception("Wine database is closed.")

        self.reopen()

        for wine in wines:
            self.connection.execute("INSERT INTO offers (name, lwin) VALUES (" + self.__sql_str_insert(wine) + ")")
        
        self.connection.commit()
        self.close()

    # Returns full string of SQL insertion values.
    def __sql_str_insert(self, wine_field_tuple):
        res = ""

        for attribute in wine_field_tuple:
            if type(attribute) is str:
                res = res + "'" + attribute + "',"

            else:
                res = res + str(attribute) + ","

        return res[:len(res) - 1]

    # Returns sorted pandas dataframe.
    def get_ranked_wines(self):
        if (self.connection == None):
            raise Exception("Wine database is closed.")

        self.reopen()
        result = pd.read_sql_query("SELECT * FROM offers ORDER BY pr ASC", self.connection)
        self.close()

        return pd.DataFrame(result, columns = self.colums_offers)

    # Clears table of content.
    def clear_wines(self):
        self.reopen()
        self.connection.execute("DELETE FROM offers")
        self.connection.commit()
        self.close()