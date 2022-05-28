#!/usr/bin/python3
"""index from views"""

from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify


@app_views.route("/status", strict_slashes=False)
def status():
    """method status"""
    return jsonify({"status": "OK"})
