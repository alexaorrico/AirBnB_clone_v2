#!/usr/bin/python3
"""
module with route /status on object app_views
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """
    returns an OK Jsonified
    """
    return jsonify({"status": "OK"})


# @app_view.route('/api/v1/stats')
# def _counts():
#     """
#     retrieves the number of each objects per type
#     """
