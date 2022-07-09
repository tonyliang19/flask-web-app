# Imports
from flask import Flask, render_template
import datetime

# Instantiate the app
app = Flask(__name__)

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