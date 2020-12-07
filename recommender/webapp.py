from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import pandas as pd

from recommender_class.svm_recommender import SVMrecommender
from recommender_class.logit_recommender import Logit_recommender
from recommender_class.nb_recommender import Naive_bayes_recommender
import exceptions
import json

app = Flask(__name__)
CORS(app)

#cat_data and num_data are arrays specifying the name of categorical and numerical data in input wine offers, respectively. 
cat_data = ['region']
num_data = ['year', 'quantity', 'isOWC', 'isOC', 'isIB', 'price']

@app.route('/')
def default():
    return """Communicate with /update-recommendation/ route in order to get new recommendation\n 
    or /update-model/ for updating model"""

@app.route('/update-model/', methods=["POST"])
def update():
    data = request.get_json()
    try:
        model_type = data['model_type']
    except TypeError:
        return make_response(jsonify({"status":"model_type not on proper format"}), 400)
    try:
        wine_offer = data['WineDeals']
    except TypeError:
        make_response(jsonify({"status":"WineDeals not on proper format"}), 400)
    
    
    wine_offer_df = pd.read_json(json.dumps(wine_offer), orient='records')
    try:    
        if model_type == "svm":
            recommender = SVMrecommender(wine_offer_df, cat_data, num_data, True)
            recommender.save_cb_model("models/svm.sav")
        elif model_type == "logit":
            recommender = Logit_recommender(wine_offer_df, cat_data, num_data, True)
            recommender.save_cb_model("models/logit.sav")
        elif model_type == "nb":
            recommender = Naive_bayes_recommender(wine_offer_df, cat_data, num_data, True)
            recommender.save_cb_model("models/nb.sav")
        else:
            return make_response(jsonify({"status":"Model unspecified"}), 400)
    except exceptions.ImpossibleTrainException:
        return make_response(jsonify({"status":"Training is not possible"}), 400)
    except exceptions.IncompatibleData:
        return make_response(jsonify({"status":"Input offers not on proper format"}), 400)
    
    return make_response(jsonify({"status": "Model updated", "training accuracy": recommender.train_acc, "test accuracy": recommender.test_acc }), 200)

@app.route('/update-recommendation/', methods=["POST"])
def update_recommendation():
    data = request.get_json()
    try:
        wines =  data['WineDeals']
    except TypeError:
        make_response(jsonify({"status":"WineDeals not on proper format"}), 400)
    try:
        model_type = data['model_type']
    except TypeError:
        make_response(jsonify({"status":"model_type not on proper format"}), 400)

    wines = pd.read_json(json.dumps(wines), orient='records')
    try:
        if model_type == 'svm':
            recommender = SVMrecommender(wines, cat_data, num_data, False)
            recommender.recommend()        
        elif model_type == 'logit':
            recommender = Logit_recommender(wines, cat_data, num_data, False)
            recommender.recommend()
        elif model_type == 'nb':
            recommender = Naive_bayes_recommender(wines, cat_data, num_data, False)
            recommender.recommend()
        else:
            return make_response(jsonify({"status":"No proper model_type selected. Please choose between 'nb', 'logit' or 'svm'"}), 400)
    except exceptions.NoModelException:
        return make_response(jsonify({"status":"No model for the chosen ML alg has been trained"}), 400)

    recommender.output()
    
    return make_response(jsonify({"Results":recommender.recommendation.to_dict(orient='records'), "model_type":model_type}), 200)
        

if (__name__ == "__main__"):
    app.run(host='0.0.0.0', port= 49501)
