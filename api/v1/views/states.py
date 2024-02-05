#!/usr/bin/python3
"""This module contains the view for the state resource."""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route("/states", methods=['GET', 'POST'], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False,)
def states(state_id=None):
    if request.method == 'GET':
        if state_id is None:
            return jsonify(
                [state.to_dict() for state in storage.all(State).values()]
            )
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        return jsonify(state.to_dict())
    elif request.method == 'POST':
        if not request.is_json:
            return jsonify({'error': 'Not a JSON'}), 400
        body = request.get_json(force=True)
        if body.get('name', None) is None:
            return jsonify({'error': 'Missing name'}), 400
        new_state = State(**body)
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201
    elif request.method == 'PUT':
        state = storage.get(State, state_id)
        if state is None:
            return abort(404)
        if not request.is_json:
            return jsonify({'error': 'Not a JSON'}), 400
        body = request.get_json(force=True)
        for name, value in {
            k: v
            for k, v in body.items()
            if k not in ['id', 'created_at', 'updated_at']
        }.items():
            setattr(state, name, value)
        state.save()
        return jsonify(state.to_dict()), 200
    elif request.method == 'DELETE':
        state = storage.get(State, state_id)
        if state is None:
            return abort(404, jsonify({}))
        state.delete()
        storage.save()
        return jsonify({}), 200
    abort(405)
