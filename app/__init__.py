"""
AngelHackDC 2013: Songlister

"""

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/songlister.db"
db = SQLAlchemy(app)

from app import views, models
