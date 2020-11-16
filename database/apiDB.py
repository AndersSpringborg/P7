import db
import flask as flask
from flask_cors import CORS


app = flask.Flask(__name__)
CORS(app)
testdb = db.wine_db()
# This defines a simple get request from root.


@app.route('/')
def sample_get():
    return "Computational Offloading <3!"

# This defines a simple get request in sub directory 'sub'.


@app.route('/GetWinesFromTimestamp/<arg>', methods=['GET'])
def get_offers_from_timestamp(arg):
    return testdb.get_offers_from_timestamp(arg)


@app.route('/GetOfferById/<arg>', methods=['GET'])
def get_offer_by_id(arg):
    return testdb.get_offer_by_id(arg)


@app.route('/GetAllTransactions', methods=['GET'])
def get_all_transactions():
    return testdb.get_all_transactions()


@app.route('/GetAllOffers', methods=['GET'])
def get_all_offers():
    return testdb.get_all_offers()

# This defines a simple get request in sub directory 'sub', where 'arg' is an argument.


@app.route('/sub/<arg>')
def sample_get_with_arg(arg):
    return "Hello, visitor! You entered a sub directory with argument '" + arg + "'."

# This defines a simple post request.


@app.route('/', methods=['POST'])
def sample_post():
    return "You posted '" + request.data + "'."


if (__name__ == "__main__"):
    app.run()
