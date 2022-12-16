#!/usr/bin/python3
""" state objects handles all default RESTFul API"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states_all():
    """Retrieves the list of all State objects: GET /api/v1/states"""
    states = []
    for state in storage.all("State").values():
        states.append(state.to_dict())
    return jsonify(states)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states_id(state_id):
    """Retrieves a State object: GET /api/v1/states/<state_id>"""
    states = storage.all("State")
    if state_id is None:
        abort(404, description="Not found")
    return jsonify(states.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state_id(state_id):
    """Deletes a State object:: DELETE /api/v1/states/<state_id>"""
    states = storage.all("State")
    for key, value in states.items():
        if value.id == state_id:
            storage.delete(value)
            storage.save()
            return {}, 200
        abort(404)

@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_state():
    """Creates a State: POST /api/v1/states"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = State(**request.get_json())
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """Updates a State object: PUT /api/v1/states/<state_id>"""
    state = storage.get("State", state_id)
    if state_id is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(state, attr, val)
    state.save()
    return jsonify(state.to_dict())
