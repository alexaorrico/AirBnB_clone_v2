#!/usr/bin/python3
"""This module houses the index for the api"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def status():
    """ returns the status 'ok' if api is running """
    return jsonify({'status': 'OK'})
