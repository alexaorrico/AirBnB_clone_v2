#!/usr/bin/python3
"""
States view
"""

from flask import Flask, jsonify, request, abort, Blueprint
from api.v1.views import app_views
from models import storage
from models.state import State

app = Flask(__name__)


@app_views.route('/danny', methods=['GET'], strict_slashes=False)
def get_danny():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State"""
    content = request.get_json()
    if content is None:
        abort(400, "Not a JSON")
    if 'name' not in content:
        abort(400, "Missing name")
    new_state = State(**content)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    content = request.get_json()
    if content is None:
        abort(400, "Not a JSON")
    for key, value in content.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())
