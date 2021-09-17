"""
    Module REST API routes that returns json responses
"""
from api.v1.views import app_views
from flask import jsonify, request


@app_views.route('/status', methods=['GET'])
def status():
    """
        Return status of '/status' route
    """
    if request.method == 'GET':
        resp = {"status": "OK"}
        return jsonify(resp)
