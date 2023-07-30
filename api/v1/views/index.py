#!/usr/bin/python3
"""create a route status"""
from flask import Blueprint, jsonify

# Create a variable app_views which is an instance of Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Create the route /status on the app_views Blueprint
@app_views.route('/status', methods=['GET'])
def get_status():
    status_data = {"status": "OK"}
    return jsonify(status_data)

# Wildcard import of everything in the package api.v1.views.index
from api.v1.views.index import *
