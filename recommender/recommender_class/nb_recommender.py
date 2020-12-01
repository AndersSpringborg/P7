from sklearn.naive_bayes import GaussianNB
from recommender_class.DefaultRecommender import DefaultRecommender
import exceptions
from sklearn.metrics import accuracy_score
import pickle

#class implementing gausian naive bayes
class Naive_bayes_recommender(DefaultRecommender):
    def __init__(self, offer_df, cat_attr, num_attr, isTrainable):
        self.model_type = 'nb'
        super(Naive_bayes_recommender,self).__init__(offer_df,cat_attr,num_attr, isTrainable)

    def content_based_recommend(self):
        clf = self.load_cb_model("models/nb.sav")
        if not self.isTrainable:
            x = self.features
        else:
            raise Exception()

        #create a new column representing the predictions
        self.offer_df = self.offer_df.assign(cb_outcome= clf.predict(x))
        return self.offer_df.drop(self.offer_df[self.offer_df.cb_outcome == 0].index)
    
    def save_cb_model(self, path):
        if not self.isTrainable:
            raise exceptions.ImpossibleTrainException("Training is not possible as 'outcome' is not present in input data")
        (x,y) = self.to_input_output_arrays()
        split_rate = 0.8
        train_x,train_y,test_x,test_y = self.train_test_split(x, y, split_rate)

        clf = GaussianNB()
        clf.fit(train_x,train_y)
        self.train_acc = accuracy_score(clf.predict(train_x),train_y)
        self.test_acc = accuracy_score(clf.predict(test_x),test_y)
        pickle.dump(clf, open(path,'wb'))