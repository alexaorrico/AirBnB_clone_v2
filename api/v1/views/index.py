#!/usr/bin/python3
""" Your first endpoint (route) will be to return the status of your API """
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status_ok():
    """ prints json rep. status: ok """
    to_print = {"status": "OK"}
    return jsonify(to_print)
