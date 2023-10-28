#!/usr/bin/python3
"""New view for State objects that handles all default RESTFul API actions."""

from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieve the list of all State objects.

    Returns:
        JSON response: A JSON response containing a list of all State objects.
    """
    states = storage.all(State)
    list_states = []
    for state in states.values():
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieve a State object.

    Args:
        state_id (str): The UUID4 string representing a State object.

    Returns:
        JSON response: A JSON response containing a State object.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Delete a State object.

    Args:
        state_id (str): The UUID4 string representing a State object.

    Returns:
        JSON response: An empty JSON response.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """
    Create a State object.

    Returns:
        JSON response: A JSON response containing a new State object.
    """
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    state = State(**request.get_json())
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """
    Update a State object.

    Args:
        state_id (str): The UUID4 string representing a State object.

    Returns:
        JSON response: A JSON response containing an updated State object.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())


if __name__ == '__main__':
    pass
