#!/usr/bin/python3
""" status of web server """
from api.v1.views import app_views
from models import storage
from flask import jsonify

@app_views.route("/status")
def status():
	return jsonify({ 'status': 'OK' })

@app_views.route("/api/v1/stats")
def stats():
	for clss in storage.classes:
		task = jsonify({clss : storage.count(storage.classes[clss])})
	return task