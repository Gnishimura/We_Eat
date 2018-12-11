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


class ALSRecommender():
    
    def __init__(self, item_factors_df, inverted_alias_dict, preds_df):
        self.item_factors_df = item_factors_df
        self.item_factors_array = np.array(self.item_factors_df['features'].tolist())
        self.inverted_alias_dict = inverted_alias_dict
        self.preds_df = preds_df

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

    def standardize_survey_results(self, ratings_dict):
        """Return the survey_results dictionary with the ratings on a scale of 1-5 (to make
        it the same as Yelp's scale)"""
        return {k: v / 2 for k, v in ratings_dict.items()} 


    def get_user_ratings_df(self, ratings_dict):
        """Return a df with columns 'item_id' and 'ratings' for an individual user's survey results"""
        survey_standardized = self.standardize_survey_results(ratings_dict)
        #make a new dictionary with keys=restaurant_id, values=user's rating
        id_to_rating = {k: survey_standardized[v] for k, v in self.inverted_alias_dict.items() if v in survey_standardized}
        user_ratings_df = pd.DataFrame.from_dict(id_to_rating, orient='index')
        user_ratings_df.reset_index(inplace=True)
        user_ratings_df.rename(columns={'index':'item_id', 0:'rating'}, inplace=True)
        return user_ratings_df
    
    def get_user_factors_array(self, item_factors_array, restaurant_idxs, user_ratings_df):
        latent_item_features = item_factors_array[restaurant_idxs]
        ratings = user_ratings_df['rating'].values
        user_factors_array, residuals, rank, s = np.linalg.lstsq(latent_item_features, ratings) 
        return user_factors_array

    def user_preds_from_survey(self, user_survey):
        """Return a df of predictions user preferences for every restaurant, given the user's survey results"""
        
        for k, v in user_survey.items():

            user_ratings_df = self.get_user_ratings_df(v)
            rest_idxs = self.get_restaurant_indexes(user_ratings_df, self.item_factors_df)
            user_factors_array = self.get_user_factors_array(self.item_factors_array, rest_idxs, user_ratings_df)

            new_user_preds = self.new_user_predict(user_factors_array, self.item_factors_array, k)
            new_user_named_preds = self.change_rest_ids_to_aliases(new_user_preds, self.inverted_alias_dict)
            return new_user_named_preds
    
    def add_to_preds_df(single_user_preds_df):
        return pd.concat([self.preds_df, single_user_preds_df], axis=0, sort=False)
        
    def sort_recs_for_two(self, user1, user2, preds_database):    
        u1 = preds_database.loc[user1]
        u2 = preds_database.loc[user2]
        double_df = pd.concat([u1, u2], axis=1, sort=False)
        double_df['mean'] = double_df.mean(axis=1)
        return double_df.sort_values(by=['mean'], ascending=False)
    
    def get_a_rec(self, user1, user2, preds_database):
        sorted_recs = sort_recs_for_two(user1, user2, preds_database).head(30)
        normalized_weights = sorted_recs['mean'] / sorted_recs['mean'].sum()
        return sorted_recs.sample(1, weights=(sorted_recs['mean'] / normalized_weights))

