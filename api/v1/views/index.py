#!/usr/bin/python3
"""
module to control the view part
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """return json text """
    return jsonify({"status": "OK"})
