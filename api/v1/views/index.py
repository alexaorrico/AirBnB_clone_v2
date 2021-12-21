#!/usr/bin/python3
"""Display the Index File"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """Status"""
    status = {"status": "OK"}
    return jsonify(status)
