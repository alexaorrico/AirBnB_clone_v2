#!/usr/bin/python3
""" This module contains a blue print for a web app """

from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.state import State

# print("debugging............................")
@app_views.route('/states', methods=['GET'])
def all_states_obj():
    """ return the all state objects """
    # print("debugging............................")
    state_objects = storage.all(State)
    object_list = []
    for obj in state_objects.values():
        object_list.append(obj.to_dict())
    return jsonify(object_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state_obj(state_id):
    """ get the state object with the respective id """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state_obj(state_id):
    """ delete the state object with the respective id """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state_obj():
    """ create a state object """
    print(request.get_json())
    try:
        state_dict = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")
    if "name" not in state_dict:
        abort(400, description="Missing name")
    new_state = State(**state_dict)
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state_obj(state_id):
    """ update the state with the respective id """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    try:
        state_dict = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")
    for key, value in state_dict.items():
        if key != "id" or key != "created_at" or key != "updated_at":
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
