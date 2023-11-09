#!/usr/bin/python3
"""this view hundles states endpoints"""
from api.v1.views import app_views
from flask import jsonify
from flask import request
from flask import abort
from flask import make_response
from models.state import State
from models import storage


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def all_states():
    """gets all states instances"""
    d_states = storage.all(State)
    states = []
    for state in d_states.values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route("/states/<states_id>", methods=["GET"], strict_slashes=False)
def get_state(states_id):
    """gets state with the given id"""
    if states_id:
        d_state = storage.get(State, states_id)
        if d_state is None:
            abort(404)
        else:
            return jsonify(d_state.to_dict())


@app_views.route("/states/<states_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(states_id):
    """deletes state with the given id"""
    if states_id:
        d_state = storage.get(State, states_id)
        if d_state is None:
            abort(404)
        else:
            storage.delete(d_state)
            storage.save()
            return make_response(jsonify({}), 200)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """create new state with the supplied data"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    if "name" not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    new = State(**data)
    new.save()
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route("/states/<states_id>", methods=["PUT"], strict_slashes=False)
def update_state(states_id):
    """updates state with supplied id"""
    if states_id:
        d_state = storage.get(State, states_id)

        if d_state is None:
            abort(404)

        if request.get_json():
            data = request.get_json()
            for k, v in data.items():
                if k not in ["id", "created_at", "updated_at"]:
                    setattr(d_state, k, v)
            d_state.save()
            return make_response(jsonify(d_state.to_dict()), 200)
        return make_response(jsonify({"error": "Not a JSON"}), 400)
