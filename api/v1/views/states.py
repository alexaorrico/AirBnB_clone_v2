#!/usr/bin/python3
"""Flask application that handle states API"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Return the state list"""
    states_all = storage.all("State")
    states_list = []
    for key, state in states_all.items():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE'],
                 strict_slashes=False)
def get_states_id(state_id):
    """Return a single state"""
    if request.method == 'GET':
        states_all = storage.all("State")
        try:
            unique_state = states_all["{}.{}".format("State",
                                                     state_id)].to_dict()
        except KeyError:
            abort(404)
        return jsonify(unique_state)
    elif request.method == 'DELETE':
        obj_to_delete = storage.get("State", state_id)
        if obj_to_delete is None:
            abort(404)
        else:
            storage.delete(obj_to_delete)
            storage.save()
            return jsonify({}), 200


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_states():
    """Post states"""
    json_tmp = request.get_json()
    if not json_tmp:
        return jsonify("Not a JSON"), 400
    try:
        json_tmp['name']
    except (KeyError, TypeError):
        return jsonify("Missing name"), 400
    new_state = State(**json_tmp)
    new_state.save()
    return(jsonify(new_state.to_dict())), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_states(state_id):
    """Put method to update states"""
    states_all = storage.all("State")
    try:
        unique_state = states_all["{}.{}".format("State", state_id)]
        json_tmp = request.get_json()
        if not json_tmp:
            return jsonify("Not a JSON"), 400
        for key, value in json_tmp.items():
            if key == 'id' or key == 'updated_at' or key == 'created_at':
                pass
            setattr(unique_state, key, value)
        unique_state.save()
    except KeyError:
        abort(404)
    return jsonify(unique_state.to_dict()), 200
