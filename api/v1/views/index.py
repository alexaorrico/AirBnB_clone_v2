#!/usr/bin/python3
'''Creates route that returns a JSON'''
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status_check():
    '''returns JSON that has only OK'''
    return jsonify({"status": "OK"})
