import logging
from os import environ

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)

# App Config
app.config.update(
    DEBUG=(environ.get('DEBUG') == 'yes'),
    SECRET_KEY=environ.get('SECRET_KEY'),
    SQLALCHEMY_DATABASE_URI=environ.get('DATABASE_URL')
)

# Setup Logging
logger = logging.getLogger('soundem')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

# Initialize database
db = SQLAlchemy(app)

from soundem import models, views, handlers
