#!/usr/bin/python3
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify

@app_views.route('/status', strict_slashes=False)
def route_status():
    return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False)
def statsRoute():
    count = storage.count()
    return jsonify({})

if __name__ == "__main__":
    pass