#!/usr/bin/python3
"""adasda"""
from os import abort
from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/states', methods=['GET'])
def getStates():
	"""aaasdasdasd"""
	states = []
	for state in storage.all("State").values():
		states.append(state.to_dict())
	return jsonify(state)

@app_views.route('/states/<state_id>', methods=['GET'])
def getStateById(state_id):
	"""asdasdasda"""
	state = storage.get("State", state_id)
	if state is None:
		abort(404)
	state = state.to_dict()
	return jsonify(state)
