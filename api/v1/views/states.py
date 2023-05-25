#!/usr/bin/python3
""" Configures RESTful api for the states route """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET", "POST"], strict_slashes=False)
def states():
    """ configures the state route """

    if request.method == "GET":
        states = storage.all(State)
        states_dict = [state.to_dict() for state in states.values()]

        return jsonify(states_dict)
    else:
        try:
            json_dict = request.get_json()
        except Exception:
            abort(400, "Not a JSON")

        try:
            name = json_dict["name"]
        except KeyError:
            abort(400, "Missing name")

        new_state = State()
        new_state.name = name

        storage.new(new_state)
        storage.save()

        return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["GET", "DELETE", "PUT"]
                 strict_slashes=False)
def states_id(state_id):
    """ configures the states/<state_id> route """

    state = storage.get("State", state_id)

    if not state:
        abort(404)

    if request.method == "GET":
        return jsonify(state.to_dict())
    elif request.method == "DELETE":
        storage.delete(state)
        storage.save()

        return jsonify({}), 200
    else:
        try:
            json_dict = request.get_json()
        except Exception:
            abort(400, "Not a JSON")

        keys_to_ignore = ["id", "created_at", "updated_at"]
        for key, val in json_dict.items():
            if key not in keys_to_ignore:
                setattr(state, key, val)

        storage.new(state)
        storage.save()

        return jsonify(state.to_dict()), 200
