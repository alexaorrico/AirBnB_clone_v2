#!/usr/bin/python3
""" This module initializes the blueprint app_views """

from flask import jsonify
from api.v1.views import app_views

# Create a route /status on the object app_views
# that returns a JSON: "status": "OK"
@app_views.route('/status', methods=['GET'])
def status():
    """ Returns a JSON: "status": "OK """
    return jsonify(status="OK")
