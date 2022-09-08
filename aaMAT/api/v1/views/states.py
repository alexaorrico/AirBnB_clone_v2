#!/usr/bin/python3
"""adasda"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def getStates():
	"""aaasdasdasd"""
	states = []
	for state in storage.all("State").values():
		states.append(state.to_dict())
	return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def getStateById(state_id):
	"""asdasdasda"""
	key = "State" + "." + "{}".format(state_id)
	state = storage.get(key)
	print(state)
	if state is None:
		abort(404)
	state = state.to_dict()
	print(state)
	return jsonify(state)
