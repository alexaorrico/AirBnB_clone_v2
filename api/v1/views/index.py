#!/usr/bin/python3
"""blueprint for app_views"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    '''returns the status of the server'''
    return jsonify({'status': 'OK'})
