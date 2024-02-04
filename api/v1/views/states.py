#!/usr/bin/python3
from flask import abort, jsonify, request
from models.__init__ import storage
from models.state import State
from api.v1.views import app_views

#Retrieve handle
@app_views.route('/states', methods=['GET'])
def get_states():
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])

#Retrieve spesific object
@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())

#Delete handle
@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

#Create handle
@app_views.route('/states', methods=['POST'])
def create_state():
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')

    data = request.get_json()
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201

#Update handle
@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)

    state.save()
    return jsonify(state.to_dict()), 200

#Error if state_id is not linked to any object
@app_views.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404
