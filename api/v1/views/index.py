#!/usr/bin/python3
"""index.py file"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """returns status of app"""
    return jsonify({'status': 'OK'})
