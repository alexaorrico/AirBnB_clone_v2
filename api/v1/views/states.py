#!/usr/bin/python3
""" objects that handles all default RESTFul API actions"""
from flask import Flask
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states',methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieves all states stored:
    """
    states = []
    for key, value in storage.all('State').items():
        states.append(value.to_dict())

    return jsonify(states)

@app_views.route('/states/<string:state_id>',methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """
    Retrieves the state by id or raise 404 if no state
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<string:state_id>',methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Deletes the state by id or raise 404 if no state
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})

@app_views.route('/states/', methods=['POST'],
                 strict_slashes=False)
def new_state():
    """ create new instance """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    jsonStr = request.get_json()
    state = State(**jsonStr)
    state.save()
    return jsonify(state.to_dict()), 201

@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """ Update state attributes ignoring id, created_at and updated_at"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict())
