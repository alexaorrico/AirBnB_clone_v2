#!/usr/bin/python3
"""
This module contains the routes for the web application
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status")
def status():
    """status of API"""
    return jsonify({'status': "OK"})
