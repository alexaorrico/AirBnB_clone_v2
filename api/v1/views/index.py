#!/usr/bin/python3
"""Includes Flask routes for airbnb clone"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns status of API"""
    if request.method == 'GET':
        answer = ({"status": "OK"})
        return jsonify(answer)
