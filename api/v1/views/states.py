#!/usr/bin/python3
"""
Create a new view for State objects
that handles all default RESTFul API actions
"""

import json
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """Retrieves the list of all State objects"""
    objs = storage.all(State)
    return jsonify([obj.to_dict() for obj in objs.values()])


@app_views.route(
    '/states/<state_id>',
    methods=['GET'],
    strict_slashes=False)
def get_states_id(state_id):
    """Retrieves a State object"""
    obj = storage.get(State, state_id)
    if obj is not None:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route(
    '/states/<state_id>',
    methods=['DELETE'],
    strict_slashes=False)
def del_states_id(state_id):
    """Deletes a State object"""
    _ = get_states_id(state_id)
    obj = storage.get(State, state_id)
    storage.delete(obj)
    storage.save()
    storage.reload()
    return make_response({}, 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_states():
    """Creates a State"""
    try:
        data = request.get_json()
        if not data:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if data.get('name') is None:
            return make_response(jsonify({'error': 'Missing name'}), 400)
    except Exception:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    obj = State(**data)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route(
    '/states/<state_id>',
    methods=['PUT'],
    strict_slashes=False)
def update_states(state_id):
    """Updates a State object"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
        return
    try:
        new_data = request.get_json()
        if not new_data:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if new_data.get('name') is None:
            return make_response(jsonify({'error': 'Missing name'}), 400)
    except Exception:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for k, v in new_data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(obj, k, v)

    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)
