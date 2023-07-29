#!/usr/bin/python3
''' Defines routes '''
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    ''' returns status in JSON '''
    return jsonify({"status": "OK"})
