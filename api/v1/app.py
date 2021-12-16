#!/usr/bin/python3
"""
the app module
"""
from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify



app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
