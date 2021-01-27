#!/usr/bin/python3
"""State Template"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def show(state_id=None):
    """return All states objects or an specific state object by id"""
    if not state_id:
        all_states = storage.all(State).values()
        list_states = []
        for state in all_states:
            list_states.append(state.to_dict())
        return jsonify(list_states)
    else:
        state = storage.get(State, state_id)
        if not state:
            abort(404)

        return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/states/", methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State"""
    if not request.is_json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    kwargs = request.get_json()
    state = State(**kwargs)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201
