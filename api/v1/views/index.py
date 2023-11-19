#!/usr/bin/python3
""" index for RESTful API """
import app_views from api.v1.views
from flask import jsonify

@app_views.route("/status")
def status():
    """ Status of API """
    return jsonify({"status": "OK"})
