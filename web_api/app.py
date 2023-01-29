# Imports
from flask import Flask, render_template, request, jsonify
import datetime
import joblib

# Instantiate the app
app = Flask(__name__)

# define the prediction function

# Definine prediction fucntion
def return_prediction(model, input_json):
    # Serializes the input json to a list of list of features
    # i.e. [ [x1, x2 , x3, x4, x5]    ]
    # makes two list for extra safe?
    # Could just use one by removing one pair of [] below in input_data
    input_data = [[input_json[k] for k in input_json.keys()]]
    # Since our input_data is [[x1, x2, x3]], hence [0] to retrieve
    # the feature array
    prediction = model.predict(input_data)[0]
    return prediction

# loading the model
model = joblib.load("abalone_predictor.joblib")

# You could have multiple routes to indicate which page you are in
# Index route
@app.route("/")
def index():
    return render_template("index.html", utc=datetime.datetime.utcnow())

# About route
@app.route("/about")
def about():
    return render_template("about.html")

# Credits route
@app.route("/credits")
def credit():
    return render_template("credits.html")

# Prediction route
@app.route("/predict", methods=["POST"])
def predict():
    content = request.json
    results = return_prediction(model, content)
    return jsonify(results)
