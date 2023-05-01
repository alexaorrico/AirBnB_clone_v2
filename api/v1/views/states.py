#!/usr/bin/python3
'''
Handles all default RESTFul API actions for state objects
'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State

F = False


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states_obj():
    '''handles Get for all statea objects'''

    state_list = []
    objs = storage.all()
    for k, v in objs.items():
        if v.__class__.__name__ == "State":
            state_list.append(v.to_dict())
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=F)
def get_state_obj(state_id):
    '''handles Get for a state object'''

    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)

    state_dict = state_obj.to_dict()
    return jsonify(state_dict)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=F)
def delete_state_obj(state_id):
    '''deletes a state object'''

    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)

    storage.delete(state_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state_obj():
    '''creates states objects'''

    json_data = request.get_json()
    if json_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif 'name' not in json_data.keys():
        return jsonify({"error": "Missing name"}), 400

    new_obj = State()
    for attr, val in json_data.items():
        setattr(new_obj, attr, val)
    # new_obj = State(**json_data)
    new_obj.save()

    return jsonify(new_obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=F)
def update_state_obj(state_id):
    '''updates a state object'''

    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)

    json_data = request.get_json()
    if json_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for attr, val in json_data.items():
        setattr(state_obj, attr, val)
    state_obj.save()

    return jsonify(state_obj.to_dict()), 200
