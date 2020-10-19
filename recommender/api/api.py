from flask import Flask, request, jsonify
import json
import pandas as pd
import db
import recommend as rec

app = Flask(__name__)

@app.route('/')
def main_page():
    return "Send POST to '/data' to upload wine deals.\nSend GET to '/data' to read wine deals recommendation."

# TODO: First check if database is not empty.
@app.route('/data', methods = ['GET'])
def read_recommendation():
    if db.empty():
        return "No recommendations to make."

    data = {
        "WineDeals": __wine_maps(db.get_ranked_wines())
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

@app.route('/data', methods = ['POST'])
def write_data():
    parsed = json.loads(request.data)
    
    # TODO: Create a pandas dataframe of parsed JSON wines and it into recommend.py.
    # TODO: Insert output into db.py.

    database = db.wine_db()
    database.add_wines(rec.recommend(None))

if (__name__ == "__main__"):
    app.run()