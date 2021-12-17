#!/usr/bin/python3
"""
index module
"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route("/status", methods=["GET"])
def status():
    """
    returns json string
    """
    return jsonify({"status": "OK"})
