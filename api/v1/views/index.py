#!/usr/bin/python3
"""
This module defines a Flask blueprint for handling status requests.
"""
from flask import jsonify

# We import the route set 'app_views' from the current module.
from . import app_views

# We define a route '/status' that responds to GET requests.
@app_views.route('/status', methods=['GET'])
def get_status():
    # We create a JSON response with an "OK" status message.
    return jsonify({"status": "OK"})
