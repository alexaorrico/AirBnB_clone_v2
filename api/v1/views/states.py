#!/usr/bin/python3
"""
handles all default RestFul API actions for states
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from flask import request
from flask import abort
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_states(state_id=None):
    """
    get all the states
    """
    list_objects = []

    if state_id is None:
        for item in storage.all(State).values():
            list_objects.append(item.to_dict())

        return jsonify(list_objects)
    else:
        data = storage.get(State, state_id)
        if data is None:
            abort(404)
        return jsonify(data.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Delete a state by id
    """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    state.delete()
    storage.save()

    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    if not request.get_json():
        abort(400, "Not a JSON")

    json_data = request.get_json()
    if "name" not in json_data:
        abort(400, "Missing name")

    new_state = State(**json_data)
    storage.new(new_state)
    storage.save()

    return (jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """
    update the state by id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    json_data = request.get_json()
    if "name" not in json_data:
        abort(400, "Missing name")

    for key, value in json_data.items():
        if key not in ["id", "updated_at", "created_at"]:
            setattr(state, key, value)
    state.save()

    return jsonify(state.to_dict())
