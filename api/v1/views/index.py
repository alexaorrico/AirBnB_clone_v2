#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import request, jsonify


@app_views.route('/status')
def status():
    """ return JSON response OK """
    if request.method == 'GET':
        return jsonify({"status": "OK"})
