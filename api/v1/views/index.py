#!/usr/bin/python3
"""basic routes for the Flask App"""
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status')
def status_api():
    """Tests the status of API"""
    return jsonify({"status": "OK"})
