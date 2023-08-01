#!/usr/bin/python3
"""create a route /status on the object app_views
that returns a JSON"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """returns a JSON with status OK"""
    return jsonify({'status': 'OK'})
