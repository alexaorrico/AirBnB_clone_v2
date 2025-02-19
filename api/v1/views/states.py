#!/usr/bin/python3
"""States API"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


def err_404(e):
    """Page not found"""
    if not e:
        abort(404)


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def list_states():
    """Retrieve states"""
    return jsonify([state.to_dict() for state
                   in storage.all(State).values()]), 200


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_id(state_id):
    """Retrieve state Using state ID"""
    data = storage.get(State, state_id)
    if not data:
        err_404(data)
    return jsonify(data.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete State with id"""
    data = storage.get(State, state_id)
    if not data:
        abort(404)
    else:
        storage.delete(data)
        storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_states():
    """ Post State """
    if not request.is_json:
        return jsonify('Not a JSON')

    data = request.get_json()

    if 'name' not in data:
        abort(404, 'Missing name')

    inst = State(**data)
    inst.save()

    return jsonify(inst.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_states(state_id):
    """update state information give state ID"""

    state = storage.get(State, state_id)

    if not state:
        abrot(404)

    if not request.is_json:
        abort(404, "Not a JSON")

    data = request.get_json()

    if 'name' not in data:
        abort(404, "Missing name data")

    ignore_fields = ['id', 'updated_at', 'created_at']

    for key, value in data.items():
        if key not in ignore_fields:
            setattr(state, key, value)

    storage.save()

    return jsonify(state.to_dict()), 200
