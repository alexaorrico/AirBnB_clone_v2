#!/usr/bin/python3
"""index """
from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route("/status")
def app_views():
    """return the status"""
    return jsonify({"status": "OK"})
