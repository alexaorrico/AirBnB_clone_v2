#!/usr/bin/python3
"""A simple route view """
from flask import jsonify
from api.v1.views import app_views

# Define route for index
@app_views.route('/', methods=['GET'])
def index():
    return jsonify(message='Welcome to the API!')

# Define route for status
@app_views.route('/status', methods=['GET'])
def status():
    return jsonify(status='OK')
