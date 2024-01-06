#!/usr/bin/python3
"""
contains endpoints(routes) for states objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False)
def get_states():
    """
    Retrieves the list of all State objects:
    """
    objs = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(objs)


@app_views.route("/states/<string:state_id>", strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a State object
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<string:state_id>", strict_slashes=False,
                 methods=['DELETE'])
def del_state(state_id):
    """
    Deletes a State object
    """
    state = storage.get(State, state_id)
    if state:
        state.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("/states", strict_slashes=False, methods=['POST'])
def create_state():
    """
    Creates a State
    """
    valid_json = request.get_json()
    obj = State(**valid_json)

    if valid_json is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in valid_json:
        return make_response(jsonify({"error": "Missing name"}), 400)

    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route("/states/<string:state_id>", strict_slashes=False,
                 methods=['PUT'])
def update_state(state_id):
    """
    Updates a State object
    """
    state = storage.get(State, state_id)
    valid_json = request.get_json()

    if not state:
        abort(404)

    if valid_json is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in valid_json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
