#!/usr/bin/python3
"""Import Modules"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def get_status():
    """Returns the app status"""
    return jsonify({"status": "OK"})
