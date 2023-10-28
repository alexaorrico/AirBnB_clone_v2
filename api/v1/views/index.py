#!/usr/bin/python3
"""
views for our project
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def ok_status():
    """
    return an ok json status
    """
    return jsonify({"status": "OK"})
