#!/usr/bin/python3
""" Create a Index """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False)
def get_states():
    """ return all state objects"""
    states = storage.all(State).values()
    resultado = []

    for state in states:
        resultado.append(state.to_dict())

    return jsonify(resultado)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_states_id(state_id=None):
    """ get state for id """
    states = storage.all("State").values()
    resultado = []
    if state_id is not None:
        for state in states:
            if state_id == state.id:
                return jsonify(state.to_dict())
        return abort(404)

    return jsonify(resultado)


@app_views.route("/states/<state_id>",
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_state(state_id=None):
    """ Deletes state by id """
    try:
        state = storage.get(State, state_id)

        if state is not None:
            storage.delete(state)
            storage.save()
            return jsonify({}), 200

        abort(404)
    except:
        abort(404)


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def create_state():
    """ Creates new state """
    try:
        state = request.get_json()

        if state.get("name") is None:
            return jsonify({"error": "Missing name"}), 400
    except:
        return jsonify({"error": "Not a JSON"}), 400

    state = State(**state)
    storage.save()

    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def update_states(state_id=None):
    """ Updates state """
    try:
        json = request.get_json()

        if isinstance(json, dict) is False:
            raise Exception(400)
    except:
        return jsonify({"error": "Not a JSON"}), 400

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    att_skip = ["id", "created_at", "updated_at"]
    for key, value in json.items():
        if key not in att_skip:
            setattr(state, key, value)

    state.save()

    return jsonify(state.to_dict()), 200
