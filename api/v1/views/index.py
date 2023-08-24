#!/usr/bin/python3
"""Module that have the route of app_views"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def hbnbstatus():
    """function that return json on status route"""
    return jsonify({'status': "OK"})
