#!/usr/bin/python3
''' index and status view for the API'''
from flask import jsonify

from api.v1.views import app_views


@app_views.route('/status')
def get_api_status():
    '''Gets the status of the api
    '''
    # return jsonify(status='OK')
    return jsonify({'status': "OK"})
