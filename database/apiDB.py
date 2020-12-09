import db
import flask as flask
from flask import request
from flask_cors import CORS
import pandas as pd
import io
import json

app = flask.Flask(__name__)
CORS(app)
wine_db = db.wine_db()

@app.route('/AddOffers', methods=['POST'])
def offers_post():
    offers = []
    offers_data = request.get_json()
    offer_ids= []
    for offer in offers_data:
        offer_ids.append(offer['id'])
        current_offer = wine_db.clean_offers_data(offer)
        if current_offer is not None:
            offers.append(wine_db.create_offer_obj(current_offer))
            
            
    print(offer_ids)
    wine_db.add_wineoffers(offers)
    return wine_db.get_all_specified_offers(offer_ids)

def offer_id_list(offers):
    ids = list()

    for offer in offers:
        ids.append(offer.id)

    return ids

# Reads JSON array of global prices into list of Global_Price objects.
# They are then inserted.
@app.route('/AddGlobalPrices', methods = ['POST'])
def global_prices_post():
    prices = []
    json_prices = request.get_json()

    for json_price in json_prices:
        prices.append(db.Global_Price.from_json(json_price))

    wine_db.add_global_prices(prices)
    return ""

@app.route('/NewRecommendation', methods = ['POST'])
def new_recommendation_post():
    wine_db.add_recommendations(request.get_json())
    return ""

@app.route('/GetRecommendation', methods = ['GET'])
def recommendation_post():
    return wine_db.get_recommendation_fast()

def is_recommended_by(recommendation_json, recommender_alg, id):
    wines = recommendation_json[recommender_alg]

    for wine in wines:
        if (wine['id'] == id and wine['offers_FK'] != None):
            return True

        elif (wine['id'] == id):
            return False

    return False

@app.route('/AddTransactions', methods=['POST'])
def transactions_post():
    data = io.StringIO(request.data.decode('UTF-8'))
    df = pd.read_csv(data)

    transactions_data = df.to_dict(orient='record')
    transactions = []

    for transaction in transactions_data:
        current_transaction = wine_db.clean_transactions_data(transaction)
        if current_transaction is not None:
            transactions.append(
                wine_db.create_transaction_obj(current_transaction))

    wine_db.add_transactions_data(transactions)

    return "Added Transactions Succesfully."

@ app.route('/GetOffers', methods=['GET'])
def get_all_offers():
    return wine_db.get_all_offers()

@ app.route('/GetFromTimestamp/<arg>', methods=['GET'])
def get_offers_from_timestamp(arg):
    return wine_db.get_offers_from_timestamp(arg)

@ app.route('/GetOfferById/<arg>', methods=['GET'])
def get_offer_by_id(arg):
    return wine_db.get_offer_by_id(arg)

@ app.route('/GetTransactions', methods=['GET'])
def get_all_transactions():
    return wine_db.get_all_transactions()

@ app.route('/GetTransactionById/<arg>', methods=['GET'])
def get_transaction_by_id(arg):
    return wine_db.get_transaction_by_id(arg)

if (__name__ == "__main__"):
    app.run(host = '0.0.0.0', port = 49502)