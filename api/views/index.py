#!/usr/bin/python3

from flask import Flask
from models import storage
from api.v1.views import app_views


@app_views.route("/status")
def get_status():
    """ Shows the HTTP status 200 ok"""
    return jsonify({"status": "OK"}), 200