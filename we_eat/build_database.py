import requests
import yaml
import pandas as pd
from pymongo import MongoClient
import time

# client = MongoClient()
we_eat_client = MongoClient()

# create Mongo database and collection
we_eat_db = we_eat_client['we_eat']
restaurant_collection = we_eat_db['restaurants']

default_params = {
    'term': 'restaurant',
    'latitude': 47.5990148,
    'longitude': -122.3338371,
    'limit': 50,
    'radius': 1609,
    'categories': 'halal'
    }

def load_api_key(filename='/Users/gnishimura/.secrets/yelp_api_key.yaml'):
    """Input a file with API key.  Keeps API keys hidden in yaml file"""
    with open(filename) as f:
        keys = yaml.load(f)
    api_key = keys['api_key']
    
    return api_key

def make_request(params, api_key):
    '''Takes in a set of parameters and the api key, and outputs a populated database of restaurants, 
    taken off the Yelp Fusion API.'''

    url = "https://api.yelp.com/v3/businesses/search"
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    return data.get('businesses', None)

def build_database(start=0, end=1000, location=None):
    """Compiles database using load_api_key(), make_request(), and add_to_database_if_new.
    start and end are default based on yelp's 1000 business max return.  Location optional."""
    params = default_params
    if location:
        params['location'] = location
    offsets = range(start, end, 50)
    
    api_key = load_api_key()
    for offset in offsets:
        print(offset)
        params['offset']=offset
        data = make_request(params=params, api_key=api_key)
        if data is None:
            print("No businesses returned")
            break
        for row in data:
            add_to_database_if_new(row)
        time.sleep(1)

def add_to_database_if_new(row):
    """Only adds to MongoDB if the restaurant id is new"""
    if restaurant_collection.count_documents({'id': row['id']}) == 0:
        restaurant_collection.insert_one(row)

def retrieve_database():
    """Return the contents of MongoDB as a dataframe."""
    return pd.DataFrame(list(restaurant_collection.find({})))


# rest_db = build_database()
# mile_from_galvanize = retrieve_database()