#!/usr/bin/python3
"""
view for State objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET', 'POST'], strict_slashes=False)
def all_states():
    if request.method == 'GET':
        return jsonify([i.to_dict() for i in storage.all(State).values()])
    if request.method == 'POST':
        if request.get_json():
            body = request.get_json()
        else:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if "name" not in body:
            return make_request(jsonify({"error": "Missing name"}), 400)
        new_state = State(**body)
        new_state.save()
        if storage.get(State, new_state.id) is not None:
            return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['GET'])
def get_state(state_id):
    """Method to get a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'])
def delete_state(state_id):
    """delete a single state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({})


@app_views.route('/states/<string:state_id>', methods=['PUT'])
def update_state(state_id):
    """update properties of a single state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.get_json():
        body = request.get_json()
    else:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    _exceptions = ["id", "created_at", "updated_at"]
    for k, v in body.items():
        if k not in _exceptions:
            setattr(state, k, v)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
