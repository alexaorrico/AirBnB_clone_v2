#!/usr/bin/python3
"""Create a new view for State objects"""

from flask import jsonify, request, abort
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states_list():
    """Retrieves the list of all State objects"""
    if request.method == 'GET':
        all_states = []
        for key in storage.all("State").values():
            all_states.append(key.to_dict())
        return jsonify(all_states)
    if request.method == 'POST':
        response = request.get_json()
        if not response:
            abort(400, "Not a JSON")
        if "name" not in response:
            abort(400, "Missing name")
        new_state = State(**response)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def states_id(state_id):
    """Deletes a State object:"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())
    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        for key, value in data.items():
            if key != "id" and key != "created_at" and key != "updated_at"\
             and hasattr(state, key):
                setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict()), 200
