#!/usr/bin/python3
'''
Import Blueprint to create routes
'''
from api.v1.views import app_views
from flask import Response
import json


@app_views.route('/status')
def status():
    '''Function to route status, return a json'''
    m = {
        'status': 'OK'
    }
    return Response(json.dumps(m), mimetype='application/json')
