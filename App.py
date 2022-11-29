import flask
from flask import Flask, redirect, url_for, request, render_template
import os
import pickle
import numpy as np

app = Flask(__name__, template_folder='templates')

@app.route('/')
@app.route('/index')
def index():
    AuthorName = "BPYD"
    return flask.render_template('index.html', user = AuthorName)

def predictor(predict_list):
    predict = np.array(predict_list).reshape(1, 2)
    loaded_model = pickle.load(
        open("./model/model.pkl", "rb"))
    result = loaded_model.predict(predict)
    return result

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        name = request.form['name']
        cholesterol = request.form['cholesterol']
        heart_rate = request.form['heart_rate']

        predict_list = list(map(int, [cholesterol, heart_rate]))
        result = predictor(predict_list)

        if int(result) == 0:
            prediction = 'You have no symptoms of heart failure'
        elif int(result) == 1:
            prediction = 'You have little bit symptoms of heart failure'
        elif int(result) == 2:
            prediction = 'You have symptoms of heart failure'

        return render_template('prediction.html', prediction=prediction, name=name)
if __name__ == '__main__':
    app.run(debug=True)