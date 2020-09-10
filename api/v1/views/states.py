#!/usr/bin/python3
""" Restful API for State objects. """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """ Retrieves a list with all states. """
    state_objs = storage.all(State).values()
    list_dic_states = []
    for state in state_objs:
        list_dic_states.append(state.to_dict())
    return jsonify(list_dic_states)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def all_states_N():
    """ Retrieves a list with all state, including the new one. """
    body_dic = request.get_json()
    if not body_dic:
        return jsonify({'error': 'Not a JSON'}), 400
    if "name" not in body_dic:
        return jsonify({'error': 'Missing name'}), 400
    new_state = State(**body_dic)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update a current state"""
    state_obj = storage.get(State, state_id)
    if state_obj:
        body_dic = request.get_json()
        if not body_dic:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in body_dic.items():
            ignore_keys = ['id', 'created_at']
            if key not in ignore_keys:
                setattr(state_obj, key, value)
        state_obj.save()
        return jsonify(state_obj.to_dict()), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Delete current state """
    state_obj = storage.get(State, state_id)
    if state_obj:
        storage.delete(state_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Get current state """
    state_obj = storage.get(State, state_id)
    if state_obj:
        return jsonify(state_obj.to_dict())
    else:
        abort(404)
