#!/usr/bin/python3
"""
Route for handling state objects and operations
"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import State

@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_get_all():
    """
    Retrieves all state objects
    :return JSON list of all states
    """
    state_list = []
    state_obj = storage.all("State")
    for obj in state_obj.values():
        state_list.append(obj.to_dict())
    return jsonify(state_list)

@app_views.route("/states", methods=["POST"], strict_slashes=False)
def state_create():
    """
    Create a new state object
    
    :return: JSON of the newly created object
    """
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    if 'name' not in state_json:
        abort(400, 'Missing name')

    # create a new state object using the JSON data
    new_state = State(**state_json)
    new_state.save()

    # Return the new state object as JSON with 202 status code
    resp = jsonify(new_state.to_dict())
    resp.status_code = 201

    return resp

@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """
    Retrieve specific state object by ID
    :param state_id: state object ID
    :return: JSON of the state objects with the specific id or 404 error

    """
    # Fetch the state objects by ID
    fetched_obj = storage.get("State", str(state_id))
    # if the object is not found return 404 error
    if fetched_obj is None:
        abort(404)

    # Return the state object as JSON
    return jsonify(fetched_obj.to_dict())

@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def state_put(state_id):
    """
    Update a specific state object by ID
    :param state_id: state objects ID
    :return: JSON of the updated state object and 200 on success
    or 400 0r 404 on failure
    """
    # Get the JSON request body
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    fetched_obj = storage.get("State", str(state_id))
    if fetched_obj is None:
        abort(404)
    # update the state object with new values , ignoring certain keys
    for key, val in state_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    # Return the updated state object as JSON
    return jsonify(fetched_obj.to_dict())

@app_views.route("/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def state_delete_by_id(state_id):
    """
    Delete a State object by ID
    :param state_id: state object ID
    :return Empty dictionary with 200 status code or 404 if not found

    """
    # Fetch the state object by ID
    fetched_obj = storage.get("State", str(state_id))
    if fetched_obj is None:
        abort(404)

    # Delete the state object
    storage.delete(fetched_obj)
    storage.save()

    # Return an empty dictionary with a 200 status code
    return jsonify({})

