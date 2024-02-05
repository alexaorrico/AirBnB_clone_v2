#!/usr/bin/python3
"""
A route that returns JSON: "status":"ok"
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """
    function for status route
    """
    if request.method == 'GET':
        resp = {"status": "OK"}
        return jsonify(resp)
