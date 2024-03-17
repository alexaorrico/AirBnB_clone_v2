#!/usr/bin/python3
""" API views for states objects
Allows routes to list, get, delete, create, and update states
as requested. """

from flask import request, jsonify, abort
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Returns a jsonify'd list of all State objects."""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Returns a singular State object.
        Returns Error 404 if none found. """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    # If we got here, that's an error.
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a state."""
    # Check if the Content-Type is application/json
    if request.content_type != 'application/json':
        abort(400,
              description="Invalid Content-Type. Expects 'application/json'")
    state_data = request.get_json()
    # Currently, we don't have a global error catch for
    # 400's, so set them manually.
    if not state_data:
        abort(400, description="Not a JSON")
    if 'name' not in state_data:
        abort(400, description="Missing name")
    state = State(**state_data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """This deletes a state."""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    # Again, if you're here, you're an error.
    abort(404)


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """This updates a state. If one is correctly passed that is."""
    # Check if the Content-Type is application/json
    if request.content_type != 'application/json':
        abort(400,
              description="Invalid Content-Type. Expects 'application/json'")
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        abort(400, description="Not a JSON")
    for key, value in json_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
