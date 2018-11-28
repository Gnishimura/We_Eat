import numpy as np

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

