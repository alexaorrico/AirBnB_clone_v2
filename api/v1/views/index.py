#!/usr/bin/python3
"""create a file index.py"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Status"""
    return jsonify({"status": "OK"})
