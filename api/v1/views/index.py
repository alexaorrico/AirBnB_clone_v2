#!/usr/bin/python3
'''BLueprint implementation for app'''

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
    '''Return status'''
    return jsonify({"status": "OK"})
