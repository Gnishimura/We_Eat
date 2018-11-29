import pandas as pd
import numpy as np


def average_user_ratings(restaurant_matrix, user_ratings_dict):
    """Takes a user's picture ratings (the results of the survey) in dictionary form,
    and the restaurant (item matrix), and returns the user's average ratings for each feature """
    ratings = restaurant_matrix.copy()
    for key, value in user_ratings_dict.items():
        ratings.loc[key] *= value
    return ratings.mean()

def update_user_ratings(user, user_matrix, average_ratings):
    """Input user name as string, user_matrix pd dataframe, and average ratings from average_user_ratings,
    ouput an updated user matrix"""
    user_matrix.loc[user] = average_ratings

