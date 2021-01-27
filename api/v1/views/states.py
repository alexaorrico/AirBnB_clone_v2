#!/usr/bin/python3
"""View for State objects that handles all default RestFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def all_states():
    """Retrieves the list of all State objects"""
    states = []
    for key, val in storage.all("State").items():
        states.append(val.to_dict())
    return jsonify(states)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def obj_state(state_id):
    """Retrieves a State objec"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    kwargs = request.get_json()
    state = State(**kwargs)
    storage.new(state)
    storage.save()
    return (jsonify(state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    content = request.get_json()
    if content is None:
        abort(400, description='Not a JSON')
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for key, val in content.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(state, key, val)
    storage.save()
    return (jsonify(state.to_dict()), 200)
