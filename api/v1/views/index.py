#!/usr/bin/python3
""" Creates a route """
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """ Creates a route that returns JSON """
    return jsonify({"status": "OK"})
