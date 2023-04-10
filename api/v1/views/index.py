#!/usr/bin/python3
"""This file contains the definition of API routes v1"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """Returns a JSON object indicating the state of the API"""
    return jsonify({'status': 'OK'})
