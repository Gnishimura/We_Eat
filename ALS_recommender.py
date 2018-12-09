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
import pickle

# Import pandas df containing info from review scrape

als_df = pd.read_pickle('als_df.pkl')
als_df.reset_index(drop=True, inplace=True)
als_df = als_df[['user_id', 'item_id', 'rating', 'date']]

# Start a spark session to train an ALS model

class ALSRecommender():
    
    def __init__(self, item_factors_df, inverted_alias_dict, survey_results):
        self.item_factors_df = item_factors_df
        self.item_factors_array = np.array(self.item_factors_df['features'].tolist())
        self.inverted_alias_dict = inverted_alias_dict
        self.survey_results = survey_results

    def get_restaurant_indexes(self, user_ratings_df, item_factors_df):
        """Return an array of restaurant indexes that were reviewed by a particular user"""
        rest_idxs = []
        for item in user_ratings_df['item_id']:
            rest_idx = self.item_factors_df.index[self.item_factors_df['id']==item]
            rest_idxs.append(rest_idx[0])
        return np.array(rest_idxs)

    def new_user_predict(self, new_user_factors, item_factors_array, username):
        """Return a new df with a single row containing the users predictions for every restaurant"""
        new_factor_list =[]
        for i in range(len(item_factors_array)):
            new_factor_list.append(np.dot(new_user_factors, item_factors_array[i]))
        new_user_preds = pd.DataFrame([new_factor_list], index=[username])
        return new_user_preds

    def change_rest_ids_to_aliases(self, new_user_preds, inverted_alias_dict):
        """Use the inverted alias dictionary to rename columns by restaurant alias"""
        new_user_preds = new_user_preds.rename(inverted_alias_dict, axis=1)
        return new_user_preds

    def standardize_survey_results(self, survey_results):
        """Return the survey_results dictionary with the ratings on a scale of 1-5 (to make
        it the same as Yelp's scale)"""
        return {k: v / 2 for k, v in self.survey_results.items()} 


    def get_user_ratings_df(self):
        """Return a df with columns 'item_id' and 'ratings' for an individual user's survey results"""

        #make a new dictionary with keys=restaurant_id, values=user's rating
        id_to_rating = {k: survey_standardized[v] for k, v in self.inverted_alias_dict.items() if v in survey_standardized}
        user_ratings_df = pd.DataFrame.from_dict(id_to_rating, orient='index')
        user_ratings_df.reset_index(inplace=True)
        user_ratings_df.rename(columns={'index':'item_id', 0:'rating'}, inplace=True)
        return user_ratings_df
    
    def get_user_factors_array(self, item_factors_array, restaurant_idxs, user_ratings_df):
        latent_item_features = item_factors_array[restaurant_idxs]
        ratings = user_ratings_df['rating'].values
        user_factors_array, residuals, rank, s = np.linalg.lstsq(latent_item_features, survey_ratings) 
        return user_factors_array

    def get_preds_from_single_survey_results(self, survey_results):
        """Return a df of predictions user preferences for every restaurant, given the user's survey results"""
        
        for k, v in survey_results.items():

            user_ratings_df = self.get_user_ratings_df(v)
            rest_idxs = self.get_restaurant_indexes(user_ratings_df, self.item_factors_df)
            latent_item_features = self.item_factors_array[rest_idxs]
            survey_ratings = user_ratings_df['rating'].values

        
        new_user_preds = self.new_user_predict(X, self.item_factors_array, username)
        new_user_named_preds = self.change_rest_ids_to_aliases(new_user_preds, self.inverted_alias_dict)
        return new_user_named_preds
    
    def compile_preds_database(self, all_surveys):
        preds = []
        for k, v in all_surveys.items():
            preds.append(self.get_preds_from_single_survey_results(k, v))
        
        return pd.concat(preds, axis=0, sort=False)



#Things that I probably don't need:

#self.user_factors_df = user_factors_df
#self.user_factors_array = np.array(self.user_factors_df['features'].tolist())

    # def predict_rating(self, user_idx, item_idx):
    #     """Return the predicted rating of item by user (by iloc)."""
    #     user_vector = self.user_factors_array[user_idx, :]
    #     item_vector = self.item_factors_array[item_idx, :].T
    #     return user_vector @ item_vector

    # def predict_rating_by_id(self, user_id, item_id):
    #     """Return the predicted rating of item by user (by id)."""
    #     user_idx = self.user_factors_df.index[uf_df['id'] == user_id][0]
    #     item_idx = self.item_factors_df.index[if_df['id'] == item_id][0]
    #     return predict_rating(user_idx, item_idx)