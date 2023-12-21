#!/usr/bin/python3
"""index task 4"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """returns the API status"""
    return jsonify({'status': 'OK'})
