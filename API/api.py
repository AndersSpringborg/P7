from flask import Flask, redirect, abort, request, jsonify, make_response
from flask_cors import CORS
import requests
import json
import io
import sys

app = Flask(__name__)
CORS(app)
mtx = False

DB_PORT = 49502
RECOMMENDER_PORT = 49501
DB_DOMAIN = 'http://worse-db:' + str(DB_PORT)
RECOMMENDER_DOMAIN = 'http://worse-recommender:' + str(RECOMMENDER_PORT)

# Dictionary of tokens for each component.
tokens = {
    "UI": 23984728947,
    "db": 74923873298,
    "recommender": 4832042343,
    "third": 4279874232
}

# Standard route for GET requests.
@app.route('/', methods = ['GET'])
def main_page():
    return '''POST: /data/transactions/ body: JSON transaction data. -> Upload transaction data to database.\r\n
            POST: /data/wine_deals/ body: JSON wine deals data. -> Upload wine deals data to database.\r\n'
            POST: /db_post/ body: Database content. -> Uploads raw content to insert into database.\r\n'
            POST: /data/interval/ body: Time interval. ->  Updates recommender model by using data from specified time interval. \r\n
            GET: /recommendation_get/ -> Gets recommended wine deals.'''

# Handles GET request from UI for database content.
@app.route('/recommendation', methods=['GET'])
def db_get():
    global mtx

    if (not 'X-Token' in request.headers) or int(request.headers['X-Token']) != tokens['UI']:
        return make_response('Request not from UI component', 401)

    while compare_swap(False, True):
        pass

    response = requests.get(DB_DOMAIN + '/GetRecommendation')

    if (int(response.status_code) >= 400):
        mtx = False
        make_response('Database component error', response.status_code)

    mtx = False
    return response.content

# Handles GET request fron UI for get all transactions from database component.
@app.route('/transactions', methods = ['GET'])
def db_get_transactions():
    global mtx

    if (not 'X-Token' in request.headers) or int(request.headers['X-Token']) != tokens['UI']:
        return make_response('Request not from UI component', 401)

    while compare_swap(False, True):
        pass

    response = requests.get(DB_DOMAIN + '/GetTransactions')

    if (int(response.status_code) >= 400):
        mtx = False
        make_response('Database component error', response.status_code)

    mtx = False
    return response.content

# Gets single wine by given wine ID.
@app.route('/wine/<arg>', methods=['GET'])
def get_wine(arg):
    global mtx

    while compare_swap(False, True):
        pass

    response = requests.get(DB_DOMAIN + '/GetOfferById/' + str(arg))

    if (int(response.status_code) >= 400):
        mtx = False
        make_response('Database component error', response.status_code)

    mtx = False
    return response.content

# Gets single transaction by given ID.
@app.route('/transaction/<arg>', methods=['GET'])
def get_transaction(arg):
    global mtx

    while compare_swap(False, True):
        pass

    response = requests.get(DB_DOMAIN + '/GetTransactionById/' + str(arg))

    if (int(response.status_code) >= 400):
        mtx = False
        make_response('Database component error', response.status_code)

    mtx = False
    return response.content

# Handles POST request from 3rd party to add global wine prices.
# Appends new global wine prices to db.
@app.route('/global_prices', methods=['POST'])
def global_prices_post():
    global mtx

    if (not 'X-token' in request.headers) or int(request.headers['X-Token']) != tokens['third']:
        return make_response('Request not from developer component', 401)

    while compare_swap(False, True):
        pass

    response = requests.post(
        DB_DOMAIN + '/AddGlobalPrices', data=request.data)

    if (int(response.status_code) >= 400):
        mtx = False
        make_response('Database component error', response.status_code)

    mtx = False
    return ""

# Handles POST request from 3rd party to add transaction data.
# Appends new transaction data to transactions relation in db.


@app.route('/data/transactions', methods=['POST'])
def transactions_post():
    global mtx

    if (not 'X-token' in request.headers) or int(request.headers['X-Token']) != tokens['third']:
        return make_response('Request not from developer component', 401)

    while compare_swap(False, True):
        pass

    response = requests.post(DB_DOMAIN + '/AddTransactions', data=request.data)

    if (int(response.status_code) >= 400):
        mtx = False
        make_response('Database component error', response.status_code)

    mtx = False
    return ""

# Handles POST request from 3rd party to add wine deals data.
# Retrieves copy of wine deals relation and sends it to recommender API.
@app.route('/data/wine_deals', methods=['POST'])
def wine_deals_post():
    global mtx

    if (not 'X-token' in request.headers) or int(request.headers['X-Token']) != tokens['third']:
        return make_response('Request not from developer component', 401)

    while compare_swap(False, True):
        pass

    json_in = request.get_json()
    db_response = requests.post(
        DB_DOMAIN + '/AddOffers', json=json_in['WineDeals'])

    if (int(db_response.status_code) >= 400):
        mtx = False
        make_response('Database component error', db_response.status_code)

    merged = {
        "WineDeals": db_response.json(),
        "model_type": json_in['model_type']
    }

    rec_result = requests.post(
        RECOMMENDER_DOMAIN + '/update-recommendation/', json=merged)

    if (int(rec_result.status_code) >= 400):
        mtx = False
        make_response('Recommender component error', rec_result.status_code)

    db_result_post = requests.post(
        DB_DOMAIN + '/NewRecommendation', json=json.loads(rec_result.text))

    if (int(db_result_post.status_code) >= 400):
        mtx = False
        make_response('Database component error', db_result_post.status_code)

    mtx = False
    return ""

# Handles POST request from 3rd party to set data interval.
# Retrieves copy of transactions relation and wine deals relation within specified time interval and sends it to recommender API.
@app.route('/data/time', methods=['POST'])
def interval_post():
    global mtx
    json_data = request.get_json()

    if (not 'X-token' in request.headers) or int(request.headers['X-Token']) != tokens['third']:
        return make_response('Request not from developer component', 401)

    elif not parse_time_interval(json_data):
        return make_response('Data couldn\'t be parsed', 400)

    while compare_swap(False, True):
        pass

    get_response = requests.get(DB_DOMAIN + '/GetFromTimestamp/' + str(
        json_data['TimeInterval']['Time']), headers={'model-type': json_data['TimeInterval']['model_type']})

    if (int(get_response.status_code) >= 400):
        mtx = False
        return make_response('Database component error', get_response.status_code)

    merged = {
        "WineDeals": json.loads(get_response.text),
        "model_type": json_data['TimeInterval']['model_type']
    }

    post_response = requests.post(
        RECOMMENDER_DOMAIN + '/update-model/', json=merged)

    if (int(post_response.status_code) >= 400):
        mtx = False
        make_response('Recommender component error', post_response.status_code)

    mtx = False
    return ""

# Parses POST request body of time interval.
def parse_time_interval(json):
    if 'TimeInterval' not in json:
        return False

    return 'Time' in json['TimeInterval'] and 'model_type' in json['TimeInterval']

# Compare-And-Swap mechanism for busy waiting.
def compare_swap(expected, new):
    global mtx
    actual = mtx

    if actual == expected:
        mtx = new

    return actual


if __name__ == "__main__":
    if (len(sys.argv) >= 2 and sys.argv[1] == 'local'):
        DB_DOMAIN = 'http://127.0.0.1:' + str(DB_PORT)
        RECOMMENDER_DOMAIN = 'http://127.0.0.1:' + str(RECOMMENDER_PORT)

    app.run(host='0.0.0.0', port=49500)
