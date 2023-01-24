#!/usr/bin/python3
'''A new view for State objects that handles all default RESTFul API action'''
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def retrieve_states():
    '''Retrieves all state information'''
    states = []
    for state in storage.all(State).values():
        states.append(state.to_dict())
    return jsonify(states), 200


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_state(state_id=None):
    '''Retrieves a specific state information'''
    if state_id is None:
        abort(404)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id=None):
    '''Deletes state with respect to the state_id'''
    if state_id is None:
        abort(404)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete(state)
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_state():
    '''Defines the a new state'''
    if request.get_json:
        kwargs = request.get_json()
    else:
        return "Not a JSON", 400

    if kwargs:
        if 'name' not in kwargs.keys():
            return 'Missing name', 400

    try:
        state = State(**kwargs)
        state.save()
    except TypeError:
        return "Not a JSON", 400

    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id=None):
    '''Updates a state'''
    if request.get_json:
        kwargs = request.get_json()
    else:
        return "Not a JSON", 400

    if kwargs:
        if 'name' not in kwargs.keys():
            return 'Missing name', 400

    try:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)

        for k in ("id", "created_at", "updated_at"):
            kwargs.pop(k, None)
            for k, v in kwargs.items():
                setattr(state, k, v)
        state.save()

    except AttributeError:
        return "Not a JSON", 400

    return jsonify(state.to_dict()), 200
