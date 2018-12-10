from flask import Flask, render_template
from ALS_recommender import ALSRecommender
import pandas as pd
import numpy as np

import pickle

app = Flask(__name__, static_url_path='')

with open('item_factors_df.pkl', 'rb') as f:
    item_factors = pickle.load(f)

with open('inv_alias_dict.pickle', 'rb') as g:
    inv_alias_dict = pickle.load(g)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    """Takes a username and makes it a key of the survey_results dictionary"""
    data = request.json
    pass

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    """Compiles a dictionary of survey results and makes that dict a value 
    (corresponding to the username key above) in the survey_results dictionary"""

    data = request.json
    login()
    survey_results["Gabe"] = request["user_data"]
    

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    """Return a recommendation, given two usernames."""
    data = request.json
    recommender = ALSRecommender(item_factors, inv_alias_dict)
    single_user_survey_results = recommender.get_preds_df_from_survey(#insert survey results from website here)
    recommender.add_to_preds_df(single_user_survey_results)
    recommender.get_a_rec(user1, user2)

    prediction = model.predict_proba([data['user_input']])

    return jsonify({'go eat HERE!': prediction[0][1]})




if __name__ == '__main__':
    app.run(debug=True)