#!/usr/bin/python3
"""It’s time to start your API!"""
from flask import jsonify, make_response
from api.v1.views import app_views


@app_views.route('/status')
def json_status():
    """Create a route on the object app_views that returns a JSON"""
    return make_response(jsonify({"status": "OK"}))
