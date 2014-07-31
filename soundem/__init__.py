import os
import logging

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# App Config
app.config.update(
    DEBUG=(os.environ.get('DEBUG') == 'yes'),
    SECRET_KEY=os.environ.get('SECRET_KEY'),
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL')
)

# Setup Logging
logger = logging.getLogger('soundem')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

# Initialize database
db = SQLAlchemy(app)

from soundem import models, views, handlers
