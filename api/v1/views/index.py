#!/usr/bin/python3
""" Gives the status of the api """
from flask import jsonify
from api.v1.views import app_views
import json


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def app_status():
    """ Returns the status of the app in json format """
    return jsonify({"status": "OK"})
