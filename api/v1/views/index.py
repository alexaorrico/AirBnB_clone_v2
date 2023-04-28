#!/usr/bin/python3
"""Index file for JSON"""

from api.v1.views import app_views
from flask import jsonify


@app.route('/status'):
    def app_views():
        """Return a JSON"""
        return jsonify({'status': 'OK'})
