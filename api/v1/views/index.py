#!/usr/bin/python3
"""display status OK!"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """Return the status OK"""
    return jsonify({'status': 'OK'})
