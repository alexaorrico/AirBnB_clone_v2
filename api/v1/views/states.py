#!/usr/bin/python3
"""
This is a new view for `State` objects that handles all default RESTful ops
"""
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from . import app_views


@app_views.route('/states', methods=['GET'])
@app_views.route('/states/<state_id>', methods=['GET'])
def read_states(state_id=None):
    """Reads all `State` objects in storage, or specified `State` object"""

    if not state_id:
        states = storage.all(State).values()
        states = [state.to_dict() for state in states]
        return jsonify(states)

    state = storage.get(State, state_id)
    # no state_id with that id in storage
    if state is None:
        abort(404)

    return jsonify(storage.get(State, state_id).to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Delete a state with `id` == `state_id`"""

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    return {}, 200


@app_views.route('/states', methods=['POST'])
def create_state():
    """Creates a new `State`. Request must be in json and contain `name`
    attribute else request is aborted.

    Returns:
        response with dictionary representation of new `State`, and 201 code
    """

    attrs = request.get_json()
    _validate_json(attrs)

    # create the `State` object
    new_state = State(name=attrs['name'])
    new_state.save()

    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_states(state_id):
    """Updates a `State` object with id == `state_id`. Request must be in json
    and contain `name` attribute else request is aborted

    Args:
        state_id (str): id of the `State` object to update

    Returns:
        returns a `State` object with updated data, and 200 response code
    """

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    attrs = request.get_json()
    _validate_json(attrs)

    state.name = request.get_json().get('name', state.name)
    state.save()

    return jsonify(state.to_dict()), 200


def _validate_json(json_obj):
    """Validates format is json"""

    if json_obj is None:
        abort(400, 'Not a JSON')
    if 'name' not in json_obj:
        abort(400, 'Missing name')
