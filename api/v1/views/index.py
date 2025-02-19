#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'])
def get_status():
    """Return the status of the API"""
    return jsonify({"status": "OK"})
