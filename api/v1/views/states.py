#!/usr/bin/python3
""" state module api v1 """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states(state_id=None):
    """
        All states or one state of method GET and returns
        all state objects
    """

    if state_id is None:
        states = storage.all(State).values()
        return jsonify([state.to_dict() for state in states]), 200

    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id=None):
    """
        Deletes a state with id and returns an empty JSON
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    """
        Stores and returns a new state
    """
    reqst = request.get_json(silent=True)
    if reqst is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in reqst:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = State(**reqst)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id=None):
    """
        Return the information of a given state
    """
    keys = ['id', 'created_at', 'updated_at']
    reqst = request.get_json(silent=True)

    if not reqst:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    for key, val in reqst.items():
        if key not in keys:
            setattr(state, key, val)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
