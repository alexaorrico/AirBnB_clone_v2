#!/usr/bin/python3
"""Index Package"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """JSON response giving the api status
    """
    return jsonify({"status": "OK"})
