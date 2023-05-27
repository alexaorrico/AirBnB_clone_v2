#!/usr/bin/python3
"""API endpoint index file"""
from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status')
def get_status():
    """Returns HTTP Json status 200"""
    return jsonify({"status": "OK"}), 200
