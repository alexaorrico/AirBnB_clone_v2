#!/usr/bin/python3

"""
Returns a JSON
"""
from api.v1.views import app_views
from flask import jsonify


"""Define a route /status on the app_views Blueprint"""
@app_views.route('/status')
def status():
    """A route that returns a JSON"""
    return jsonify({"status": "OK"})
