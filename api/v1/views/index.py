#!/usr/bin/python3

"""endpoint that ritrievs the number of each objects by type"""

from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """checks status of api"""
    return jsonify({"status": "OK"}), 200

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """retrieve stats"""
    return jsonify(storage.count()), 200
