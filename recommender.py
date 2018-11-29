import pandas as pd
import numpy as np


def average_user_ratings(restaurant_matrix, user_ratings_dict):
    """Takes a user's picture ratings (the results of the survey) in dictionary form,
    and the restaurant (item matrix), and returns the user's average ratings for each feature """
    ratings = restaurant_matrix.copy()
    for key, value in user_ratings_dict.items():
        ratings.loc[restaurant_matrix['alias'] == key] *= value
    return ratings.mean()

def update_user_ratings(user, user_matrix, restaurant_matrix, user_ratings_dict):
    """Input user name as string, user_matrix pd dataframe, and average ratings from average_user_ratings,
    ouput an updated user matrix"""
    average_rats = average_user_ratings(restaurant_matrix, user_ratings_dict)
    user_matrix.loc[user] = average_rats


def find_top_recs(user, n, ratings_matrix):
    """Input user alias, number of recs, and the ratings matrix.  Output a sorted series"""
    unweighted_prefs = ratings_matrix.loc[user]
    weighted = unweighted_prefs * np.log(popularity + 1)
    return weighted.sort_values(ascending=False)[:n]


