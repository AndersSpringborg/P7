import pandas as pd
import random as rand
import pickle

import exceptions


#This class should be used as an abstract class, meaning that a subclass should override the content_based_recommend and save_cb_model
# methods
class DefaultRecommender():
    #The Recommender must be instantiated with the wineoffers as a dataframe, a list of categorical attributes, a list of numerical attributes
    #and a boolean specifying whether the purpose is to train a classifier.
    def __init__(self, offer_df, cat_attr, num_attr, isTrainable):
        self.offer_df = offer_df
        self.cat_attr = cat_attr
        self.num_attr = num_attr
        self.__input_offer_on_proper_format__()
        self.isTrainable = isTrainable
        
        if isTrainable:
            self.train_input = self.to_input_output_arrays()
        else:
            self.features = self.feature_to_array()
        
        #fields will contain training and test accuracy when calling save_cb_model
        self.train_acc = None
        self.test_acc = None

    #method needs to be defined in subclass, and should output a filtering of wine deals
    def content_based_recommend(self):
        raise exceptions.NotImplementedException("The Content based recommend function needs to be overridden")
    
    #method needs to be defined in subclass, and should save an internal represenation (parameters) of the chosen recommender algorithm
    def save_cb_model(self):
        raise exceptions.NotImplementedException("The saving of the content based model function should be overridden")
    
    #method loads a model
    def load_cb_model(self, path):
        clf = pickle.load(open(path, 'rb'))
        return clf

    #Checks whether the input offers have the necessary attributes specified by cat_attr and num_attr
    def __input_offer_on_proper_format__(self):
        attribute_list = []
        attribute_list.extend(self.cat_attr)
        attribute_list.extend(self.num_attr)
        offer_attributes =  self.offer_df.columns
        for attr in attribute_list:
            if not attr in offer_attributes:
                raise exceptions.IncompatibleData("Missing "+str(attr)+" from the input offers")

    #categorical data to one hot encoding for training
    def cat2one_hot(self, df, attribute, cat_dict):
        if not attribute in df.columns:
            raise exceptions.IncompatibleData()
        #TODO:ensure that the same categorical encoding is created
        one_hot = pd.get_dummies(df[attribute], prefix=attribute)
        cat_dict[attribute] = one_hot.columns
        df = pd.concat([df, one_hot], axis = 1)
        df = df.drop(labels=[attribute], axis = 1)
        return df

    def cat2one_hot_for_predict(self, df, attribute, cat_dict):
        if not attribute in df.columns:
            raise exceptions.IncompatibleData()

        one_hot = pd.get_dummies(df[attribute], prefix=attribute)
        one_hot.reindex(columns = cat_dict[attribute], fill_value=0)
        df = pd.concat([df, one_hot], axis = 1)
        df = df.drop(labels=[attribute], axis = 1)
        return df

    #return the data from dataframe a np arrays, and if a 'outcome' column is present then this column wil be returned as an array.
    def to_input_output_arrays(self):
        #To ensure method is only executed once.
        if hasattr(self, 'train_input'):
            return self.train_input
        
        cat_dict = {}
        offer_df = self.offer_df.copy()
        for cat in self.cat_attr:
            offer_df = self.cat2one_hot(offer_df, cat, cat_dict)
        
        with open('models/'+self.model_type+'.pickle', 'wb') as handle:
            pickle.dump(cat_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
        all_attr = []
        all_attr.extend(self.cat_attr)
        all_attr.extend(self.num_attr)
        droplist = []
        for x in offer_df.columns:
            if not x in all_attr:
                droplist.append(x)

        #TODO:change from 'outcome' to right name
        if 'outcome' in offer_df.columns:
            droplist.append('outcome')
            x = offer_df.drop(labels= droplist,axis=1).to_numpy()
            y = offer_df['outcome'].to_numpy()
            self.train_input = (x,y)
            return (x,y)
        else:
            raise exceptions.IncompatibleData("'outcome' attribute missing")

    #converts input attributes to feature matrices
    def feature_to_array(self):
        if hasattr(self, 'features'):
            return self.features
        with open('models/'+self.model_type+'.pickle', 'rb') as handle:
            cat_dict = pickle.load(handle)

        offer_df = self.offer_df.copy()
        for cat in self.cat_attr:
            offer_df = self.cat2one_hot_for_predict(offer_df, cat, cat_dict)
        all_attr = []
        all_attr.extend(self.cat_attr)
        all_attr.extend(self.num_attr)
        droplist = []
        for x in offer_df.columns:
            if not x in all_attr:
                droplist.append(x)
        return offer_df.drop(labels=droplist,axis=1).to_numpy()

    #splits dataset arrays into train and test arrays based on a split_rate in the interval of [0 - 1]
    def train_test_split(self, x, y, split_rate):
        split_size =int(round(len(y)*split_rate))
        # get first split_size elements
        train_x = x[:split_size]
        train_y = y[:split_size]

        #get last elemests starting from split_size
        test_x = x[split_size:]
        test_y = y[split_size:]
        return train_x,train_y,test_x,test_y

    #ranks the offers according to global offer price in local df
    def price_ranking(self, df, rank_name='PR'):
        if not 'globalPrice' in self.offer_df:
            raise exceptions.GlobalWinePriceException("Global Wine Price Column not defined")
        df['profit'] = df.apply(lambda row: self.get_profit(row), axis=1)
        df[rank_name] = df['profit'].rank(method="first", ascending=False)
        df = df.drop(['profit'], axis=1)
        df = df.sort_values('PR', axis=0, ascending=True)
        return df

    #calculates the possible profit for a wine offer in the dataframe 
    def get_profit(self,row):
        return row['globalPrice'] - row['price']
    
    #calculates and return the content-based ranking appended to the wine_offer data
    def cb_ranking(self, df):
        df1 = self.content_based_recommend()
        df1 = self.price_ranking(df1, rank_name='CBR')
        df1 = df1[['PR','CBR']]
        df = pd.merge(df, df1, how='left', on='PR')
        return df
    
    #calculates the price ranking and content based ranking. Access rankings through offer_df field.
    def recommend(self):
        self.offer_df = self.price_ranking(self.offer_df)
        self.offer_df = self.cb_ranking(self.offer_df)    
    
    #organises the recommendation on proper format and saves it into recommendation field.
    def output(self):
        columns_left = ['CBR', 'PR', 'linkedWineLwin']
        droplist_columns = []
        for column in self.offer_df.columns:
            if not column in columns_left:
                droplist_columns.append(column)
        self.recommendation = self.offer_df.drop(droplist_columns, axis=1)


#random value of 1 or 0 for each wine deals.
def expected_offer_row(row):
    i = rand.randint(0,100)
    if i >= 50:
        return 1
    else:
        return 0

#a static way of creating dummy global wine price data 
def static_profit(row):
    return 100
    
#dummy data for testing while database has not been created.
def get_dummy_data():
    df = pd.read_json("offers.json", encoding='utf-8')
    df = df.drop(df[df.wineName == ''].index)
    df = df.dropna(axis=0, subset=['linkedWineLwin'])
    df = df.drop_duplicates(subset='linkedWineLwin', keep = "first")
    df['outcome'] = df.apply(lambda row: expected_offer_row(row), axis=1)
    df['globalPrice'] = df.apply(lambda row: static_profit(row), axis = 1)
    return df
