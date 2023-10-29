#!/usr/bin/python3
""" Handles all default RESTful API action """
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states():
	states = storage.all("State")
	states_list = []
	for state in states.values():
		states_list.append(state.to_dict())
	return jsonify(states_list), 200


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id):
	state = storage.get(State, state_id)
	if not state:
		abort(404, description="State not found")
	return jsonify(state.to_dict()), 200


@app_views.route(
		'/states/<state_id>', strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
	state = storage.get(State, state_id)
	if not state:
		abort(404)
	state.delete()
	storage.save()
	return jsonify({}), 200


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def post_state():
	if not request.get_json():
		abort(400, description="Not a JSON")
	if 'name' not in request.get_json():
		abort(400, description="Missing name")
	data = request.get_json()
	new_state = State(**data)
	storage.new(new_state)
	storage.save()
	return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def put_state(state_id):
	if not request.get_json():
		abort(400, description="Not a JSON")
	state = storage.get(State, state_id)
	if not state:
		abort(404)
	if 'name' not in request.get_json():
		abort(400, description="Missing name")
	data = request.get_json()
	for key, value in data.items():
		if key != "id" and key != "created_at" and key != "updated_at":
			setattr(state, key, value)
	storage.save()
	return jsonify(state.to_dict()), 200
