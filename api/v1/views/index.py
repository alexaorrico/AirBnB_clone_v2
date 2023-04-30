#!/usr/bin/python3

""" This module contains the routes for the web application
"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def get_status():
    """ status code"""
    return jsonify(status="ok")
