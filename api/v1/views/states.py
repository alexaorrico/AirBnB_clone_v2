#!/usr/bin/python3

from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False, methods=["GET", "POST"])
def states_base():
    """x"""
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


@app_views.route("/states/<s_id>", strict_slashes=False, methods=["GET", "DELETE", "PUT"])
def states_id(s_id):
    """x"""
    if request.method == "GET":
        for state in storage.all("State").values():
            if state.id == s_id:
                return state.to_dict()
        abort(404)
    if request.method == "DELETE":
        for state in storage.all("State").values():
            if state.id == s_id:
                state.delete()
                storage.save()
                return {}, 200
        abort(404)
    if request.method == "PUT":
        for state in storage.all("State").values():
            if state.id == s_id:
                if not request.is_json:
                    return "Not a JSON", 400
                for k, v in request.get_json().items():
                    setattr(state, k, v)
                storage.save()
                return state.to_dict()
        abort(404)
