#!/usr/bin/python3
"""defines the route /status"""

from api.v1.views import app_views
from flask import jsonify

@app_views.route("/status")
def status():
	"""returns status of response"""
	return jsonify({"status": "OK"})
