#!/usr/bin/python3
"""
routes module
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status", methods=['GET'])
def status():
    ''' returns status code of the api '''
    return jsonify(status="OK")
