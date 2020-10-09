import sqlite3

# Wine database class.
class wine_db:
    def __init__(self, filename = "wine.db"):
        self.connection = sqlite3.connect(filename)
        c = self.connection.cursor()

        c.execute('''CREATE TABLE wines
                    (name VARCHAR(100) NOT NULL,
                     lwin INT NOT NULL,
                     rank INT UNIQUE),
                     PRIMARY KEY (lwin)''')
        self.connection.commit()
    
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

        c = self.connection.cursor()
        c.execute("INSERT INTO wines VALUES ({name},{lwin}, {rank})")
        self.connection.commit() 

    # Returns sorted list of ranked wines.
    def get_ranked_wines(self):
        c = self.connection.cursor()
        c.execute("SELECT * FROM wines ORDER BY rank ASC")
        c.fetchall()

        result_list = []
        
        for row in c:
            result_list.append(tuple(row))

        return result_list
            

    # Clears table of content.
    def clear_wines(self):
        c = self.connection.cursor()
        c.execute("DELETE FROM wines")
        self.connection.commit()