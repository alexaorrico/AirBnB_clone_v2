#!/usr/bin/python3
"""state view"""
from models.amenity import Amenity
from models.user import User
from models.state import State
from models.review import Review
from models.place import Place
from models.city import City
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request
import json
import re


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """return a list of dictionary states"""
    states = storage.all(State).values()
    states_list = []
    for state in states:
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """return state for a given id"""
    my_state = storage.get(State, state_id)
    if my_state is None:
        abort(400)
    return jsonify(my_state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state_by_id(state_id):
    """delete state for a given id and return an empty dictionary"""
    my_state = storage.get(State, state_id)
    storage.delete(my_state)
    storage.save()
    if my_state is None:
        abort(400)
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """post a new state as a dictionary"""
    try:
        form = request.get_json()
    except Exception as e:
        abort(400, "Not a JSON")

    if form['name'] is None:
        abort(400, "Missing name")
    my_state = State(**form)
    storage.new(my_state)
    storage.save()
    return jsonify(my_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state_by_id(state_id):
    """delete state for a given id and return an empty dictionary"""
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, 'Not a JSON')
    my_state = storage.get(State, state_id)
    if my_state:
        for key, value in data.items():
            if key not in ("id", "created_at", "updated_at"):
                setattr(my_state, key, value)
        storage.save()
    else:
        abort(404)
    return jsonify(my_state.to_dict()), 200
