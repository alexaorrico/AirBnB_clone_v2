#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import jsonify, request


@app_views.route('/status', methods=['GET'])
def status():
    """returns status"""
    if request.method == 'GET':
        status = {
            "status": "OK"
        }
        return (jsonify(status))
