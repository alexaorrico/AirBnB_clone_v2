#!/usr/bin/python3
"""Creating state objects to handle all default RESTFUL APIs"""
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from api.v1.views import app_views
from models.base_model import BaseModel


@app_views.route('/states', methods=["GET", "POST"],
                 strict_slashes=False)
def all_states():
    """Retrieving all states from the database"""
    if request.method == "GET":
        state_list = []
        states = storage.all(State).values()
        for state in states:
            state_list.append(state.to_dict())
        return (jsonify(state_list))

    if request.method == 'POST':
        data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'name' not in request.json:
            abort(400, description="Missing name")
        state = State(**data)
        state.save()
        return (jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=["GET", "PUT"],
                 strict_slashes=False)
def get_state_by_id(state_id):
    """Gets states by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if request.method == "GET":
        one_state = state.to_dict()
        return (jsonify(one_state))

    if request.method == "PUT":
        print("test\n")
        data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        for key, value in data.items():
            setattr(state, key, value)
        state.save()
        return (jsonify(state.to_dict()), 200)


@app_views.route('/states/<state_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_state_by_id(state_id):
    """Deletes states by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if request.method == "DELETE":
        storage.delete(State)
        storage.save()
        status = make_response(jsonify({}), 200)
        return status
