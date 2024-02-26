#!/usr/bin/python3
"""
States file
"""
from flask import jsonify, abort, request, make_response
import json
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """returns a json of all states"""
    states = storage.all(State).values()
    jsonlist = []
    for state in states:
        jsonlist.append(state.to_dict())
    resp = make_response(jsonify(jsonlist))
    resp.status_code = 200
    return resp


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Get state from id"""
    state: State = storage.get(State, id=state_id)
    if state:
        resp = make_response(jsonify(state.to_dict()))
        resp.status_code = 200
        return resp
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete state on DELETE with id"""
    state: State = storage.get(State, id=state_id)
    if state:
        storage.delete(state)
        storage.save()
        resp = make_response(jsonify({'status': 200}))
        resp.status_code = 200
        return resp
    resp = make_response(jsonify)
    resp.status = 404
    return resp


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create State from POST"""
    try:
        kwargs = request.get_json(force=True)
    except json.on_json_loading_failed:
        resp = make_response(jsonify({'error': 'Not a JSON'}))
        resp.status_code = 400
        return resp
    if not isinstance(kwargs, dict) or 'name' not in kwargs:
        resp = make_response(jsonify({'error': 'Missing Name'}))
        resp.status_code = 400
        return resp
    state = State(**kwargs)
    storage.new(state)
    storage.save()
    resp = make_response(jsonify(state.to_dict()))
    resp.status_code = 201

    return resp


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def updated_state(state_id):
    """"Update Sate From PUT """
    state: State = storage.get(State, state_id)
    if not state:
        abort(404)

    try:
        kwargs: dict = request.get_json(force=True)
        for key in kwargs.keys():
            if key in ('id', 'created_at', 'updated_at'):
                kwargs.pop(key)
    except json.on_json_loading_failed:
        resp = make_response(jsonify({'error': 'Not a JSON'}))
        resp.status_code = 400
        return resp
    if not isinstance(kwargs, dict):
        resp = make_response(jsonify({'error': 'Missing Name'}))
        resp.status_code = 400
        return resp
    state_dict = state.to_dict()
    state_dict.update(kwargs)
    state = State(**state_dict)
    storage.new(state)
    storage.save()
    resp = make_response(jsonify(state.to_dict()))
    resp.status_code = 201

    return resp
