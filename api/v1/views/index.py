#!/usr/bin/python3
""""""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns status of API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def count_objet():
    