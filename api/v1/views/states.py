from api.v1.views import app_views
from models.state import State
from models import storage
from flask import Flask, jsonify, abort, make_response, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    states = storage.all(State).values()
    states_list = [state.to_dict() for state in states]
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def id_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort (404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort (404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post():
    dict = request.get_json()
    if dict is None:
        abort (400, 'Not a JSON')
    if dict.get('name') is None:
        abort (400, 'Missing name')
    new_status = State(**dict)
    storage.save()
    return make_response(jsonify(new_status.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort (404)
    dict = request.get_json()
    if dict is None:
        abort (400, 'Not a JSON')
    keys_substract = ['id', 'created_at', 'updated_at']
    for key, val in dict.items():
        if key not in keys_substract:
            setattr(state, key, val)
    storage.save()
    return (jsonify(state.to_dict()), 200)
