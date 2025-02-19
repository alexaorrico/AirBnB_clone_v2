#!/usr/bin/python3
"""index.py to connect to API"""
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import Flask, Blueprint, jsonify, abort, request, make_response


@app_views.route("/states", methods=["GET"],strict_slashes=False)
def states_retrive():
    all_st = storage.all("State")
    states = []
    for state in all_st.values():
        states.append(state.to_dict())
    return jsonify(states)

@app_views.route("/states/<string:state_id>", methods=["GET"], strict_slashes=False)
def states_id(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state = state.to_dict()
    return jsonify(state)

@app_views.route("/states/<string:state_id>", methods=["DELETE"], strict_slashes=False)
def states_id_del(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})

@app_views.route("/states/", methods=["POST"], strict_slashes=False)
def states_id_post():
    if not request.get_json():
            return make_response(jsonify({"error":"Not a JSON 1"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error":"Missing name"}), 400)
    state = State(**request.get_json())
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)
    
@app_views.route("/states/<string:state_id>", methods=["PUT"], strict_slashes=False)
def states_id_put(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error":"Not a JSON"}), 400)
    for key, val in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, val)
    state.save()
    return make_response(jsonify(state.to_dict()))
