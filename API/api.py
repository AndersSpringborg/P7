from flask import Flask, redirect, abort, request, jsonify, make_response
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)
mtx = False

DB_DOMAIN = 'worse-db:49502'
RECOMMENDER_DOMAIN = 'worse-recommender:49501'

# Dictionary of tokens for each component.
tokens = {
    "UI": 23984728947,
    "db": 74923873298,
    "recommender": 4832042343,
    "third": 4279874232
}

@app.route('/', methods = ['GET'])
def main_page():
    return '''POST: /data/transactions/ body: JSON transaction data. -> Upload transaction data to database.\r\n
            POST: /data/wine_deals/ body: JSON wine deals data. -> Upload wine deals data to database.\r\n'
            POST: /db_post/ body: Database content. -> Uploads raw content to insert into database.\r\n'
            POST: /data/interval/ body: Time interval. ->  Updates recommender model by using data from specified time interval. \r\n
            GET: /recommendation_get/ -> Gets recommended wine deals.'''

# Handles GET request from UI for database content.
@app.route('/recommendation_get', methods = ['GET'])
def db_get():
    if (not 'X-Token' in request.headers) or int(request.headers['X-Token']) != tokens['UI']:
        return make_response('Request not from database', 401)

    response = requests.get('db_url/ranked_data')

    if response.status_code < 200 or response.status_code > 299:
        abort(500)

    return response.content

# Handles POST request from 3rd party to add transaction data.
# Appends new transaction data to transactions relation in db.
@app.route('/data/transactions', methods = ['POST'])
def transactions_post():
    global mtx

    if (not 'X-token' in request.headers) or int(request.headers['X-Token']) != tokens['third']:
        return make_response('Request not from developer', 401)

    elif not parse_transactions(request.get_json()):
        return make_response('Data couldn\'t be parsed', 400)

    while compare_swap(False, True):
        pass

    response = requests.post(DB_DOMAIN + '/transaction/append', data = request.get_json())
    mtx = False

    return ""

# Parses POST request body of transactions.
def parse_transactions(json):
    if 'Transactions' not in json:
        return False

    for transaction in json['Transactions']:
        # Check for existence of all necessary field.
        # For example, 'if 'SomeField' not in transaction'.
        pass

    return True

# Handles POST request from 3rd party to add wine deals data.
# Retrieves copy of wine deals relation and sends it to recommender API.
@app.route('/data/wine_deals', methods = ['POST'])
def wine_deals_post():
    global mtx

    if (not 'X-token' in request.headers) or int(request.headers['X-Token']) != tokens['third']:
        return make_response('Request not from developer', 401)

    elif not parse_wine_deals(request.get_json()):
        return make_response('Data couldn\'t be parsed', 400)

    while compare_swap(False, True):
        pass

    response = requests.post(DB_DOMAIN + '/wine_deals/append', data = request.get_json())
    rec_result = requests.post(RECOMMENDER_DOMAIN + '/update-recommendation', data = response.text)
    requests.post(DB_DOMAIN + '/wine_deals/recommendation', data = res_result.text)
    mtx = False

    return ""

# Parses POST request body of wine deals.
def parse_wine_deals(json):
    if 'WineDeals' not in json:
        return False

    for wine_deal in json['WineDeals']:
        # Check for existence of all necessary field.
        # For example, 'if 'SomeField' not in wine_deal'.
        pass

    return True

# Handles POST request from 3rd party to set data interval.
# Retrieves copy of transactions relation and wine deals relation within specified time interval and sends it to recommender API.
@app.route('/data/interval', methods = ['POST'])
def interval_post():
    global mtx

    if (not 'X-token' in request.headers) or int(request.headers['X-Token']) != tokens['third']:
        return make_response('Request not from developer', 401)

    elif not parse_time_interval(request.get_json()):
        return make_response('Data couldn\'t be parsed', 400)

    while compare_swap(False, True):
        pass

    json_data = request.get_json()
    response = requests.get(DB_DOMAIN + '/interval/' + str(json_data["start"]) + '/' + str(json_data["end"]))
    requests.post(RECOMMENDER_DOMAIN + '/update-model', data = response.text)
    mtx = False

    return ""

# Parses POST request body of time interval.
def parse_time_interval(json):
    if 'TimeInterval' not in json:
        return False

    elif 'Start' not in json['TimeInterval'] or 'End' not in json['TimeInterval']:
        return False

    return True

# Handles POST request from recommender API to add content into db API.
@app.route('/db_post', methods = ['POST'])
def output_post():
    global mtx

    if (not 'X-token' in request.headers) or int(request.headers['X-Token']) != tokens['recommender']:
        return make_response('Request not from recommender', 401)

    elif not parse_recommendation(request.get_json()):
        return make_response('Data couldn\'t be parsed', 400)

    while compare_swap(False, True):
        pass

    requests.post(DB_DOMAIN + '/wine_deals/recommendation', data = request.get_json())
    mtx = False

    return ""

# Parses POST request body of recommendation results.
def parse_recommendation(json):
    if 'Results' not in json:
        return False

    for result in json['Results']:
        if 'PR' not in result or 'CBR' not in result or 'WineID' not in result:
            return False

    return True

# Compare-And-Swap mechanism for busy waiting.
def compare_swap(expected, new):
    global mtx
    actual = mtx

    if actual == expected:
        mtx = new

    return actual

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 49500)
