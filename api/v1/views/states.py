#!/usr/bin/python3
"""
file for "/api/v1/states" API
with GET, POST, PUT and DELETE
for getting, posting, putting and deleting
State objects in 'storage', imported from
'models', and saving those changes in the
'storage's database/JSON file.
"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route(
        "/states",
        strict_slashes=False,
        methods=["GET"]
    )
def all_state_objects_in_JSON():
    """
    Returns all State objects in 'storage',
    as a JSON, from the values returned
    by 'storage.all(State)'.
    """
    return jsonify(
        [
            state.to_dict()
            for state in
            storage.all(State).values()
        ]
    )


@app_views.route(
        "/states/<state_id>",
        strict_slashes=False,
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
    result = storage.get(State, state_id)

    if result is None:
        abort(404)

    return jsonify(result.to_dict())


@app_views.route(
        "/states/<state_id>",
        strict_slashes=False,
        methods=["DELETE"]
    )
def delete_state_by_id(state_id):
    """
    Deletes State object with 'state_id' as its 'id'
    field/column value (let's call it 'target')
    from 'storage.all' dictionary, by calling storage.delete(<target>)

    Returns ({}, 200) if successful,
    404 if 'target' doesn't exist.

    NOTE:
    If the state being deleted is related to cities,
    and the 'storage' variable is a 'DBStorage' instance,
    an SQLalchemy error will occur, since the
    state is related to cities.
    """
    target = storage.get(State, state_id)

    if target is None:
        abort(404)
    storage.delete(target)
    storage.save()

    return jsonify({}), 200


@app_views.route(
        "/states/",
        strict_slashes=False,
        methods=["POST"]
    )
def post_state_in_JSON():
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
    new_state_in_JSON = request.get_json(silent=True)
    # If the request's JSON isn't valid,
    # 'new_state_in_JSON' is None.
    if new_state_in_JSON is None:
        abort(400, "Not a JSON")

    if 'name' not in new_state_in_JSON:
        abort(400, "Missing name")

    new_state = State(**new_state_in_JSON)
    storage.new(new_state)
    storage.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route(
        "/states/<state_id>",
        strict_slashes=False,
        methods=["PUT"]
    )
def put_state_in_JSON(state_id):
    """
    Overrides State object's fields
    except for 'id', 'created_at' and 'updated_at',
    where the object's id is 'state_id',
    with the json attributes provided in the
    PUT request.

    If the state with 'state_id' as its 'id'
    doesn't exist, this function calls
    abort(404).

    Otherwise, this function returns the JSON
    format of the new state with code 200.
    """
    if storage.get(State, state_id) is None:
        abort(404)

    new_state_info = request.get_json(silent=True)
    # If the request's JSON isn't valid,
    # 'new_state_in_JSON' is None.
    if new_state_info is None:
        abort(400, "Not a JSON")

    state = storage.get(State, state_id)
    # state acts like a "pointer" to the State object,
    # so it doesn't need to be put back
    # in the storage.
    if 'name' in new_state_info:
        state.name = new_state_info['name']
    storage.save()
    # We have to re-write the object change
    # to the database/storage file,
    # so that the changes are saved
    # there too, and not just in this
    # Python object.

    return jsonify(state.to_dict()), 200
