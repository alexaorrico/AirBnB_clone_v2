#!/usr/bin/python3
"""
starts a Blueprint
"""

from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status')
def status_check():
	return jsonify({"status": "OK"})
