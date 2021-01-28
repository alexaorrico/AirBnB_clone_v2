#!/usr/bin/python3
""" Task 4 """
from flask import Flask, Blueprint, jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def all_State():
    """ Task 7 """
    ls = []
    for st in storage.all('State').values():
        ls.append(st.to_dict())
    return jsonify(ls)


@app_views.route('/states/<state_id>', strict_slashes=False)
def retrive_State(state_id):
    """ Task 7 """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_State(state_id):
    """ Task 7 """
    to_del = storage.get(State, state_id)
    if to_del:
        storage.delete(to_del)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_State(state_id=None):
    """ Task 7 """
    to_update = storage.get(State, state_id)
    req = request.get_json()

    if to_update is None:
        abort(404)

    if req is None:
        abort(400)

    for key, value in req.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(to_update, key, value)

    storage.save()
    return jsonify(to_update.to_dict())


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_state():
    """create a new state"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_state = State(**request.get_json())
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)