#!/usr/bin/python3
"""creating routs on app_views obj"""

from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.routs('status')
def status():
    """returns a JSON and The Status"""
    return jsonify({"status": "OK"})
