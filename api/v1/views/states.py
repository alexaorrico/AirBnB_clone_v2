#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from models import storage
from flask import jsonify, make_response, abort
from models.state import State
from api.v1.views import app_views


@app.route('/states', methods=['GET'])
def states_get():
    """Retrieves the list of all State"""
    if request.methods == 'GET':
        states_list = []
        all_states = storage.all(State)
        for key, value in all_states.items():
            states_list.append(value.to_dict())
        return jsonify(states_list)

@app.route('/states', methods=['POST'])
def states_post():
    """Creates a State"""
    if request.methods == 'POST':
        transform_dict = request.get_json()
        if transform_dict is None:
            abort(400, "Not a JSON")
        if 'name' not in transform_dict.keys():
            abort(400, "Missing name")
        else:
            new_state = State(**transform_dict)
            new_state.save()
            return make_response(jsonify(new_state.to_dict()), 201)

@app.route('/states/<state_id>', methods=['GET'])
def state_id_get():
    """Retrieves a State object and 404 if it's an error"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        return (jsonify(obj.to_dict()))

@app.route('/states/<state_id>', methods=['DELETE'])
def state_id_delete():
    """Deletes a State object and 404 if it's an error"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)


@app.route('/states/<state_id>', methods=['PUT'])
def state_id_put():
    """Updates a State object"""
    ignore_list = ['id', 'created_at', 'updated_at']
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == 'PUT':
        transform_dict = request.get_json()
        if transform_dict is None:
            abort(400, "Not a JSON")
        for key, value in transform_dict.items():
            if key not in ignore_list:
                setattr(state, key, value)
            else:
                storage.save()
                return make_response(jsonify(state.to_dict()), 200)

