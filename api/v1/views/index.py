#!/usr/bin/python3
""" api/vi/views/index.py"""

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methodes=['GET'])
def status():
    return jsonify({'status': 'OK'})
