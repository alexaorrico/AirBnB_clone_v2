#!/usr/bin/python3
"""index.py that returns a JSON"""

from api.v1.views import app_views, jsonify


@app_views.route("/status")
def status():
    """ status method"""
    data = {
        'status': 'OK'
    }
    return (jsonify(data))
