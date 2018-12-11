from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from pymongo import MongoClient

from ..ALS_recommender import ALSRecommender

import pickle

we_eat_client = MongoClient()
we_eat_database = we_eat_client['we_eat']

app = Flask(__name__, static_url_path='')

with open('../../data/item_factors_df.pkl', 'rb') as f:
    item_factors = pickle.load(f)

with open('../../data/inv_alias_dict.pickle', 'rb') as g:
    inv_alias_dict = pickle.load(g)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/survey', methods=['POST'])
def survey():
    data = request.get_json()
    survey_collection = we_eat_database['surveys']
    survey_collection.insert_one(data)
    print(data)
    return f"received data for {data['user']}"


@app.route('/recommend', methods=['POST'])
def recommend():
    """Return a recommendation, given two usernames."""
    data = request.get_json()
    #TODO(Gabe): get user 1 and user 2 from data
    user1 = survey_collection.find_one({'user': user1})
    user2 = survey_collection.find_one({'user': user2})
    recommender = ALSRecommender(item_factors_df, inv_alias_dict)
    user1_df = recommender.user_preds_from_survey(user1)
    user2_df = recommender.user_preds_from_survey(user2)
    compiled_df = recommender.compile_df(user1_df, user2_df)
    rec = recommender.get_a_rec(user1, user2, compiled_df)
    return jsonify({'go eat HERE!': rec})

@app.route('/recommend/<user1>/<user2>')
def recommend(user1, user2):
    """Return a recommendation, given two usernames."""
    user1 = survey_collection.find_one({'user': user1})
    user2 = survey_collection.find_one({'user': user2})
    recommender = ALSRecommender(item_factors_df, inv_alias_dict)
    user1_df = recommender.user_preds_from_survey(user1)
    user2_df = recommender.user_preds_from_survey(user2)
    compiled_df = recommender.compile_df(user1_df, user2_df)
    rec = recommender.get_a_rec(user1, user2, compiled_df)
    return jsonify({'go eat HERE!': rec})






if __name__ == '__main__':
    app.run(debug=True)