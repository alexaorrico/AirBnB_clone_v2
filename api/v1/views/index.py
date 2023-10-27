#!/usr/bin/python3
"""an object that returns a JSON: "status": "OK"""
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status', methods=['GET'])
def show_status():
    """returns the status"""
    if request.method == 'GET':
        resp = {"status": "OK"}
        return jsonify(resp)
