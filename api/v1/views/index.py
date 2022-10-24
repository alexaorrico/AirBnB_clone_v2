#!/usr/bin/python3
"""Retrieves number for each type"""
from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False)
def status():
    """Returns status"""
    return jsonify({'status': 'OK'})

