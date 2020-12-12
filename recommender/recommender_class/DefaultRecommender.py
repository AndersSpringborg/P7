import pandas as pd
import random as rand
import pickle
import numpy as np
from os import path

import exceptions


# This class should be used as an abstract class, meaning that a subclass should override the content_based_recommend and save_cb_model
# methods
class DefaultRecommender():
    # The Recommender must be instantiated with the wineoffers as a dataframe, a list of categorical attributes, a list of numerical attributes
    # and a boolean specifying whether the purpose is to train a classifier.
    def __init__(self, offer_df, cat_attr, num_attr, isTrainable):
        self.offer_df = offer_df
        self.cat_attr = cat_attr
        self.num_attr = num_attr
        self.__input_offer_on_proper_format__()
        self.isTrainable = isTrainable

        if isTrainable:
            self.train_input = self.to_input_output_arrays()

        # fields will contain training and test accuracy when calling save_cb_model
        self.train_acc = None
        self.test_acc = None

    # method needs to be defined in subclass, and should output a filtering of wine deals
    def content_based_recommend(self):
        raise exceptions.NotImplementedException(
            "The Content based recommend function needs to be overridden")

    # method needs to be defined in subclass, and should save an internal represenation (parameters) of the chosen recommender algorithm
    def save_cb_model(self):
        raise exceptions.NotImplementedException(
            "The saving of the content based model function should be overridden")

    # method loads a model
    def load_cb_model(self, path):
        clf = pickle.load(open(path, 'rb'))
        return clf

    # Checks whether the input offers have the necessary attributes specified by cat_attr and num_attr
    def __input_offer_on_proper_format__(self):
        attribute_list = []
        attribute_list.extend(self.cat_attr)
        attribute_list.extend(self.num_attr)
        offer_attributes = self.offer_df.columns
        for attr in attribute_list:
            if not attr in offer_attributes:
                raise exceptions.IncompatibleData(
                    "Missing "+str(attr)+" from the input offers")

    # categorical data to one hot encoding for training
    def cat2one_hot(self, df, attribute, cat_dict):
        if not attribute in df.columns:
            raise exceptions.IncompatibleData()
        # TODO:ensure that the same categorical encoding is created
        one_hot = pd.get_dummies(df[attribute], prefix=attribute)
        cat_dict[attribute] = one_hot.columns
        df = pd.concat([df, one_hot], axis=1)
        df = df.drop(labels=[attribute], axis=1)
        return df

    def cat2one_hot_for_predict(self, df, attribute, cat_dict):
        if not attribute in df.columns:
            raise exceptions.IncompatibleData()

        one_hot = pd.get_dummies(df[attribute], prefix=attribute)
        one_hot.reindex(columns=cat_dict[attribute], fill_value=0)
        df = pd.concat([df, one_hot], axis=1)
        df = df.drop(labels=[attribute], axis=1)
        return df

    # return the data from dataframe a np arrays, and if a 'outcome' column is present then this column wil be returned as an array.
    def to_input_output_arrays(self):
        # To ensure method is only executed once.
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

        if 'transactions_id' in offer_df.columns:
            droplist.append('transactions_id')
            x = offer_df.drop(labels=droplist, axis=1).to_numpy()
            offer_df['transactions_id'] = offer_df['transactions_id'].fillna(0)
            y = offer_df['transactions_id'].to_numpy()
            self.train_input = (x, y)
            return (x, y)
        else:
            raise exceptions.IncompatibleData(
                "'transactions_id' attribute missing")

    # converts input attributes to feature matrices
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
        return offer_df.drop(labels=droplist, axis=1).to_numpy()

    # splits dataset arrays into train and test arrays based on a split_rate in the interval of [0 - 1]
    def train_test_split(self, x, y, split_rate):
        split_size = int(round(len(y)*split_rate))
        # get first split_size elements
        train_x = x[:split_size]
        train_y = y[:split_size]

        # get last elemests starting from split_size
        test_x = x[split_size:]
        test_y = y[split_size:]
        return train_x, train_y, test_x, test_y

    # calculates the possible profit for a wine offer in the dataframe

    def get_profit(self, row):
        if(np.isnan(row['global_price'])):
            return np.nan

        return int(row['global_price']) - int(row['price'])

    # checks whether model serialisation in model_path exists
    def check_for_model(self, model_path):
        path_to_parent_dir = path.abspath(
            path.join(path.dirname(__file__), ".."))
        model_path = path.join(path_to_parent_dir, model_path)
        if not path.exists(model_path):
            raise exceptions.NoModelException()
        else:
            return

    # calculates the price difference and content-based filtering.
    def recommend(self):
        if not 'global_price' in self.offer_df:
            raise exceptions.GlobalWinePriceException(
                "Global Wine Price Column not defined")
        self.offer_df['price_diff'] = self.offer_df.apply(
            lambda row: self.get_profit(row), axis=1)
        self.content_based_recommend()

    # organises the recommendation on proper format and saves it into recommendation field.
    def output(self):
        columns_left = ['price_diff', 'id', 'cb_outcome']
        droplist_columns = []
        for column in self.offer_df.columns:
            if not column in columns_left:
                droplist_columns.append(column)
        self.recommendation = self.offer_df.drop(droplist_columns, axis=1)
