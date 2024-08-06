#!/usr/bin/python3
from flask import Flask, Blueprint, jsonify
from flask import abort, request
from models import storage
from api.v1.views import app_views
from models.engine.db_storage import classes

@app_views.route("/states", strict_slashes=False, methods=["GET"])
def get_states():
    """Return all states
    """
    states = storage.all("State")
    states_list = []
    for s in states.values():
        states_list.append(s.to_dict())
    return jsonify(states_list)

@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
def get_state(state_id):
    """Retrieve a specific state by ID.
    Args:
        state_id: The ID of the state.
    Returns: A JSON response containing the details of the retreved state.
    Raises: 404: If the state with the specified ID does not exist.
    """
    state = storage.get(classes["State"], state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["DELETE"])
def delete_state(state_id):
    """Delete a state.
    Args:
        state_id: The ID of the state to delete.
    Returns: An empty JSON response.
    Raises:
        404: If the state with the specified ID does not exist.
    """
    state = storage.get(classes["State"], state_id)
    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()
    return jsonify({})


@app_views.route("/states/", strict_slashes=False, methods=["POST"])
def post_state():
    """Create a new state.
    Returns:  A JSON response containing the details of a new state.
    Raises:
        400: If the request data is not a valid JSON
             or if the 'name' field is missing.
    """
    state_data = request.get_json(force=True, silent=True)
    if type(state_data) is not dict:
        abort(400, "Not a JSON")

    if "name" in state_data:
        new_state = classes["State"](**state_data)
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201
    else:
        abort(400, "Missing name")


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def put_state(state_id):
    """Update an existing state.
    Args:
        state_id: The ID of the state to update.
    Returns:
        A JSON response containing state updated details.
    Raises:
        404: If the state ID does not exist.
        400: If the request data is not a valid JSON.
    """
    state = storage.get(classes["State"], state_id)
    if state is None:
        abort(404)

    data_json = request.get_json(force=True, silent=True)
    if type(data_json) is not dict:
        abort(400, "Not a JSON")

    for key, value in data_json.items():
        if key in ["id", "created_at", "updated_at"]:
            continue
        setattr(state, key, value)

    storage.save()
    return jsonify(state.to_dict())

