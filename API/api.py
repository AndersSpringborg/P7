from flask import Flask, request, jsonify
import json
import pandas as pd

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def main_page():
    return '''POST: /data/transactions/ body: JSON transaction data. -> Upload transaction data to database.\r\n
            POST: /data/wine_deals/ body: JSON wine deals data. -> Upload wine deals data to database.\r\n'
            POST: /db_post/ body: Database content. -> Uploads raw content to insert into database.\r\n'
            GET: /db_get/ -> Gets database content.\r\n
            GET: /recommendation_get/ -> Gets recommended wine deals.'''

# Handles GET request from recommender API for database content.
@app.route('/db_get', methods = ['GET'])
def recommendation_get():
    return "Contact db API to get content."

# Handles GET request from UI for database content.
@app.route('/recommendation_get', methods = ['GET'])
def db_get():
    return "Contact db API to get recommendations."

# Handles POST request from 3rd party to add transaction data.
@app.route('/data/transactions', methods = ['POST'])
def transactions_post():
    return "Post the data to db API."

# Handles POST request from 3rd party to add wine deals data.
@app.route('/data/wine_deals', methods = ['POST'])
def wine_deals_post():
    return "Post the data to db API."

# Handles POST request from recommender API to add content into db API.
@app.route('/db_post', methods = ['POST'])
def output_post():
    return "Post the data to db API."

"""@app.route('/data', methods = ['GET'])
def read_recommendation():
    # None is subbed with Pandas DataFrame.
    data = {
        "WineDeals": __wine_maps(None)
    }

    return data

# Returns list of maps of wine deals in pandas dataframe.
def __wine_maps(frame):
    res = []

    for index, row in frame.iterrows():
        res.append({
            "name": row['name'],
            "lwin": row['lwin'],
            "rank": row['rank']
        })

    return res"""

if __name__ == "__main__":
    app.run()