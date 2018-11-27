import pandas as pd
from collections import Counter


def clean_cats(categories):
    """Change list of categories into a string."""
    return ','.join(cat['alias'] for cat in categories)

def cat_counts(categories):
    """Create a dictionary with a list of all the categories in the 'cats' feature and their counts"""
    cat_dict = Counter()
    for row in categories:
        temp = row.split(',')
        for cat in temp:
            cat_dict[cat] += 1
    return cat_dict

#get category dict with:  cat_counts = cat_counts(mile_from_galvanize_copy['cats'])

def load_categories():
    with open('categories.csv') as f:
        categories = [cat.strip() for cat in f.readlines()]
    return categories

categories = load_categories()

def get_category_dummies(categories_col, categories=categories):
    """Return a DataFrame of dummy columns for the categories specified."""
    cat_list_col = categories_col.str.split(',')
    df = pd.DataFrame(index=categories_col.index)
    for cat in categories:
        df['category_' + cat] = cat_list_col.apply(lambda cats: cat in cats).astype(int)
    
    return df

def prune_rare_cats(df):
    """Remove any categories that have less than 5 restaurants"""

    new_df = df.copy()
    categories = []
    [categories.append(item) for item in list(df.columns) if 'category_' in item]       
   
    [new_df.drop(columns=category, inplace=True) for category in categories if df[category].sum() < 5]
    
    return new_df

def add_popularity(df):
    """Make a popularity column based on average rating multiplied by number of reviews"""
    df['popularity'] = df['rating'] * df['review_count']

def separate_coords(df):
    """Change list of categories into a string."""
    return df['coordinates'].apply(lambda x: x['latitude']), df['coordinates'].apply(lambda x: x['longitude'])

def change_price_nulls(df):
    """Change all nulls to the mode of the price data, $$"""
    return df['price'].fillna(value='$$', inplace=True)

def dummify_price(df):
    """Change yelp's price categories ('$', '$$', '$$$, '$$$$') into dummy variables"""
    df['$'] = (df['price']=='$')*1
    df['$$'] = (df['price']=='$$')*1
    df['$$$'] = (df['price']=='$$$')*1
    df['$$$$'] = (df['price']=='$$$$')*1
 
def drop_unnecessaries(df):
    """Remove any permanently closed restaurants, and remove unused columns"""
    df_copy = df.copy()
    df_pruned = df_copy[df_copy['is_closed']==False]
    df_pruned.drop(columns=['_id', 'categories', 'coordinates', 'display_phone', 'is_closed', 'phone', 'price', 'name', 'display_phone'], inplace=True)
    return df_pruned

# #Clean categories
# mile_from_galvanize['cats'] = mile_from_galvanize['categories'].apply(clean_cats)

# #Separate coordinates into lats and longs
# mile_from_galvanize['lats'], mile_from_galvanize['longs'] = clean_coords(mile_from_galvanize)

# #Change nulls in price to $$
# change_price_nulls(mile_from_galvanize)

# #Dummify price
# dummify_price(mile_from_galvanize)

# #Drop unwanted rows and columns
# drop_unneccessaries(mile_from_galvanize)

