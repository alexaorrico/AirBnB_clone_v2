#!/usr/bin/python3
"""RESTful API view to handle actions for 'State' objects"""

from flask import abort, request, jsonify

from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET", "POST"], strict_slashes=False)
def states_routes():
    """Retrieves the list of all State objects"""
    if request.method == "GET":
        states = [state.to_dict() for state in storage.all(State).values()]
        return jsonify(states)

    if request.method == "POST":
        in_data = request.get_json(silent=True)
        if in_data is None or not isinstance(in_data, dict):
            return 'Not a JSON\n', 400

        name = in_data.get("name")
        if name is None:
            return "Missing name\n", 400

        state = State(**in_data)
        state.save()
        return state.to_dict(), 201


@app_views.route("/states/<state_id>", methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def state_id_routes(state_id):
    """Retrieves the list of all State objects"""
    if request.method == "GET":
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        return jsonify(state.to_dict())

    elif request.method == "PUT":
        state = storage.get(State, state_id)
        if state is None:
            abort(404)

        in_data = request.get_json(silent=True)
        if in_data is None or not isinstance(in_data, dict):
            return 'Not a JSON\n', 400

        in_data = {key: val for key, val in in_data.items()
                   if key not in ["id", "created_at", "updated_at"]}
        state.__init__(**in_data)
        state.save()
        return state.to_dict(), 200

    elif request.method == "DELETE":
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
