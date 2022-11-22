#!/usr/bin/python3
""" index file which returns json response on /status endpoint"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """ returns json response to the route"""
    return jsonify({"status": "OK"})
