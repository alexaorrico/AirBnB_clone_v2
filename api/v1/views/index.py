#!/usr/bin/python3
""" module"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """DOC"""
    return jsonify({"status": "OK"})
