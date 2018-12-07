from flask import Flask, render_template

app = Flask(__name__, static_url_path='')

#loaded_model = pickle.load(open('____.sav', 'rb'))
#prediction = get_pred_one(url, loaded_model)


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)