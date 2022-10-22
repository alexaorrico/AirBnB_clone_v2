#!/usr/bin/python3
""" index module """


from api.v1.views import state_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@state_views.route('states', strict_slashes=False)
def get_states():
    """ returns a list of all the states in db """
    states = storage.all(State)
    lst = [state.to_dict() for state in states.values()]
    return jsonify(lst)


@state_views.route('states/<state_id>', strict_slashes=False)
def get_state_with_id_eq_state_id(state_id):
    """ returns a state with id == state_id """
    state = storage.get(State, state_id)
    return jsonify(state.to_dict()) if state else abort(404)


@state_views.route('states/<state_id>', strict_slashes=False,
                   methods=["DELETE"])
def delete_state_with_id_eq_state_id(state_id):
    """ deletes a state with id == state_id """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@state_views.route('states', strict_slashes=False,
                   methods=["POST"])
def create_state():
    """ creates a new state """
    try:
        data = request.get_json()
    except Exception:
        return jsonify({
            "error": "Not a JSON"
            }), 400
    name = data.get("name")
    if not name:
        return jsonify({
            "error": "Missing name"
            }), 400
    state = State(name=name)
    state.save()
    return jsonify(
        state.to_dict()
        ), 201


@state_views.route('states/<state_id>', strict_slashes=False,
                   methods=["PUT"])
def update_state_with_id_eq_state_id(state_id):
    """ updates a state's record """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        return jsonify({
            "error": "Not a JSON"
            }), 400

    state_dict = state.to_dict()
    dont_update = ["id", "created_at", "updated_at"]
    for skip in dont_update:
        data[skip] = state_dict[skip]
    state_dict.update(data)
    state.delete()
    storage.save()
    updated_state = State(**state_dict)
    updated_state.save()
    return jsonify(
            updated_state.to_dict()
            )
