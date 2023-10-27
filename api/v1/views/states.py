#!/usr/bin/python3
""" CRUD operation on state object"""
from models.state import State
from api.v1.views import app_views
from models import storage
from flask import jsonify
from flask import abort, request, make_response


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """
    The function `all_states` retrieves all instances of the
    `State` class from storage and returns them as a JSON list."""
    all_state = storage.all(State)
    my_list = []
    for i in all_state.values():
        my_list.append(i.to_dict())
    return jsonify(my_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_id(state_id):
    """
    The function `states_id` takes an ID as input and returns the
    corresponding state object as a JSON response, or raises a
    404 error if the state is not found.
    """
    state = storage.get(State, id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def states_id_delete(state_id):
    """
    The function `states_id_delete` deletes a state
    object from storage based on its ID.
    """
    state = storage.get(State, id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def states_post():
    """
    The function `states_post()` receives a JSON object,
    checks if it is valid, creates a new State object,
    saves it to storage, and returns the State object as a JSON response.
    """
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in data.keys():
        return make_response(jsonify({"error": "Missing name"}), 400)
    state = State(**data)
    # storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('states/<state_id>', methods=['PUT'], strict_slashes=False)
def states_put(state_id):
    """
    The function updates the attributes of a state object based
    on the provided JSON data and returns the updated state
    object as a JSON response."""
    state = storage.get(State, id)
    if state is None:
        abort(404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
