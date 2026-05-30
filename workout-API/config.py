# config.py
# handles initialization: Flask app, database connections & security extensions

import os 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate 
from flask_restful import Api
from flask_bcrypt import Bcrypt 

app = Flask(__name__)

# secret key: signing session cookies
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'super-secret-dev-key')

# data configuration 
app.config['SQLACHEMY_DATABASE_URI'] = 'sqlite:///workout_tracker.db'
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = flask_restful

# initalize extensions 
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
api = Api(app)