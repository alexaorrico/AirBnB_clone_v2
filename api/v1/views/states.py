#!/usr/bin/python3
"""index """

from models import storage
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.state import State


@app_views.route("/states", methods=['GET', 'POST'])
def states_without_id():
    """Create a new state or return all the states"""
    if request.method == 'GET':
        states_list = []
        states_dict = storage.all(State)
        for state in states_dict.values():
            states_list.append(state.to_dict())
        return jsonify(states_list)

    if request.method == 'POST':
        json = request.get_json(silent=True)
        if json is None:
            abort(400, "Not a JSON")
        if json.get('name') is None:
            abort(400, "Missing name")
        state = State(**json)
        state.save()
        return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['GET', 'PUT', 'DELETE'])
def states_with_id(state_id=None):
    """Perform READ UPDATE DELETE operations on a state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(state.to_dict())

    if request.method == 'DELETE':
        state.delete()
        del state
        return jsonify({})

    if request.method == 'PUT':
        json = request.get_json(silent=True)
        if json is None:
            abort(400, "Not a JSON")
        state.update(**json)
        return jsonify(state.to_dict())
