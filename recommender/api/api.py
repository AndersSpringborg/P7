from flask import Flask, request, jsonify
import json
import pandas as pd
import db as data
import recommend as rec

app = Flask(__name__)
database = data.wine_db()

@app.route('/')
def main_page():
    return "Send POST to '/data' to upload wine deals.\nSend GET to '/data' to read wine deals recommendation."

@app.route('/data', methods = ['GET'])
def read_recommendation():
    if database.empty():
        return "null"

    data = {
        "WineDeals": __wine_maps(database.get_ranked_wines())
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

# Appends received data to db.
# Then, starts ranking the content of the DB and insert it into recommender db.
@app.route('/data', methods = ['POST'])
def write_data():
    parsed = json.loads(request.data)
    
    # TODO: Create a pandas dataframe of parsed JSON wines and it into recommend.py.
    # TODO: Insert output into db.py.

    database.add_wines(rec.recommend(None))

if (__name__ == "__main__"):
    app.run()