#!/usr/bin/python3

""" Module handling requests for State objects """

from models import storage
from models.state import State
from api.v1.views import app_views
from flask import request, jsonify, abort


@app_views.route('/states', strict_slashes=False,
                 methods=['GET', 'POST'])
def all_states():
    """ Handles GET and POST request for all states """
    if request.method == 'GET':
        state_objects = storage.all(State)
        states_list = []
        for key, val in state_objects.items():
            states_list.append(val.to_dict())
        return jsonify(states_list)

    if request.method == 'POST':
        data = request.get_json(silent=True)
        state = State()
        if data is None:
            return 'Not a JSON', 400
        if 'name' not in data.keys():
            return 'Missing name', 400
        ignored_keys = ['id', 'created_at', 'updated_at']
        for key in data:
            if key not in ignored_keys:
                setattr(state, key, data[key])
        state.save()
        return(state.to_dict()), 201
    abort(404)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def state_by_id(state_id):
    """ Handles GET, DELETE and PUT requests for state by id """
    if request.method == 'GET':
        state_objects = storage.all(State)
        for key, val in state_objects.items():
            if val.id == state_id:
                return val.to_dict()
        abort(404)

    if request.method == 'DELETE':
        state_objects = storage.all(State)
        for key, val in state_objects.items():
            if val.id == state_id:
                storage.delete(val)
                storage.save()
                return {}, 200
        abort(404)

    if request.method == 'PUT':
        valid_request = request.get_json(silent=True)
        if valid_request is None:
            return 'Not a JSON', 400

        ignored_keys = ['id', 'created_at', 'updated_at']
        state_objects = storage.all(State)
        for key, val in state_objects.items():
            if val.id == state_id:
                for key in valid_request:
                    if key not in ignored_keys:
                        setattr(val, key, valid_request[key])
                storage.save()
                return val.to_dict(), 200
        abort(404)
