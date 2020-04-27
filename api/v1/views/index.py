#!/usr/bin/python3
"""
Flask index file that returns the json status response
"""
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """
    function for status route that returns the status
    """
    if request.method == 'GET':
        resp = {"status": "OK"}
        return jsonify(resp)
