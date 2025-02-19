#!/usr/bin/python3
""" Python script for State Routes & views"""
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, abort, request


@app_views.route("/states", methods=["GET", "POST"])
def get_state():
    """ Get methods for states routes"""
    # get method
    if request.method == "GET":
        states = []
        for state in storage.all("State").values():
            states.append(state.to_dict())
        return jsonify(states)

    # post method
    data = request.get_json(silent=True)
    if not data:
        return "Not a JSON", 400
    if "name" not in data:
        return "Missing name", 400

    # create new state
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["GET", "DELETE", "PUT"])
def get_state_id(state_id):
    """ Get methods for retriving states objects by id"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    # DELETE method
    if request.method == "DELETE":
        state.delete()
        storage.save()
        return jsonify({}), 200

    # GET method
    elif request.method == "GET":
        return jsonify(state.to_dict())

    # PUT method
    data = request.get_json(silent=True)
    if not data:
        return "Not a JSON", 400
    keys_ignored = {"id", "created_at", "updated_at"}
    [setattr(state, k, v) for k, v in data.items() if k not in keys_ignored]
    state.save()
    return jsonify(state.to_dict()), 200
