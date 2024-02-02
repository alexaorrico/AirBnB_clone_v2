#!/usr/bin/python3
""" The implementation of blueprint for index routing behaviour"""
from api.v1.views import app_views


@app_views.route("/status")
def status():
    from flask import jsonify
    return jsonify({"status": "OK"})
