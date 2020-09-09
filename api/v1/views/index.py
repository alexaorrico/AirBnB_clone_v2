#!/usr/bin/python3
"""Return the status of API"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"}), 200
