#!/usr/bin/python3
""" Module for index.py """

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def get_route():
    """ Returns first json object """
    return jsonify({"status": "OK"})
