#!/usr/bin/python3
"""create a route /status on the object app_views"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def get_status():
    return jsonify({"status": "OK"})
