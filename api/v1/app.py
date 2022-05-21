#!/usr/bin/python3
"""
Python flask
"""


from flask import Flask
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)

