#!/usr/bin/python3
"""
Create a new view for State objects that handles
all default RESTFul API action
"""
from api.v1.views import app_views
from flask import jsonify, Blueprint, make_response, abort, request
from models import storage
from models.state import State
from models.base_model import BaseModel


@app_views.route('/states', methods=["GET", "POST"], strict_slashes=False)
def get_all_states():
    """
    function retrieves all state objects
    """
    if request.method == 'GET':
        user_output = []
        states = storage.all(State).values()
        for state in states:
            user_output.append(state.to_dict())
        return (jsonify(user_output))
    if request.method == 'POST':
        user_data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'name' not in request.json:
            abort(400, description="Missing name")
        state = State(**user_data)
        state.save()
        return (jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=["GET", "PUT"],
                 strict_slashes=False)
def get_single_state(state_id):
    """
    retrieves one unique state object depending on its ID
    """
    defined_state = storage.get(State, state_id)
    if defined_state is None:
        abort(404)
    if request.method == "GET":
        user_output = defined_state.to_dict()
        return (jsonify(user_output))
    if request.method == "PUT":
        print("test\n")
        data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        for key, value in data.items():
            setattr(defined_state, key, value)
        defined_state.save()
        return (jsonify(defined_state.to_dict()), 200)


@app_views.route('/states/<state_id>', methods=["GET", "DELETE"],
                 strict_slashes=False)
def del_single_state(state_id):
    """
    delete one unique state object, with its ID as reference
    """
    defined_state = storage.get(State, state_id)
    if defined_state is None:
        abort(404)
    storage.delete(defined_state)
    storage.save()
    result = make_response(jsonify({}), 200)
    return result
