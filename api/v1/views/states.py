#!/usr/bin/python3
""" Routes for states """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=["GET"], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=["GET"], strict_slashes=False)
def state(state_id=None):
    """Get all states or state by id"""
    if state_id is None:
        states = storage.all("State")
        all_states = [value.to_dict() for key, value in states.items()]
        return jsonify(all_states)
    all_states = storage.get(State, state_id)
    if all_states is None:
        abort(404)
    return jsonify(all_states.to_dict()), 200


@app_views.route('/states/<state_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_states(state_id):
    """Deletes state based on ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return (jsonify({})), 200


@app_views.route('/states', methods=["POST"], strict_slashes=False)
def post_states():
    """Creates state"""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if "name" not in data.keys():
        abort(400, "Missing name")
    new_data = State(**data)
    new_data.save()
    return (jsonify(new_data.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=["PUT"], strict_slashes=False)
def put_states(state_id):
    """Updates state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    for key, value in req.items():
        if key in ['id', 'created_at', 'updated_at']:
            continue
        else:
            setattr(state, key, value)
    state.save()
    return (jsonify(state.to_dict()), 200)
