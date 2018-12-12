from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from pymongo import MongoClient

from ..ALS_recommender import ALSRecommender

import pickle

we_eat_client = MongoClient()
we_eat_database = we_eat_client['we_eat']
survey_collection = we_eat_database['surveys']
partner_collection = we_eat_database['partners']


app = Flask(__name__, static_url_path='')

with open('data/item_factors_df.pkl', 'rb') as f:
    item_factors = pickle.load(f)

with open('data/inv_alias_dict.pickle', 'rb') as g:
    inv_alias_dict = pickle.load(g)

@app.route('/')
def home():
    return render_template('stylish.html')


@app.route('/survey', methods=['POST'])
def survey():
    data = request.get_json()
    survey_collection.insert_one(data)
    print(data)
    return f"received data for {data['user']}"

@app.route('/recommend/<user1>/<user2>', methods=['GET'])
def recommend_for_two_users(user1, user2):
    """Return a recommendation, given two usernames."""
    user1_survey = survey_collection.find_one({'user': user1})
    user2_survey = survey_collection.find_one({'user': user2})
    recommender = ALSRecommender(item_factors, inv_alias_dict)
    user1_df = recommender.user_preds_from_survey(user1_survey)
    user2_df = recommender.user_preds_from_survey(user2_survey)
    compiled_df = recommender.compile_df(user1_df, user2_df)
    rec = recommender.get_a_rec(user1, user2, compiled_df)
    return f'https://www.yelp.com/biz/{rec.index[0]}'



if __name__ == '__main__':
    app.run(debug=True)