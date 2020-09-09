#!/usr/bin/python3
"""Index file using blueprint"""
from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/status', strict_slashes=False)
def index():
    """return a status"""
    return jsonify({"status": "OK"})

if __name__ == "__main__":
    pass
