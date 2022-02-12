#!/usr/bin/python3
""" contain routes on app_views blueprint """

from api.v1.views import app_views
from flask import jsonify, request


@app_views.route('/status', methods=['GET'])
def status():
    """
    function for status route
    """
    if request.method == 'GET':
        return jsonify({"status": "OK"})
