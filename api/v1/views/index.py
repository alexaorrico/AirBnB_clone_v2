#!/usr/bin/python3
""" Module that returns an object """


from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """
    Return status ok
    Returns:
        json: status
    """
    return jsonify({"status": "OK"})
