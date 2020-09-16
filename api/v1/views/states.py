#!/usr/bin/python3
""" Create a new view for State objects
that handles all default RestFul API actions """
from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, abort, request
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def getstate(state_id=None):
    """GET state """
    if state_id is None:
        all_states = []
        states_values = storage.all("State").values()
        for obj in states_values:
            all_states.append(obj.to_dict())
        return jsonify(all_states)
    elif storage.get(State, state_id):
        return jsonify(storage.get(State, state_id).to_dict())
    abort(404)


@app_views.route(
    '/states/<state_id>', methods=['DELETE'],
    strict_slashes=False)
def deletestate(state_id=None):
    """DELETE state"""
    if storage.get(State, state_id):
        storage.delete(storage.get(State, state_id))
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def poststate():
    """POST state """
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    elif "name" not in body.keys():
        abort(400, "Missing name")
    else:
        post_state = State(**body)
        storage.save()
        return jsonify(post_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def putstate(stateid=None):
    """PUT state """
    state = storage.get("State", stateid)
    if state is None:
        abort(404)
    new = request.get_json()
    if new is None:
        abort(400, "Not a JSON")
    for key, value in update.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
