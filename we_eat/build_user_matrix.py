import pandas as pd
import numpy as np
import sys

class BuildUserMatrix():
    """Class that compiles a user matrix in the proper form to be used by the RestaurantRecommender class.  
    Has methods compile (which initializes the user matrix) and update (which adds a single user's results)"""

    def __init__(self, restaurant_matrix, survey_results_list, user_names):
        self.restaurant_matrix = restaurant_matrix
        self.survey_results_list = survey_results_list
        self.user_names = user_names

        self.survey_restaurants = survey_results_list[1].keys()
        self.survey_restaurant_matrix = self.restaurant_matrix.loc[self.survey_restaurants, :]
        
    def standardize_ratings(self, average_ratings):
        """Takes in the average ratings from a user and standardizes them"""
        return (average_ratings - average_ratings.mean())/average_ratings.std()

    def compile(self):
        """Takes in the survey results list and assigns values to each category that the user rated."""

        #Create an empty user matrix
        user_matrix = pd.DataFrame(columns=self.survey_restaurant_matrix.columns,
                                   index=self.user_names)

        #iterate over each user (dictionary) in the survey results list
        for i, user in zip(self.user_names, self.survey_results_list):

            feature_rating_matrix = self.survey_restaurant_matrix.copy()

            #iterate over each restaurant (key) and rating (value) in the user's dictionary
            for restaurant, rating in user.items():
                feature_rating_matrix = feature_rating_matrix.replace(0, np.NaN)  #replace 0s with NaNs so that your average doesn't include unrated features
                if restaurant in feature_rating_matrix.index:
                    feature_rating_matrix.loc[restaurant, :] *= rating    #broadcast user's ratings of restaurants over the restaurant matrix to get the user's ratings of features

            #take the average rating for each feature that corresponded to each restaurant that the user rated
            average_ratings = feature_rating_matrix.mean(axis=0)
            #average_ratings.replace(1.0, 0, inplace=True)
            #standardize
            standardized_rats = self.standardize_ratings(average_ratings)
            
            user_matrix.loc[i, :] = standardized_rats.values

        return user_matrix.replace(np.NaN, 0)

    def update(self, username, single_survey_results_dict, user_matrix):
        """Input user name as string, that user's survey results in dictionary form, and the user matrix, and outputs an
        updated user matrix"""
        # average_ratings = 
        # standardized_rats = self.standardize_ratings(average_ratings)
        # self.user_matrix.loc[i, :] = standardized_rats.values
        pass


    # popularity_weight_log = np.log(cleaned_df['popularity'] + 1)
    # average_rating_weight = cleaned_df['rating']