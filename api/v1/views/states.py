#!/usr/bin/python3
"""States"""


from flask import jsonify, Response, abort, request, make_response
from werkzeug.exceptions import BadRequest
import json
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """Retrieves the list of all States"""
    states = [state.to_dict() for state in storage.all(State).values()]
    resp = Response(
        # The indent=4 argument is used to add indentation
        response=json.dumps(states, indent=4),
        status=200,
        # Sets the MIME type of the response to indicate that
        # it is in JSON format.
        mimetype='application/json'
    )
    return resp


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_by_id(state_id):
    """Retrieve a State by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a new State
    """
    if not request.is_json:
        return make_response("Not a JSON", 400)
    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')

    new_state = State(**data)
    new_state.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update an existing state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        raise BadRequest('Not a JSON', 400)
    data = request.get_json(silent=True)
    for key, value in data.items():
        # Ignore keys: id, created_at, and updated_at
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
