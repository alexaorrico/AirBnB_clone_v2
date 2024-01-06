#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def index():
    return jsonify({
		"status": "OK"
	})