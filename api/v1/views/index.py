#!/usr/bin/python3
from flask import jsonify
"""
    We import the 'jsonify' function from Flask
    to format the responses in JSON format.
"""
# We import the route set 'app_views' from the current module.
from . import app_views

# We define a route '/status' that responds to GET requests.
@app_views.route('/status', methods=['GET'])
def get_status():
    # We create a JSON response with an "OK" status message.
    return jsonify({"status": "OK"})
