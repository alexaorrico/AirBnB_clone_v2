#!/usr/bin/python3
"""
This module contains the view for State objects
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def states():
    """retrieves the list of all State objects"""
    states = storage.all(State)
    return jsonify([obj.to_dict() for obj in states.values()])


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """retrieves a State object using its id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_state_by_id(state_id):
    """deletes a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def create_state():
    """create a new State object"""
    data = request.get_json(silent=True)
    if not data:
        abort(400, "Not a JSON")
    if not data.get('name'):
        abort(400, "Missing name")
    obj = State(**data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """updates a State object"""
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict())
