#!/usr/bin/python3
"""
returns a JSON: "status": "OK"
"""
from api.v1.views import app_views
from flask import jsonify, request


@app_views.route('/status', methods=['GET'])
def status_rt():
    """ returns status route ok for GET """
    if request.method == 'GET':
        return jsonify({"status": "OK"})
