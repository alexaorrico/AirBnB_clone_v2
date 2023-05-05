#!/usr/bin/python3
""" state objects thst handles all RESTFUL api actions"""

from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """returns list of all json objects"""
    return jsonify([i.to_dict() for i in storage.all(State).values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """returns a particular state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete a state object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a state object"""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400
    state = State(name=data['name'])
    state.save()

    return jsonify(stat.to.dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state():
    """update state object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    ignore = ['id', 'created_at', 'updated_at']

    data_request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
