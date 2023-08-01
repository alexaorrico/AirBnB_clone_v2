#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """
    Get the status of the API.

    Returns:
        JSON: {"status": "OK"}
    """
    return jsonify({"status": "ok"})
