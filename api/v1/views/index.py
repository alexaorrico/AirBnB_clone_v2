#!/usr/bin/python3
""" for starting api """
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False)
def status():
    '''returns a JSON: "status": "OK"'''
    return jsonify({'status': 'OK'})
