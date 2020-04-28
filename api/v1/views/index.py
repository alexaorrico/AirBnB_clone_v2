#!/usr/bin/python3
""" index """
from api.v1.views import app_views
from flask import jsonify, make_response

@app_views.route('/status')
def route():
    """ Return a Json response """
    return make_response(jsonify({'status': 'OK'}))
