#!/usr/bin/python3
"""Index file for api views"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """Returns the API status"""

    return jsonify({'status': 'OK'})
