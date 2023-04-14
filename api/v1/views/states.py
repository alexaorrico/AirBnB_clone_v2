#!/usr/bin/python3
"""
file for "/api/v1/states" API
with GET, POST, PUT and DELETE
"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route(
        "/states",
        methods=["GET"]
    )
def all_state_objects_in_JSON():
    """
    Returns all State objects in 'storage',
    in dictionary form,
    which is JSON serializable.
    """
    return jsonify(
        {
            key: state.to_dict()
            for key, state in
            storage.all(State).items()
        }
    )

@app_views.route(
        "/states/<state_id>",
        methods=["GET"]
    )
def get_state_in_JSON(state_id):
    """
    Returns the State with the 'state_id'
    argument and route in 'storage',
    in its JSON-serializable dict form,
    if the State object exists.

    Raises 404 otherwise.
    """
    result = storage.get(State, f"State.{state_id}")

    if result is None:
        abort(404)

    print(result.to_dict())

    return jsonify(result.to_dict())


@app_views.route(
        "/states/<state_id>",
        methods=["DELETE"]
    )
def delete_state_by_id(state_id):
    """
    Deletes State object with 'state_id' as its 'id'
    field/column value (let's call it 'target')
    from 'storage.all' dictionary, by calling storage.delete(<target>)

    Returns ({}, 200) if successful,
    404 if 'target' doesn't exist.
    """
    target = storage.get(State, state_id)

    if target is None:
        abort(404)
    storage.delete(target)

    return jsonify({}), 200


@app_views.route(
        "/states/",
        methods=["POST"]
    )
def post_state_by_id():
    """
    Creates new State object based on
    JSON input and the State and BaseModel
    constructors (these constructors are in
    <project root>/models/).

    If the input provided isn't valid JSON
    or if the JSON provided has no 'name' key,
    this function calls 'flask.abort(400)',
    with a message of what went wrong:
    either "Not a JSON" or "Missing name".
    """
    new_state_in_JSON = request.get_json()
    # Automatically calls 400 when POST request
    # has invalid JSON.
    # So, this new state object MUST be valid
    # (if the keys are also valid):
    if 'name' not in new_state_in_JSON:
        abort(400, "Missing name")

    new_state = State(**new_state_in_JSON)
    storage.new(new_state)
    return new_state, 201


@app_views.route(
    "/states/<state_id>",
    methods=["PUT"])
def put_state_in_JSON(state_id):
    """
    Overrides State object with id in PUT request
    (??)
    """
    if f"State.{state_id}" not in storage.all(State):
        abort(404)

    new_state_info = request.get_json()

    state = storage.get(State, state_id)
    # state acts like a "pointer" to the State object,
    # so it doesn't need to be put back
    # in the storage.
    if 'name' in new_state_info:
        state.name = new_state_info['name']
    
    return jsonify(state.to_dict()), 200
