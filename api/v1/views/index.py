#!/usr/bin/python3
# Imports app_views and creates /status route on app_views
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    '''returns JSON: "status": OK'''
    result = {'status': 'OK'}
    return jsonify(result), 200
