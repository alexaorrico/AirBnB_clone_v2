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


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def creates_state():
    req_json = request.get_json()
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    newState = State()
    for k, v in req_json.items():
        setattr(newState, k, v)
    storage.new(newState)
    storage.save()
    return make_response(jsonify(newState.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    obj = storage.get(State, state_id)
    if not obj:
        return make_response(jsonify({"error": "Not found"}), 404)
    json_obj = request.get_json()
    if not json_obj:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for k, v in json_obj.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(obj, k, v)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)
