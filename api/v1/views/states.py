#!/usr/bin/python3
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def get_states():
    """ Return status of the APP as OK """
    states_list = []
    for state in storage.all('State').values():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_states():
    """ Return status of the APP as OK """
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states_id(state_id):
    """ Return status of the APP as OK """
    for state in storage.all('State').values():
        if state.id == state_id:
            return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_states_id(state_id):
    """ Return status of the APP as OK """
    catch_state = storage.get('State', state_id)
    if catch_state is None:
        abort(404)
    else:
        storage.delete(catch_state)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_states_id(state_id):
    """ Return status of the APP as OK """
    catch_state = storage.get('State', state_id)
    if catch_state is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(catch_state, key, value)
    storage.save()
    return jsonify(catch_state.to_dict()), 200
