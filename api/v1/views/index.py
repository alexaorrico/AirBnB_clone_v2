#!/usr/bin/python3
"""
script that starts a Flask web application:
"""

from api.v1.views import app_views
from flask import jsonify, Flask, Response
from models import storage


@app_views.route('/status')
def status():
    """
    Status
    """
    status = {"status": "OK"}
    return jsonify(status)
