import pandas as pd
import numpy as np
import pyspark as ps
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    IntegerType, StringType, IntegerType, FloatType, 
    StructField, StructType, DoubleType
)
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator
import matplotlib.pyplot as plt
import cPickle as pickle

# Import pandas df containing info from review scrape

als_df = pd.read_pickle('als_df.pkl')
als_df.reset_index(drop=True, inplace=True)
als_df = als_df[['user_id', 'item_id', 'rating', 'date']]

# Start a spark session to train an ALS model

class ALSRecommender():
    
    def __init__(self, user_factors_df, item_factors_df, survey_results):
        self.user_factors_df = user_factors_df
        self.item_factors_df = item_factors_df
        self.survey_results = survey_results


    def predict_rating(self, user_idx, item_idx):
        """Return the predicted rating of item by user (by iloc)."""
        user_factors_array = np.array(self.user_factors_df['features'].tolist())
        item_factors_array = np.array(self.item_factors_df['features'].tolist())

        user_vector = user_factors_array[user_idx, :]
        item_vector = item_factors_array[item_idx, :].T
        return user_vector @ item_vector

    def predict_rating_by_id(user_id, item_id):
        """Return the predicted rating of item by user (by id)."""
        user_idx = self.user_factors_df.index[uf_df['id'] == user_id][0]
        item_idx = self.item_factors_df.index[if_df['id'] == item_id][0]
        return predict_rating(user_idx, item_idx)

    def get_restaurant_indexes(user_ratings_df, item_factors_df):
        """Return an array of restaurant indexes that were reviewed by a particular user"""
        rest_idxs = []
        for item in user_ratings_df['item_id']:
            rest_idx = if_df.index[if_df['id']==item]
            rest_idxs.append(rest_idx[0])
        return np.array(rest_idxs)

    def newuser_predict(new_user_factors, item_factors_array):
        """Return a new df with a single row containing the users predictions for every restaurant"""
        new_factor_list =[]
        for i in range(len(item_factors_array)):
            new_factor_list.append(np.dot(new_user_factors, item_factors_array[i]))
        newuser_preds = pd.DataFrame([new_factor_list], index=['newuser'])
        return new_user_preds

    def change_rest_ids_to_aliases(new_user_preds):
        """Use the inverted alias dictionary to rename columns by restaurant alias"""
        new_user_preds = new_user_preds.rename(inv_alias_dict, axis=1)
        new_user_preds.sort_values(by='newuser', axis=1, ascending=False, inplace=True)
        return new_user_preds

    def get_preds_from_survey_results(survey_results):



