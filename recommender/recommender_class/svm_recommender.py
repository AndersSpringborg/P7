from recommender_class.DefaultRecommender import DefaultRecommender, get_dummy_data
from sklearn import svm, datasets
from sklearn.metrics import accuracy_score
import pickle
import exceptions

#class implementing support vector machine
class SVMrecommender(DefaultRecommender):
    def __init__(self, offer_df, cat_attr, num_attr, isTrainable):
        self.model_type = 'svm'
        super(SVMrecommender,self).__init__(offer_df,cat_attr,num_attr, isTrainable)

    def content_based_recommend(self):
        self.check_for_model("models/svm.sav")
        clf = self.load_cb_model("models/svm.sav")
        if not self.isTrainable:
            x = self.feature_to_array()
        else:
            (x,_) = self.to_input_output_arrays()
        
        #create a new column representing the predictions
        self.offer_df = self.offer_df.assign(cb_outcome= clf.predict(x))
        
        return self.offer_df.drop(self.offer_df[self.offer_df.cb_outcome == 0].index)

    def save_cb_model(self, path):
        clf = svm.SVC()
        if not self.isTrainable:
            raise exceptions.ImpossibleTrainException("Training is not possible as the recommender is not in training mode")
        (x,y) = self.to_input_output_arrays()
        split_rate = 0.8
        train_x,train_y,test_x,test_y = self.train_test_split(x, y, split_rate)
        
        clf.fit(train_x,train_y)
        self.train_acc = accuracy_score(clf.predict(train_x),train_y)
        self.test_acc = accuracy_score(clf.predict(test_x),test_y)
        pickle.dump(clf, open(path,'wb'))
