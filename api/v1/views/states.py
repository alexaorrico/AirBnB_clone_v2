#!/usr/bin/python3
""" API view for State objects. """
from api.v1.views import app_views
from flask import jsonify, request, abort
import json
from models import storage
from models.state import State
import os


@app_views.route("/states", methods=['GET'])
def all_states():
    """Returns all states"""
    states = storage.all(State)
    statelist = []
    for state in states.values():
        statelist.append(state.to_dict())
    return jsonify(statelist)


@app_views.route("/states/<state_id>", methods=['GET'])
def get_state(state_id=None):
    """Returns a list of one State"""
    if request.method == 'GET':
        if state_id is not None:
            obj = storage.get(State, state_id)
            if obj is not None:
                return obj.to_dict()
            else:
                return abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'])
def state_delete(state_id):
    """Deletes a State"""
    if state_id:
        obj = storage.get(State, state_id)
        if obj is not None:
            storage.delete(obj)
            storage.save()
            return {}
        else:
            return abort(404)


@app_views.route("/states", methods=['POST'])
def state_create():
    """Creates state"""
    if request.method == 'POST':
        if not request.json:
            abort(400, "Not a JSON")
        if 'name' not in request.json:
            abort(400, "Missing name")
        state_dict = request.get_json()
        state = State(**state_dict)
        state.save()
        return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """ Updates an existing State obj. """
    try:
        state = storage.all(State)["State.{}".format(state_id)]
    except (TypeError, KeyError):
        abort(404)
    if not state:
        abort(404)
    content = request.get_json()
    try:
        json.dumps(content)
    except (TypeError, OverflowError):
        abort(400, {'message': 'Not a JSON'})
    ignored_keys = ['id', 'created_at', 'updated_at']
    for key, value in content.items():
        if key not in ignored_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
