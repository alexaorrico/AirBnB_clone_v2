#!/usr/bin/python3
"""
    this module contains flask app routes
        flask APP routes:
        methods:
            GET:
                /states:
                    list all states
                /states/<state_id>:
                    display state dictionary using ID
            DELETE:
                /states/<state_id>:
                    delete a state using ID
            POST:
                /states:
                    creates a new state
            PUT:
                /states/<state_id>:
                    update state object using ID
"""

from api.v1.views import app_views
from flask import abort, jsonify, request

# import State and Storage models
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"])
def get_states():
    """display all states"""
    state_list = []
    [state_list.append(state.to_dict())
     for state in storage.all(State).values()]
    return jsonify(state_list)


@app_views.route("/states/<state_id>", methods=["GET"])
def get_state(state_id):
    """diplay a state using ID"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    return obj.to_dict()


@app_views.route("/states/<state_id>", methods=["DELETE"])
def remove_state(state_id):
    """delete a state instance using ID"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"])
def create_state():
    """creates a new state instance"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    obj = State(**(request.get_json()))
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """update a state instance using ID"""
    ignore_keys = ["id", "created_at", "updated_at"]
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    [setattr(obj, key, value) for key, value in request.get_json().items()
     if key not in ignore_keys]
    obj.save()
    return jsonify(obj.to_dict()), 200
