import db
import flask as flask
from flask import request
from flask_cors import CORS
import pandas as pd
import io

app = flask.Flask(__name__)
CORS(app)
db = db.wine_db()

@app.route('/AddOffers', methods=['POST'])
def offers_post():
    offers = []
    offers_data = request.get_json()

    for offer in offers_data:
        current_offer = db.clean_offers_data(offer)
        if current_offer is not None:
            offers.append(db.create_offer_obj(current_offer))

    db.add_wineoffers(offers)

    return "Added Wines Succesfully."

@app.route('/AddTransactions', methods=['POST'])
def transactions_post():
    data = io.StringIO(request.data.decode('UTF-8'))
    df = pd.read_csv(data)

    transactions_data = df.to_dict(orient='record')
    transactions = []

    for transaction in transactions_data:
        current_transaction = db.clean_transactions_data(transaction)
        if current_transaction is not None:
            transactions.append(
                db.create_transactionobj(current_transaction))

    db.add_transactions_data(transactions)

    return "Added Transactions Succesfully."

@ app.route('/GetOffers', methods=['GET'])
def get_all_offers():
    return db.get_all_offers()

@ app.route('/GetFromTimestamp/<arg>', methods=['GET'])
def get_offers_from_timestamp(arg):
    return db.get_all_from_timestamp(arg)

@ app.route('/GetOfferById/<arg>', methods=['GET'])
def get_offer_by_id(arg):
    return db.get_offer_by_id(arg)

@ app.route('/GetTransactions', methods=['GET'])
def get_all_transactions():
    return db.get_all_transactions()

if (__name__ == "__main__"):
    app.run(host = '0.0.0.0', port = 49502)