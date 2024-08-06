#!/usr/bin/python3
""" module containing the status route """
from . import app_views
from flask import jsonify

@app_views.route("/status")
def status():
    return jsonify({"status": "OK"})
