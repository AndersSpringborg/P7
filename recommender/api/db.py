import sqlite3
import pandas as pd

# Wine database class.
class wine_db:
    def __init__(self, filename = "wine.db"):
        self.columns = ['name', 'lwin', 'rank']

        self.reopen()
        self.connection.execute('''CREATE TABLE IF NOT EXISTS wines 
                            (name VARCHAR(100) NOT NULL, 
                            lwin INT NOT NULL PRIMARY KEY, 
                            rank INT UNIQUE)''')
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

    # Adds wine.
    def add_wine(self, name, lwin, rank):
        if (self.connection == None):
            raise Exception("Wine database is closed.")

        t = tuple(name, lwin, rank)

        self.reopen()
        self.connection.execute("INSERT INTO wines (name, lwin, rank) VALUES (" + self.__sql_str_insert(t) + ")")
        self.connection.commit()
        self.close()

    # Adds several wines.
    # wines is a pandas dataframe.
    def add_wines(self, wines):
        if (self.connection == None):
            raise Exception("Wine database is closed.")

        self.reopen()

        for wine in wines:
            self.connection.execute("INSERT INTO wines (name, lwin, rank) VALUES (" + self.__sql_str_insert(wine) + ")")
        
        self.connection.commit()
        self.close()

    # Returns full string of SQL insertion values.
    def __sql_str_insert(wine):
        res = ""

        for attribute in wine:
            if type(attribute) is str:
                res = res + "'" + attribute + "'"

            else:
                res = res + attribute

    # Returns sorted pandas dataframe.
    def get_ranked_wines(self):
        if (self.connection == None):
            raise Exception("Wine database is closed.")

        self.reopen()
        result = self.connection.execute("SELECT * FROM wines ORDER BY rank ASC")
        df = pd.DataFrame(columns = self.columns)
        i = 0

        for row in result:
            for attribute in tuple(row):
                df.loc[i] = df.loc[i] + attribute
            i = i + 1

        self.close()
        return df

    # Clears table of content.
    def clear_wines(self):
        self.reopen()
        self.connection.execute("DELETE FROM wines")
        self.connection.commit()
        self.close()