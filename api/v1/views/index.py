#!/usr/bin/python3
"""define a route /status on the app_views blueprint"""
from flask import jsonify
from . import app_views


@app_views.route('/status')
def status():
    """returns json format of {"status": 'OK'}"""
    return jsonify({"status": "OK"})
