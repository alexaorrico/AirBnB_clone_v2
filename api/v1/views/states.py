#!/usr/bin/python3
""" handles states views """
from models import storage
from api.v1.views import app_views
from flask import make_response, jsonify, abort, request
from sqlalchemy import text
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ get list of all states in
    json format """
    all_states = []
    states_obj = storage.all('State')
    for st in states_obj.values():
        all_states.append(st.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<states_id>', methods=['GET'], strict_slashes=False)
def retrive_state(states_id):
    """ retrives a singl state
    using states id
    """
    state = storage.get("State", str(states_id))
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<states_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(states_id):
    """ Deletes a state
    given the id"""
    state = storage.get('State', str(states_id))
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ creates a new state """
    state = request.get_json()
    if state is None:
        abort(400, 'Not a JSON')
    if 'name' not in state:
        abort(400, 'Missing Name')
    new_state = State(**state)
    new_state.save()
    resp = new_state.to_dict()

    return make_response(jsonify(resp), 201)


@app_views.route('/states/<states_id>', methods=['PUT'], strict_slashes=False)
def update_state(states_id):
    """ updates states object """
    state = storage.get('State', str(states_id))
    if state is None:
        abort(404)
    update = request.get_json(silent=True)
    if update is None:
        abort(400, 'Not a JSON')
    for key, val in update.items():
        if key not in ['id', 'created_at', 'updated-at']:
            setattr(update, key, val)
    update.save()
    return jsonify(update.to_dict())
