from api.v1.views import app_views
from flask import request, jsonify
from models import storage

@app_views.route("/status", method=["GET"])
def status():
    """request status route"""
    return jsonify({"status": "OK"})