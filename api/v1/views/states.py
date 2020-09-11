#!/usr/bin/python3
"""View for State objects that handles
    all default RestFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def get_states():
    """Retrieves the list of all State bjects: GET /api/v1/states"""
    states = []
    all_states = storage.all(State).values()
    for state in all_states:
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object: GET /api/v1/states/<state_id>"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a state object by it's id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states',
                 strict_slashes=False,
                 methods=['POST'])
def create_state():
    """Creates a State: POST /api/v1/states"""
    req_json = request.get_json()
    if not req_json:
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'name' not in req_json:
        return jsonify({'error': 'Missing name'}), 400
    else:
        _state = State(**req_json)
        storage.new(_state)
        storage.save()
        return jsonify(_state.to_dict()), 201


@app_views.route('/states/<state_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """Updates a State object: PUT /api/v1/states/<state_id>"""
    update_obj = storage.get(State, state_id)
    req_json = request.get_json()
    if not req_json:
        return jsonify({'error': 'Not a JSON'}), 400
    if update_obj:
        for key, value in req_json.items():
            setattr(update_obj, key, value)
        storage.save()
        return jsonify(update_obj.to_dict()), 200
    else:
        abort(404)
