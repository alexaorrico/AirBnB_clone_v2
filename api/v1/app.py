#!/usr/bin/python3
""" HBNB flask application """

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


