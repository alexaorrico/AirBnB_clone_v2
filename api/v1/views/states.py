#!/usr/bin/python3
"""module is document"""
from api.v1.views import app_views
from flask import jsonify, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', method=['GET'])
def list_states():
    all_states = storage.all(State)
    all_states = list(v.to_dict() for v in all_states.values())
    return jsonify(all_states)


@app_views.route('/states/<state_id>', method=['GET'])
def state_obj(state_id):
    state_obj = storage.get('State', state_id)
    if state_ob is None:
        abort(404, 'Not found')
    return jsonify(state_obj.to_dict())


@app_views.route('/states/<state_id>', method=['DELETE'])
def delete_state_obj(state_id):
    state_ob = storage.get('State', state_id)
    if state_ob is None:
        abort(404, 'Not found')
    state_obj.delete()
    return jsonify({})


@app_views.route('/states', method=['POST'])
def creates_state():
    req_json = request.get_json()
    if req_json is None:
        abort(404, "Not a JSON")
    if req_json.get("name") is None:
        abort(404, "Missing name")
    inst = State(**req_json)
    inst.save()
    return make_response(jsonify(inst.to_dict(), 201))

@app_views.route('/states/<state_id>', method=['PUT'])
def update_state(state_id):
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(404, "Not a JSON")
    ignore = ["state_id", "created_at", "updated_at"]
    req_json = request.get_json()
    for k, v in req_json:
        if k not in ignore:
            setattr(state, k, v)
    storage.save()
    return make_response(jsonify(state.to_dict), 200)
