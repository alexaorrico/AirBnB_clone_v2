#!/usr/bin/python3

from api.v1.views import app_views
from models.storage import count

@app_views.route("/status")
def get_status():
    """gets a json status"""
    return jsonify({"status": "OK"})

@app.route("/api/v1/stats")
def 
