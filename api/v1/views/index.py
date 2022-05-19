#!/usr/bin/python3
import json
from api.v1.views import app_views
from flask import Flask
from flask import jsonify


@app_views.route("/status", strict_slashes=False)
def status():
    """ Display the status of the API"""
    return jsonify({"status": "OK"})
