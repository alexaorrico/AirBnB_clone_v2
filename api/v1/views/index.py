#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import jsonify, request


@app_views.route('/status', methods=['GET'])
def status():
    """
    func for status route
    """
    if request.method == 'GET':
        response = {"status": "OK"}
        return jsonify(response)
