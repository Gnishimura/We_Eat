import requests
import yaml
import pandas as pd
from pymongo import MongoClient
import time

# client = MongoClient(???)
mc = MongoClient()

db = mc['we_eat']
rc = db['restaurants']


offsets = list(range(1, 2000, 50))

#for starting_point in offsets:
default_params = {
    'location': '98104',
    'limit': 50,
    'term': 'restaurant'
    }

def load_api_key(filename='/Users/gnishimura/.secrets/yelp_api_key.yaml'):
    with open(filename) as f:
        keys = yaml.load(f)
    api_key = keys['api_key']
    
    return api_key

def make_request(params, api_key):
    '''Takes in a set of parameters and offsets, and outputs a populated database of restaurants, 
    taken off the Yelp Fusion API.'''

    url = "https://api.yelp.com/v3/businesses/search"
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    return data.get('businesses', None)

def build_database(start=1, end=1101, location=None):
    params = default_params.copy()
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
    if rc.count_documents({'id': row['id']}) == 0:
        rc.insert_one(row)

def retrieve_database():
    """Return the contents of MongoDB as a dataframe."""
    return pd.DataFrame(list(rc.find({})))
