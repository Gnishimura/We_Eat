import numpy as np
import pandas as pd

from IPython.display import Image, display
from IPython.core.display import HTML 

def get_urls(restaurants_list, df):
    restaurant_aliases = np.array(restaurants_list)
    urls = df.loc[df['alias'].isin(restaurant_aliases), 'image_url']
    names = df.loc[df['alias'].isin(restaurant_aliases), 'alias']
    return urls, names

def display_pics(restaurants_list, df):
    urls, names = get_urls(restaurants_list, df)
    restaurant_names = dict(zip(names, urls))
    for key, value in restaurant_names.items():
        print(key)
        display(Image(url=value, width=200, height=200))

def find_most_popular(df, categories):
    most_popular = []
    for category in categories:
        temp_df = df[df[category]==1]
        most_popular.append(df.loc[temp_df['popularity'].idxmax()]['alias'])
        print(f"{category}:".format(), df.loc[temp_df['popularity'].idxmax()]['alias'])
    
    return most_popular
        