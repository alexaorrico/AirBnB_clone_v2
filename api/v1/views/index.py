#!/usr/bin/python3

"""
Returns a JSON
"""
from api.v1.views import app_views
from flask import Flask

@app_views.route('/status', methods=['GET'])
def get_status():
    """A route that returns a JSON"""
    return jsonify({"status": "OK"})
