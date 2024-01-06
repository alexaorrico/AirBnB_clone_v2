#!/usr/bin/python3
""" index.py """


from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'])
def status():
    """Returns a JSON string"""
    return jsonify({"status": "OK"})
