#!/usr/bin/python3
"""handles api reqeust to states"""
from flask import jsonify, abort, make_response, request
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get_states():
    """method to get all states"""
    states = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(states)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    for state in storage.all(State).values():
        if state.id == state_id:
            return jsonify(state.to_dict())
    abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ deletes a state by id if it exist else raise 404"""
    state_to_delete = None
    for state in storage.all(State).values():
        if state.id == state_id:
            state_to_delete = state

    if state_to_delete:
        state_to_delete.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def create_state():
    """method to create a new state"""
    request_data = request.get_json(silent=True)
    if request_data is None:
        abort(400, "Not a JSON")
    if 'name' not in request_data:
        abort(400, "Missing name")

    # create a new state object
    state = State(**request_data)

    # save new state to database
    state.save()

    return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """method to update state by id"""
    # prevent reqeust.get_json from raising exception if
    # its unable to convert request body to json and rather
    # return None
    request_data = request.get_json(silent=True)

    if request_data is None:
        abort(400, "Not a JSON")
    # search for the state to update based on id
    for state in storage.all(State).values():
        if state.id == state_id:
            for attrib, value in request_data.items():
                if attrib in ["id", "created_at", "updated_at"]:
                    continue
                setattr(state, attrib, value)
            state.save()
            return make_response(jsonify(state.to_dict()), 200)
    abort(404)
