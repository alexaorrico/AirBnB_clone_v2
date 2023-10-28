#!/usr/bin/python3
""" API status"""

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', strict_slashes=False)
def status():
	""" Return OK"""
	return jsonify(status='OK')


