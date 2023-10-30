#!/usr/bin/python3
"""index.py to connect to API"""
from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/status', strict_slashes=False)
def status_ok():
    """Status Ok method"""
    return jsonify({"status": "OK"})

if __name__ == "__main__":
    pass
