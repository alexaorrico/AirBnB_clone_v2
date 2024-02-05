#!/usr/bin/python3
"""RESTful API view to handle actions for 'State' objects"""

from flask import abort, request, jsonify

from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET", "POST"], strict_slashes=False)
def states_routes():
    """
    GET: Retrieves the list of all State objects
    POST: Creates a State object
    """
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
    """
    GET: Retrieves the State where id == state_id
    PUT: Updates the State that has id == state_id
    PUT: Deletes the State that has id == state_id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == "GET":
        return jsonify(state.to_dict())

    elif request.method == "PUT":
        in_data = request.get_json(silent=True)
        if in_data is None or not isinstance(in_data, dict):
            return 'Not a JSON\n', 400

        for key, val in in_data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(state, key, val)
        state.save()
        return state.to_dict(), 200

    elif request.method == "DELETE":
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
