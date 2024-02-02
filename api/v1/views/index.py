#!/usr/bin/python3
"""
a route /status on the object app_views
returns a JSON: "status": "OK" (see example)
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status',  methods=['GET'])
def index():
    return jsonify({"status": "OK"})
