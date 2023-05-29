#!/usr/bin/python3
"""app_views index file"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def get_status():
    """method to get status and return a JSON file"""
    return jsonify({"status": "OK"})
