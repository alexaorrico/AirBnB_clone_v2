#!/usr/bin/python3
'''
Module contains the routes to be used for the API.
'''

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def app_status():
    '''Returns the status code.'''
    return jsonify({'status': 'OK'})
