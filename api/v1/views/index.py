#!/usr/bin/python3
"""
returns json status response
"""

from api.v1.views import app_views
from flask import jsonify, request



@app_views.route('/status', methods=['GET'])
def status():
    """
    Returns a JSON: "status": "OK"
    """

    if request.method == 'GET':
        response = {"status":'OK'}
        return jsonify(response)