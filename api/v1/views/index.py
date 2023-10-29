#!/usr/bin/python3
'''
This Python script creates a route `/status` on the object app_views.
'''

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def api_status():
    '''
    This method returns a JSON response for the RESTful API health.
    '''
    response = {'status': 'OK'}
    return jsonify(response)
