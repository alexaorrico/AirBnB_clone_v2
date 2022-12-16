#!/usr/bin/python3
"""module is document"""
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def list_states():
    all_states = storage.all(State)
    all_states = list(v.to_dict() for v in all_states.values())
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'])
def state_obj(state_id):
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    return jsonify(state_obj.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state_obj(state_id):
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    storage.delete(state_obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'])
def creates_state():
    req_json = request.get_json()
    if req_json is None:
        abort(400, "Not a JSON")
    if "name" not in req_json:
        abort(400, "Missing name")
    newState = State()
    for k, v in req_json.items():
        setattr(newState, k, v)
    storage.new(newState)
    storage.save()
    return make_response(jsonify(newState.to_dict), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    ignore = ["state_id", "created_at", "updated_at"]
    req_json = request.get_json()
    for k, v in req_json:
        if k not in ignore:
            setattr(state, k, v)
    storage.save()
    return make_response(jsonify(state.to_dict)), 200
