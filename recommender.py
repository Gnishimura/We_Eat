import pandas as pd
import numpy as np


def average_user_ratings(restaurant_matrix, user_ratings_dict):
    """Takes a user's picture ratings (the results of the survey) in dictionary form,
    and the restaurant (item matrix), and returns the user's average ratings for each feature """
    ratings = restaurant_matrix.copy()
    for key, value in user_ratings_dict.items():
        ratings.loc[key] *= value
    average_ratings = ratings.mean()
    return average_ratings

def standardize_ratings(average_ratings):
    return (average_ratings - average_ratings.mean())/average_ratings.std()

def update_user_ratings(user, user_matrix, restaurant_matrix, user_ratings_dict):
    """Input user name as string, user_matrix pd dataframe, and average ratings from average_user_ratings,
    ouput an updated user matrix"""
    average_rats = average_user_ratings(restaurant_matrix, user_ratings_dict)
    standardized_rats = standardize_ratings(average_rats)
    user_matrix.loc[user] = standardized_rats

def find_individual_recs(user, ratings_matrix, popularity_scores, n=None):
    """Input user alias, number of recs, ratings matrix, and popularity series.  Output a sorted series"""
    if n:
        n == n
    unweighted_prefs = ratings_matrix.loc[user]
    weighted = unweighted_prefs * np.log(popularity_scores + 1)
    return weighted.sort_values(ascending=False)[:n]


def produce_recs(user1, user2, n):
    
    u1 = find_top_recs(user1, R, popularity)
    u2 = find_top_recs(user2, R, popularity)
    
    recs_df = pd.concat([u1, u2], axis=1)
    recs_df['mean'] = recs_df.mean(axis=1)
    return recs_df.sort_values(by=['mean'], ascending=False)[:5]
