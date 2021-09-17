#!/usr/bin/python3
"""Index for our web flask"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """
    Return json status of web flask
    """
    status = {'status': 'OK'}
    return jsonify(status)
