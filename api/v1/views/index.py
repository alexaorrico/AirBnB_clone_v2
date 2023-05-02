#!/usr/bin/python3
"""Load the json responses for the api"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def return_json():
    return jsonify(status="OK")
