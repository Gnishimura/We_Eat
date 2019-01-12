import pandas as pd
import numpy as np
from statistics import mean, stdev

import pickle

# Import pandas df containing info from review scrape

als_df = pd.read_pickle('data/als_df.pkl')
als_df.reset_index(drop=True, inplace=True)
als_df = als_df[['user_id', 'item_id', 'rating', 'date']]

class ALSRecommender():
    """Initialize with an item_factors_df and inverted_alias_dict, then use method 
    min_dissat_recs to get a rec"""
    def __init__(self, item_factors_df, inverted_alias_dict):
        self.item_factors_df = item_factors_df
        self.item_factors_array = np.array(self.item_factors_df['features'].tolist())
        self.inverted_alias_dict = inverted_alias_dict

    def single_rec(self, user1, user2, preds_df):
        """Return a single, random, weighted recommendaton from the user's top 30 restaurants"""
        sorted_recs = self.min_dissat_recs(user1, user2, preds_df, 30)
        normalized_weights = sorted_recs['mean'] / sorted_recs['mean'].sum()
        return sorted_recs.sample(1, weights=(sorted_recs['mean'] / normalized_weights))

    def min_dissat_recs(self, user1, user2, preds_df, n=None):
        """Input two usernames and output a sorted pandas dataframe with the restaurants that received the
        highest average and, in the case of ties, the highest minimum ratings between the two users"""
        preds_df['mean'] = preds_df.mean(axis=1).round(1)
        preds_df['min'] = preds_df.min(axis=1)
        preds_df_sorted = preds_df.sort_values(by=['mean','min'], ascending=False)
        return preds_df_sorted[:n]
    
    def get_combined_preds_df(self, user1_df, user2_df):
        """Return the 'preds_df' that contains both user's predicted scores for every restaurant"""
        preds_df = pd.concat([user1_df, user2_df], axis=0, sort=False).round(1)
        return preds_df

    def user_preds_from_survey(self, user_survey):
        """Return a df of predictions of user preferences for every restaurant, given the user's survey results"""
        raw_user_ratings_df = self.get_raw_ratings_df(user_survey['survey'])
        rest_idxs = self.get_restaurant_indexes(raw_user_ratings_df, self.item_factors_df)
        user_factors_array = self.get_user_factors_array(self.item_factors_array, rest_idxs, raw_user_ratings_df)

        ids_user_df = self.new_user_predict(user_factors_array, self.item_factors_array, user_survey['user'])
        user_df = self.ids_to_aliases(ids_user_df, self.inverted_alias_dict)
        normed_user_df = self.normalize(user_df)
        return normed_user_df
    
    def normalize(self, user_df):
        return (user_df - float(user_df.min(axis=1))) / (float(user_df.max(axis=1) - user_df.min(axis=1))) * 5

    def get_restaurant_indexes(self, raw_user_ratings_df, item_factors_df):
        """Return an array of restaurant indexes that were reviewed by a particular user"""
        rest_idxs = []
        for item in raw_user_ratings_df['item_id']:
            rest_idx = self.item_factors_df.index[self.item_factors_df['id']==item]
            rest_idxs.append(rest_idx[0])
        return np.array(rest_idxs)

    def get_raw_ratings_df(self, user_survey):
        """Return a df with columns 'item_id' and 'ratings' for an individual user's survey results"""
        #survey_standardized = self.standardize(user_survey)
        #make a new dictionary with keys=restaurant_id, values=user's rating
        standardized_dict = {k: user_survey[v] for k, v in self.inverted_alias_dict.items() if v in user_survey}
        raw_user_ratings_df = pd.DataFrame.from_dict(standardized_dict, orient='index')
        raw_user_ratings_df.reset_index(inplace=True)
        raw_user_ratings_df.rename(columns={'index':'item_id', 0:'rating'}, inplace=True)
        return raw_user_ratings_df

    def get_user_factors_array(self, item_factors_array, restaurant_idxs, raw_user_ratings_df):
        """Return a user_factors_array to be used by new_user_predict()"""
        latent_item_features = item_factors_array[restaurant_idxs]
        ratings = raw_user_ratings_df['rating'].values
        user_factors_array, residuals, rank, s = np.linalg.lstsq(latent_item_features, ratings) 
        return user_factors_array

    def new_user_predict(self, user_factors_array, item_factors_array, username):
        """Return a new df with a single row containing the users predictions for every restaurant"""
        new_factor_list =[]
        for i in range(len(item_factors_array)):
            new_factor_list.append(np.dot(user_factors_array, item_factors_array[i]))
        new_user_preds = pd.DataFrame([new_factor_list], index=[username])
        return new_user_preds
    
    def ids_to_aliases(self, user_df, inverted_alias_dict):
        """Use the inverted alias dictionary to rename columns by restaurant alias"""
        named_user_df = user_df.rename(inverted_alias_dict, axis=1)
        return named_user_df
        




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

    # def compile_preds_df(self, all_surveys):
    #     preds = []
    #     for k, v in all_surveys.items():
    #     preds.append(self.get_preds_from_single_survey_results(k, v))
    #     return pd.concat(preds, axis=0, sort=False)

    # def sort_recs_for_two(self, user1, user2, preds_df): 
    #     """Return the sorted datafram with restaurants containing the highest mean score between two users"""   
    #     u1 = preds_df.loc[user1]
    #     u2 = preds_df.loc[user2]
    #     double_df = pd.concat([u1, u2], axis=1, sort=False)
    #     double_df['mean'] = double_df.mean(axis=1)
    #     return double_df.sort_values(by=['mean'], ascending=False)


    # def standardize(self, survey):
    #     """Standardize survey results"""
    #     ave = mean(survey.values())
    #     sd = stdev(survey.values())
    #     return {k: (v-ave)/sd for k, v in survey.items()}





