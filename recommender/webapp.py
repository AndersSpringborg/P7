from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import pandas as pd

from recommender_class.svm_recommender import SVMrecommender
from recommender_class.logit_recommender import Logit_recommender
from recommender_class.nb_recommender import Naive_bayes_recommender
import exceptions

app = Flask(__name__)
CORS(app)

#TODO:determine whether supplier name should be included
#cat_data and num_data are arrays specifying the name of categorical and numerical data in input wine offers, respectively. 
cat_data = ['region']
num_data = ['year', 'quantity', 'isOWC', 'isOC', 'isIB', 'price']

@app.route('/')
def default():
    return """Communicate with /update-recommendation/ route in order to get new recommendation\n 
    or /update-model/ for updating model"""

@app.route('/update-model/', methods=["POST"])
def update():
    model_type = request.form.get('model_type')
    transaction = request.form.get('Transactions') #TODO:determine whether this is necessary
    wine_offer = request.form.get('WineDeals')
    
    #check for the necessary arguments
    if model_type == None or transaction == None or wine_offer == None:
        return make_response(jsonify({"status":"Input not on proper format"}), 400)
    
    wine_offer_df = pd.read_json(wine_offer, orient='records')
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
    wines =  request.form.get('WineDeals')
    model_type = request.form.get('model_type')
        
    if wines == None or model_type == None:
        make_response(jsonify({"status":"data in body not on proper structure. A json string with wine-offers and a specification of model is needed"}), 400)
    wines = pd.read_json(wines, orient='records')
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
            return make_response(jsonify({"status":"No proper model_type selected. Please choose between 'nb', 'logit' or 'svm'"}), 300)
    except exceptions.NoModelException:
        return make_response(jsonify({"status":"No model for the chosen ML alg has been trained"}), 300)

    recommender.output()
    
    return make_response(jsonify({"Results":recommender.recommendation.to_json(orient='records')}), 200)
        

if (__name__ == "__main__"):
    app.run(host='0.0.0.0', port= 49501)
