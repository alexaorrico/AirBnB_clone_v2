#!/usr/bin/python3
''''''
from flask import jsonify, request, make_response, abort
from api.v1.views import app_views
from models import storage
from models.state import State

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    states_dict = storage.all(State)
    states_list = []
    for elem in states_dict.values():
        states_list.append(elem.to_dict())
    return jsonify(states_list)

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    if not request.get_json():
        abort(400, description='Not a JSON')
    if 'name' not in request.get_json():
        abort(400, description='Missing name')
    query = request.get_json()
    new = State(**query)
    new.save()
    return make_response(jsonify(new.to_dict()), 201)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    return make_response(jsonify({}), 200)

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    if not storage.get(State, state_id):
        abort(404)
    if request.content_type != 'application/json':
        abort(400, description='Not a JSON')
    state = storage.get(State, state_id)
    query = request.get_json()
    ignore_list = ['id', 'created_at', 'updated_at']
    for key, val in query.items():
        if key not in ignore_list:
            setattr(state, key, val)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
        
