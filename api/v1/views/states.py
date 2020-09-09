#!/usr/bin/python3
"""
Module for State objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', defaults={'state_id': None}, methods=['GET'])
@app_views.route('/states/<state_id>', methods=['GET'])
def get_states(state_id):
    """ Retrieves the list of all State objects """
    if state_id is None:
        states_list = []
        for value in storage.all(State).values():
            states_list.append(value.to_dict())
        return jsonify(states_list)
    else:
        try:
            state_dic = storage.get(State, state_id).to_dict()
            return jsonify(state_dic)
        except:
            abort(404)


@app_views.route('/states', methods=['POST'])
def create_state():
    """ Create a new State object """
    if not request.json:
        return make_response(jsonify({"message": "Not a JSON"}), 400)

    if not 'name' in request.json:
        return make_response(jsonify({"message": "Missing name"}), 400)

    data = request.get_json()
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """ Update a State object """
    if not request.json:
        return make_response(jsonify({"message": "Not a JSON"}), 400)
    try:
        state_obj = storage.get(State, state_id)
        data = request.get_json()

        for key, value in data.items():
            if key != 'id' or key != 'created_at' or key != 'updated_at':
                setattr(state_obj, key, value)

        storage.save()
        return jsonify(state_obj.to_dict()), 200
    except:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ Delete a State object """
    try:
        storage.delete(storage.get(State, state_id))
        storage.save()
        return jsonify({}), 200
    except:
        abort(404)
