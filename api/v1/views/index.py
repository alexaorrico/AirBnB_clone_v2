#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify, request


@app_views.route('/status', METHOD=['GET'])
def status():
    """returns the status"""
    if request.method == 'GET':
        response = {"status": "OK"}
        return jsonify(response)
