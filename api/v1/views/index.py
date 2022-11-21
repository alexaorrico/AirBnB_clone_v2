#!/usr/bin/python3
"""This module is a blueprint"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    status = {
            "status": "OK"
            }
    return status
