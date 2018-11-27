import pandas as pd

def clean_cats(categories):
    """Change list of categories into a string."""
    return ','.join(cat['alias'] for cat in categories)

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

