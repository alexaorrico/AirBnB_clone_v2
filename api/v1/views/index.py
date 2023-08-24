#!/usr/bin/python3
"""
Status route on app_views
"""
from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.run('/status', strict_slashes=False)
def status():
    return jsonify({'status': 'OK'})
