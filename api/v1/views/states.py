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
"""from turtle import st"""


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
    states = storage.all(State).values()
    for state in states:
        if state.id == state_id:
            return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state_by_id(state_id):
    """delete state for a given id and return an empty dictionary"""
    states = storage.all(State).values()
    for state in states:
        if state.id == state_id:
            storage.delete(state)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    form = request.get_json()
