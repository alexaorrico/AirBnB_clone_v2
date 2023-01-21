#!/usr/bin/python3
""" state view """
from api.v1.views import app_views
from flask import jsonify, Blueprint, make_response, abort, request
from models import storage
from models.state import State
from models.base_model import BaseModel


@app_views.route('/states', methods=["GET", "POST"], strict_slashes=False)
def get_states():
    """get all instances of the state object"""
    if request == "GET":
        response = []
        states = storage.all(State).values()
        for state in states:
            response.append(state.to_dict())
        return (jsonify(response))

    if request == "POST":
        """post a new instance"""
        new_data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'name' not in request.json:
            abort(400, description="Missing name")
        state = State(**new_data)
        state.save()
        return (jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_is>', methods=["GET", "PUT", "DELETE"],
        strict_slashes=False)
def get_state_by_id(state_id):
    """get, update an delete state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == "GET":
        response = state.to_dict()
        return (jsonify(response))
    if request.method == "PUT":
        new_data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        for key, value in new_data.items():
            setattr(state, key, value)
        state.save()
        return (jsonify(state.to_dict()), 200)
    if request.method == "DELETE":
        storage.delete(state)
        storage.save()
        response = make_response(jsonify({}), 200)
        return response
