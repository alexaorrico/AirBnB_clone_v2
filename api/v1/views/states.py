#!/usr/bin/python3
"""
a new view for State objects that handles
all default RestFul API actions
"""

from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False, methods=["GET", "POST"])
def states_base():
    """Retrieves the list of all State objects"""
    if request.method == "GET":
        out = []
        for state in storage.all("State").values():
            out.append(state.to_dict())
        return jsonify(out)
    if request.method == "POST":
        if not request.is_json:
            return "Not a JSON", 400
        out = State(**request.get_json())
        if "name" not in out.to_dict().keys():
            return "Missing name", 400
        out.save()
        return out.to_dict(), 201


@app_views.route("/states/<s_id>",
                 strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def states_id(s_id):
    """Retrieves a State object"""
    if request.method == "GET":
        state = storage.get(State, s_id)
        if state:
            return state.to_dict()
        abort(404)
    if request.method == "DELETE":
        state = storage.get(State, s_id)
        if state:
            state.delete()
            storage.save()
            return {}, 200
        abort(404)
    if request.method == "PUT":
        state = storage.get(State, s_id)
        if state:
            if not request.is_json:
                return "Not a JSON", 400
            for k, v in request.get_json().items():
                setattr(state, k, v)
            storage.save()
            return state.to_dict()
        abort(404)
