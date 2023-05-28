#!/usr/bin/python3
""" A  new view for State objects that handles
    all default RESTFul API actions """

from models.state import State
from models import storage
from flask import Flask, request, jsonify, abort, make_response
from api.v1.views import app_views

@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states():
    """Retrieves the list of all State objects"""
    if request.method == 'GET':
        return jsonify([state.to_dict() for state in
                        storage.all(State).values()])

    if request.method == 'POST':
        if not request.json:
            abort(400, "Not a JSON")
        elif not 'name' in request.json:
            abort(400, "Missing name")
        else:
            new_state = State(**request.get_json())
            new_state.save()
            return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def state_id(state_id):
    """Retrieves a State object using states_id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if request.method == 'GET':
        return make_response(jsonify(state.to_dict()), 200)

    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        for k, v in request.json.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(state, k, v)
        state.save()
        return make_response(jsonify(state.to_dict()), 200)
