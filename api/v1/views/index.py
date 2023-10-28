#!/usr/bin/python3
'''
creates the routestatus on the app_views object
'''
from flask import jsonify
from models import storage
from api.v1.views import app_views

@app_views.route('/status', methods=('GET'))
def api_status():
    '''
    Returns a json response of OK status
    '''
    response = {'status': 'OK'}
    return jsonify(response)
