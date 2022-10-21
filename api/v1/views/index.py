#!/usr/bin/pyton3
"""
create a route status
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methodes=['GET'])
def json_string(self):
    """ return the JSON representation of the status of the flask"""
    new = {'status': 'OK'}
    return jsonify(new)
