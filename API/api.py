from flask import Flask, request, jsonify
import json
import pandas as pd

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def main_page():
    return '''POST: /data/transactions/ body: JSON transaction data. -> Upload transaction data to database.\r\n
            POST: /data/wine_deals/ body: JSON wine deals data. -> Upload wine deals data to database.\r\n'
            POST: /db_post/ body: Database content. -> Uploads raw content to insert into database.\r\n'
            GET: /db_get/ -> Gets database content.'''

@app.route('/data', methods = ['GET'])
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

    return res

if __name__ == "__main__":
    app.run()