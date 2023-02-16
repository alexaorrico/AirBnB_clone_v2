#!/usr/bin/python3

from flask import jsonify
from api.v1.views import app_views
from models.storage import count

@app_views.route("/status")
def get_status():
    """gets a json status"""
    return jsonify({"status": "OK"})

@app.route("/api/v1/stats")
def get_stats():
    """endpoint that retrieves number of
    each object by type"""
    end_point = count()
    return jsonify(end_point)
