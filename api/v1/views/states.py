#!/usr/bin/python3
"""API endpoints for managing State objects.

Provides methods to retrieve, update and delete State objects
in the storage model.
"""
from api.v1 import app
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.state import State
from flasgger.utils import swag_from


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ define get states """
    states = storage.all(State)
    return jsonify([state.to_dict() for state in states.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ define id for states """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ delete request """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    """ create states """
    data = request.get_json()
    if not data:
        return jsonify(error="Not a JSON"), 400
    if "name" not in data:
        return jsonify(error="Missing name"), 400

    state = State(name=data['name'])
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ update states """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify(error="Not a JSON"), 400

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()

    return jsonify(state.to_dict()), 200
