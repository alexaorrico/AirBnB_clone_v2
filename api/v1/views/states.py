#!/usr/bin/python3
"""
A new view for State objects that handles all default RESTFul API actions
"""
from flask import abort
from flask import jsonify
from flask import request

from . import State
from . import storage
from . import app_views

# f are class properties to validate the request payload
f = ("name",)


@app_views.route("/states", methods=["GET", "POST"], strict_slashes=False)
def all_states():
    """
    Retrieves the list of all State objects
    """
    if request.method == "GET":
        return jsonify([s.to_dict() for s in storage.all(State).values()])
    else:
        body = request.get_json(silent=True)
        if request.is_json and body is not None:
            pay = {k: str(v) for k, v in body.items() if k in f}
            if not pay.get("name", None):
                abort(400, description="Missing name")
            new_state = State(**pay)
            storage.new(new_state), storage.save()
            return jsonify(new_state.to_dict()), 201
        abort(400, description="Not a JSON")


@app_views.route("/states/<state_id>",
                 methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def one_state(state_id):
    """
    Retrieves a State object
    """
    state = storage.get(State, str(state_id))
    if not state:
        abort(404, description="Not found")
    if request.method == "GET":
        return jsonify(state.to_dict())
    elif request.method == "DELETE":
        storage.delete(state), storage.save()
        return jsonify({})
    else:
        body = request.get_json(silent=True)
        if request.is_json and body:
            [setattr(state, k, str(v)) for k, v in body.items() if k in f]
            state.save()
            return jsonify(state.to_dict()), 200
        abort(400, description="Not a JSON")
