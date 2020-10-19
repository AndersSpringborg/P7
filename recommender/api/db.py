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

    # Checks whether database is empty.
    def empty(self):
        self.reopen()
        result = self.connection.execute("SELECT * FROM wines")
        self.close()

        return result.arraysize == 0

    # Adds wine.
    def add_wine(self, name, lwin, rank):
        if (self.connection == None):
            raise Exception("Wine database is closed.")

        t = (name, lwin, rank)
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
        result = pd.read_sql_query("SELECT * FROM wines ORDER BY rank ASC", self.connection)
        self.close()

        return pd.DataFrame(result, columns = self.columns)

    # Clears table of content.
    def clear_wines(self):
        self.reopen()
        self.connection.execute("DELETE FROM wines")
        self.connection.commit()
        self.close()

database = wine_db()
database.add_wine("Wine 1", 123, 2)
database.add_wine("Wine 2", 7654, 1)
database.add_wine("Wine 3", 273, 3)

df = database.get_ranked_wines()
print(df)