from recommender_class.DefaultRecommender import DefaultRecommender
from sklearn.linear_model import LogisticRegression
import exceptions
from sklearn.metrics import accuracy_score
import pickle
import exceptions

#class implementing logistic regression
class Logit_recommender(DefaultRecommender):
    def __init__(self, offer_df, cat_attr, num_attr, isTrainable):
        self.model_type = 'logit'
        super(Logit_recommender,self).__init__(offer_df,cat_attr,num_attr, isTrainable)

    def content_based_recommend(self):
        self.check_for_model("models/logit.sav")
        
        regr = self.load_cb_model("models/logit.sav")
        if not self.isTrainable:
            x = self.feature_to_array()
        else:
            raise exceptions.ImpossibleTrainException()

        #create a new column representing the predictions
        self.offer_df = self.offer_df.assign(cb_outcome= regr.predict(x)) 
        return self.offer_df.drop(self.offer_df[self.offer_df.cb_outcome == 0].index)

    #save the parameters of the logistic regression after training with the training data
    def save_cb_model(self, path):
        if not self.isTrainable:
            raise exceptions.ImpossibleTrainException("Training is not possible. Check data")
        (x,y) = self.to_input_output_arrays()
        split_rate = 0.8
        train_x,train_y,test_x,test_y = self.train_test_split(x, y, split_rate)

        regressor = LogisticRegression().fit(train_x,train_y)
        self.train_acc = accuracy_score(regressor.predict(train_x),train_y)
        self.test_acc = accuracy_score(regressor.predict(test_x),test_y)
        pickle.dump(regressor, open(path,'wb'))

    
