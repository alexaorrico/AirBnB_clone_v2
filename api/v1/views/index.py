#!/usr/bin/python3
"""
index.py
"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status_check():
    """Returns a JSON status message"""
    text_format = {'status': 'OK'}
    return jsonify(text_format)
