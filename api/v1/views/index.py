#!/usr/bin/python3
"""
    Module of blueprints of flask
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status")
def status_ok():
    return jsonify({'status': 'OK'})
