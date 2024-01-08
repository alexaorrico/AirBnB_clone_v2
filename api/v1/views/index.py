#!/usr/bin/python3
"""index file for the api views"""

from api.v1.views import app_views
from flask import jsonify, request


@app_views.route('/status', methods=['GET'])
def status():
    """
    endpoint for the /status route
    """

    if request.method == 'GET':
        data = {"status": "OK"}
        return jsonify(data)
