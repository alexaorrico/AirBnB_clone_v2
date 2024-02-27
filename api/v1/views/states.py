#!/usr/bin/python3
"""
Routes for handling state objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import State

@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_all_states():
    """
    Retrieve all state objects
    :return: JSON of all states
    """
    state_list = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(state_list)

@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """
    Create a state
    :return: Newly created state object
    """
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    if "name" not in state_json:
        abort(400, 'Missing name')

    new_state = State(**state_json)
    new_state.save()
    resp = jsonify(new_state.to_dict())
    resp.status_code = 201

    return resp

@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state_by_id(state_id):
    """
    Get a specific state object by ID
    :param state_id: State object id
    :return: State object with the specified id or error
    """
    obj_fetched = storage.get(State, str(state_id))
    if obj_fetched is None:
        abort(404)
    return jsonify(obj_fetched.to_dict())

@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state_by_id(state_id):
    """
    Update a specific state object by ID
    :param state_id: State object ID
    :return: State object and 200 on success, or 400 or 404 on failure
    """
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    obj_fetched = storage.get(State, str(state_id))
    if obj_fetched is None:
        abort(404)
    for key, val in state_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(obj_fetched, key, val)
    obj_fetched.save()
    return jsonify(obj_fetched.to_dict())

@app_views.route("/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def delete_state_by_id(state_id):
    """
    Delete a state by id
    :param state_id: State object id
    :return: Empty dict with 200 or 404 if not found
    """
    obj_fetched = storage.get(State, str(state_id))
    if obj_fetched is None:
        abort(404)
    storage.delete(obj_fetched)
    storage.save()
    return jsonify({}), 200
