from flask import Flask, render_template
from ALS import ALSRecommender


app = Flask(__name__, static_url_path='')

#loaded_model = pickle.load(open('____.sav', 'rb'))
#prediction = get_pred_one(url, loaded_model)

with open('item_factors_df.pkl', 'rb') as f:
    item_factors = pickle.load(f)




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
    survey_results = {}
    login()
    survey_results["Gabe"] = request["user_data"]
    

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    """Return a recommendation, given two usernames."""
    data = request.json
    prediction = model.predict_proba([data['user_input']])
    return jsonify({'probability of spam': prediction[0][1]})




if __name__ == '__main__':
    app.run(debug=True)