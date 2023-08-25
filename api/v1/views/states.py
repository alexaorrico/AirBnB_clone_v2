#!/usr/bin/python3
"""
Module State
"""
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, abort, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """
    Retrives list of all State objects
    """
    states = []
    for state in storage.all("State").values():
        states.append(state.do_dict())
    return jsonify(states)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states(state_id):
    """
    All objects of State
    """
    # get data at given state_id
    state = storage.get(State, state_id)
    # raises 404 error if the state_id is not linked to a state
    if state is None:
        abort(404)

    result = state.to_dict()
    return jsonify(result)


@app_views.route('/states/<path:state_id>', methods=['DELETE'], strict_slashes=False)
def delete(state_id):
    """
    Deletes a State object
    """
    # get data
    delete_state = storage.get(State, state_id)
    # raises 404 error if the state_id is not linked to a state
    if delete_state is None:
        abort(404)
    else:
        # deletes and saves at given state_id
        storage.delete(delete_state)
        storage.save()
        # returns a empty dict with status 200
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """
    Post a new State
    """
    # parses incoming json file
    posted = request.get_json()
    # returns error message and status 400 if not a json file
    if posted is None:
        return jsonify({'error': 'Not a JSON'}), 400
    # returns error message and status 400 if no key 'name'
    if 'name' not in posted:
        return jsonify({'error': 'Mising name'}), 400
    # gets, saves and returns the new state with code 201
    new_state = State(**posted)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state_id(state_id):
    """
    Updates a State objects
    """
    # parses incoming json file
    body = request.get_json()
    # returns error and status 400 if not a json file
    if body is None:
        return jsonify({'error': 'Not a JSON'}), 400
    # gets the state linked to state_id
    state = storage.get(State, state_id)
    # if state_id not linked to a state status error 404
    if state is None:
        abort(404)
    else:
        # sets ignored keys
        ignore = ['id', 'created_at', 'updated_at']
        # updates the state with all key-value pairs of dict
        for key, value in body.items():
            if key not in ignore:
                setattr(state, key, value)
            else:
                pass
        # saves and returns object with status 200
        state.save()
        return jsonify(state.to_dict()), 200
