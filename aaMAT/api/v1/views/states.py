#!/usr/bin/python3
"""adasda"""
from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/api/v1/states', methods=['GET'])
def getStates():
	states = []
	for state in storage.all("State").values():
		states.append(state.to_dict())
	return jsonify(state)
