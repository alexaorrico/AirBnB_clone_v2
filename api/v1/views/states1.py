#!/usr/bin/python3
"""creates a new view for State Objects"""
from os import name
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.state import State
from models import storage
import json

@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def get_states():
    """gets all state objects"""
    if request.method == 'GET':
        all_objects = storage.all(State)
        single_object = []
        for key, value in all_objects.items():
            single_object.append(value.to_dict)
        return jsonify(single_object)

@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_state_id(state_id):
    """gets the state object using his id"""
    if request.method == 'GET':
        all_objects = storage.all(State)
        new_dict = {}
        for key, value in all_objects.items():
            if state_id == value.id:
                new_dict = value.to_dict
                return jsonify(new_dict)
        abort(404)
