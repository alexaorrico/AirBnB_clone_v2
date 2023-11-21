#!/usr/bin/python3
"""
defines views 4 stat
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """
    returns a json route for stat
    """
    return jsonify({"status": "OK"})
