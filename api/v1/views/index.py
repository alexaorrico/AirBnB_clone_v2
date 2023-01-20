#!/usr/bin/python3
'''Defines the JSON GET request from the application'''
from api.v1.views import app_views


@app_views.route("/status", methods=["GET"])
def status():
    '''Returns JSON status'''
    return jsonify({"status": "OK"})
