#!/usr/bin/python3
"""
Index endpoint
"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
	"""
	return status in JSON
	"""
	return jsonify(status= "OK")



