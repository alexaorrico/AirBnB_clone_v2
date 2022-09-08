#!/usr/bin/python3
"""adasda"""
from ast import Return
from crypt import methods
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.state import State


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
	state = storage.get(State, state_id)
	if state is None:
		abort(404)
	state = state.to_dict()
	return jsonify(state)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def deleteState(state_id):
	"""asdasdasda"""
	
	state = storage.get(State, state_id)
	if state is None:
		abort(404)
	storage.delete(state)
	storage.save()
	return jsonify({}), 200

@app_views.route("/states", methods=['POST'])
def create_state():
	json_req = request.get_json()
	if json_req is None:
		abort(400, 'Not a JSON')
	if json_req.get("name") is None:
		abort(404, 'Missing name')
	new_obj = State(**json_req)
	new_obj.save()
	return jsonify(new_obj.to_json()), 201
