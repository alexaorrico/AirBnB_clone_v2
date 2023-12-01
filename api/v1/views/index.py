#!/usr/bin/python3
""" The index module"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def get_status():
    """Return the status of the API."""
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats', methods=['GET'])
def get_obj():
    """Retrieves the number of each objects by type"""
    number_obj = storage.count()
    return jsonify(number_obj)
