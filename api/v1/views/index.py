#!/usr/bin/python3
"""
Module defining routes for api
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """ Display a json of the status """
    return jsonify(status="OK")
