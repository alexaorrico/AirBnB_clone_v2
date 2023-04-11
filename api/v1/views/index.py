#!/usr/bin/python3
"""Return status """
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", methods=['GET'])
def return_status():
    """Return status of GET request"""
    return jsonify({'status': 'OK'})

