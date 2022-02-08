#!/usr/bin/python3
"""
Create a new view for State objects
that handles all default RESTFul API actions
"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route("/states",
                 methods=["GET"],
                 strict_slashes=False)
def get_state():
    """ list all state"""
    get_states = storage.all("State").values()
    list_states = []
    for state in get_states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route("/states/<state_id>",
                 methods=["GET"],
                 strict_slashes=False)
def id_state(state_id):
    """ return id of state"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route("/states/<state_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """ delete state"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states",
                 methods=["POST"],
                 strict_slashes=False)
def post_state():
    """ creat state"""
    data = request.get_json()
    if type(data) is not dict:
        return "Not a JSON", 400
    if "name" not in data:
        return"Missing name", 400

    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>",
                 methods=["PUT"],
                 strict_slashes=False)
def put_state(state_id):
    """update state"""
    up_date = storage.get(State, state_id)
    if up_date:
        data = request.get_json()
        if type(data) is dict:
            ignore = ["id", "created_at", "updated_at"]
            for k, v in data.items():
                if k not in ignore:
                    setattr(up_date, k, v)
            storage.save()
            return jsonify(up_date.to_dict()), 200
        else:
            return"Not a JSON", 400
    else:
        abort(404)
