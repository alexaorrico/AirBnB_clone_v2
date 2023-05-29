#!/usr/bin/python3
"""a new view for State objects that handles all default RESTFul API actions"""
from flask import jsonify, make_response, request, abort
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """retrieves the list of all state objects"""
    all_states = storage.all(State).values()
    states_list = []
    for state in all_states:
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """retrieves state information for specified state by state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """deletes a state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    storage.delete(State)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<string:state_id>', methods=['POST'],
                 strict_slashes=False)
def create_state():
    """creates a new state"""
    res = request.get_json()
    if not res:
        abort(404, 'Not a JSON')

    if 'name' not in res:
        abort(400, 'Missing a name')

    new_state = State(**res)
    new_state.save()
    return make_response(jsonify(new_state.to_dict(), 201))


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
