#!/usr/bin/python3
'''Contains the blueprint for the API.'''
from flask import jsonify

from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    '''Gets the status of the API.
    '''
    return jsonify(status='OK')
