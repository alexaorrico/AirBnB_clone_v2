#!/usr/bin/python3

"""
Create a new view for State objects that handles
all default RestFul API actions.
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def getAll():
    """Retrieve all objects"""
    l = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(l)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get(state_id):
    """Retrieve an object by id"""
    obj = storage.get(State, state_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete(state_id):
    """Delete a state object by id"""
    obj = storage.get("State", state_id)
    if obj:
        obj.delete()
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create():
    """Create an object"""
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    if body.get('name') is None:
        abort(400, "Missing name")
    d = request.get_json()
    obj = State(**d)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update(state_id):
    """Update an object"""
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    for k, v in body.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict()), 200
