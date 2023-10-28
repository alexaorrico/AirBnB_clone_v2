#!/usr/bin/python3
"""A host file for status of objects of api blueprint."""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def get_status():
    """Function to get status of API"""
    return jsonify(status="OK")
