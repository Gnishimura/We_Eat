import numpy as np
import pandas as pd
from clean_database import cat_counts

from IPython.display import Image, display
from IPython.core.display import HTML 

class PictureSurvey():
    def __init__(self, main_database):
        self.main_database = main_database
    
    def top_twenty(self):
        sorted_cat_list = cat_counts(self.main_database).most_common()[:20]
        top_cats = []
        for x in sorted_cat_list:
            top_cats.append(x[0])
        return top_cats

    #Later gotta make this so that if one restaurant is most popular in multiple categories
    #it chooses the next most popular (in order to get all unique restaurants)
    def find_highest_rated(self, categories):
        highest_rated_rests = []
        for category in categories:
            temp_df = self.main_database[self.main_database['category_' + category]==1]
            for i in range(3):
                if temp_df['popularity'].nlargest(3).index[i] not in highest_rated_rests:
                    highest_rated_rests.append(temp_df['popularity'].nlargest(2).index[i])
                else:
                    continue
            #print(f"{category}:".format(), temp_df['popularity'].nlargest(2).index[i])
        
        return highest_rated_rests

    def get_urls(self, restaurants_list):
        """Takes in a list of restaurants and the master dataframe"""
        restaurant_aliases = np.array(restaurants_list)
        urls = self.main_database.loc[self.main_database.index.isin(restaurant_aliases), 'image_url']
        names = urls.index.values
        return urls, names

    def display_pics(self, restaurants_list):
        urls, names = self.get_urls(restaurants_list)
        restaurant_names = dict(zip(names, urls))
        for key, value in restaurant_names.items():
            print(key, value)
            display(Image(url=value, width=200, height=200))



    def build_survey():
        pass
        