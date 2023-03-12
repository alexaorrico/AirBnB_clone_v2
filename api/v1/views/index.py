#!/usr/bin/python3
""" API index views module """

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """
    Returns json response as the status
    Returns:
        JSON: json object
    """
    status = {
        "status": "OK"
    }
    return jsonify(status)
