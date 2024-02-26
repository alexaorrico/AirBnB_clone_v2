#!/usr/bin/python3
"""
flask route with json response
"""
from api.v1.views import app_views
from flask import jsonify, request


@app_views.route('/status', methods=['GET'])
def status():
    """function that returns the status"""
    if request.method == 'GET':
        resp = {"status": "OK"}
        return jsonify(resp)