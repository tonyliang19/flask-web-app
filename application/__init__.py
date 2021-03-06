from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from flask_restx import Api

# Instantiate the api
api = Api()

# Instantiate the app
app = Flask(__name__)
# Reads the config file
app.config.from_object(Config)

# Instiate a db connection
db = MongoEngine()
# connects app to db
db.init_app(app)
# Initialize the api
api.init_app(app)

# These import should stay here and not above, otherwise infinite loop?
from application import routes

