#!/usr/bin/python3
'''Contains the index route for the API.'''
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
    '''Gets the status of the API.
    '''
    return jsonify(status='OK')
