import sqlite3

# Wine database class.
class wine_db:
    def __init__(self, filename = "wine.db"):
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

        self.reopen()
        self.connection.execute("INSERT INTO wines (name, lwin, rank) VALUES ('" + name + "', " + str(lwin) + ", " + str(rank) + ")")
        self.connection.commit()
        self.close()

    # Returns sorted list of ranked wines.
    def get_ranked_wines(self):
        if (self.connection == None):
            raise Exception("Wine database is closed.")

        self.reopen()
        result = self.connection.execute("SELECT * FROM wines ORDER BY rank ASC")

        result_list = []

        for row in result:
            result_list.append(tuple(row))

        self.close()
        return result_list

    # Clears table of content.
    def clear_wines(self):
        self.reopen()
        self.connection.execute("DELETE FROM wines")
        self.connection.commit()
        self.close()