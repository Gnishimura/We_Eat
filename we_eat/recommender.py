import pandas as pd
import numpy as np
import sys

class RestaurantRecommender():
    
    def __init__(self, main_database, user_matrix, restaurant_matrix):
        self.main_database = main_database
        self.user_matrix = user_matrix
        self.restaurant_matrix = restaurant_matrix
        
    def build_ratings_matrix(self):
        """Using the user and restaurant matrices, output a ratings matrix with users as rows and restaurants as columns"""
        ratings_matrix = self.user_matrix.dot(self.restaurant_matrix.T) 
        #divide by num of features that the row contains
        self.ratings_matrix = (ratings_matrix / (self.restaurant_matrix.sum(axis=1))) 
        return self.ratings_matrix

    def find_individual_recs(self, user, ratings_matrix, n=None):
        """Input user alias, number of recs, ratings matrix, and popularity series.  Output a sorted series"""
        if n:
            n == n
        popularity_weight = np.log(np.log(self.main_database['popularity'] + 1) + 1)
        average_rating_weight = np.log(self.main_database['rating'])

        unweighted_prefs = ratings_matrix.loc[user]
        weighted_prefs = unweighted_prefs * popularity_weight * average_rating_weight
        return weighted_prefs.sort_values(ascending=False)[:n]


    def max_sat_recs(self, user1, user2, n=None):
        """Input two usernames and output a sorted pandas dataframe with the restaurants that received the
        highest average ratings between the two users"""

        u1 = self.find_individual_recs(user1, self.ratings_matrix)
        u2 = self.find_individual_recs(user2, self.ratings_matrix)
        
        recs_df = pd.concat([u1, u2], axis=1, sort=False)
        recs_df['mean'] = recs_df.mean(axis=1)
        return recs_df.sort_values(by=['mean'], ascending=False)[:n]
    
    def min_dissat_recs(self, user1, user2, n=None):
        recs_df = self.max_sat_recs(user1, user2)
        pass

    def produce_recs(self, user1, user2):
        # recs_df = self.max_sat_recs(user1, user2)
        # recs_df = recs_df['mean'] > 
        # recs_df.sample()
        
        pass




def main(var1, var2):
    pass


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stdout.write('Incorrect arguments: use this format: ')
    argv1 = sys.argv[1]
    argv2 = sys.argv[2]
    main(argv1, arv2)