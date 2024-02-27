#!/usr/bin/python3
'''
Create a route `/status` that returns a JSON: "status": "OK".
'''


from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def api_status():
    '''
    Returns a JSON response "status": "OK".
    '''
    response = {'status': 'OK'}
    return jsonify(response)
