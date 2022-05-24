#!/usr/bin/python3
""" State """
import json
from models import storage
from flask import jsonify, abort, request, make_response
from models.state import State
from api.v1.views import app_views


@app_views.route("/states", methods=['GET', 'POST'], strict_slashes=False)
def states():
    """ Retrieves the list of all State objects """
    if request.method == 'GET':
        list_states = []
        states = storage.all(State).values()
        for state in states:
            list_states.append(state.to_dict())
        return jsonify(list_states)

    if request.method == 'POST':
        response = request.get_json()
        if response is None:
            abort(400, "Not a JSON")
        if response.get("name") is None:
            abort(400, "Missing name")

        new = State(**response)
        new.save()
        return make_response(jsonify(new.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def states_id(state_id):
    """ Retrieves a State object """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if request.method == 'GET':
        return jsonify(state.to_dict())

    elif request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({})

    elif request.method == 'PUT':
        ignore = ["id", "created_at", "updated_at"]
        response = request.get_json()
        if response is None:
            abort(400, "Not a JSON")
        for key, value in response.items():
            if key not in ignore:
                setattr(state, key, value)
        storage.save()
        return make_response(jsonify(state.to_dict()), 200)
