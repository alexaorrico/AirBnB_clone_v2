#!/usr/bin/python3
""" Create a view for the State Objects """


from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route("/states", methods=["GET"])
def all_states():
    """ Retrieve all State objects """
    states = storage.all(State)
    state_list = [state.to_dict() for state in states.values()]
    return jsonify(state_list)


@app_views.route("/states/<state_id>", methods=["GET"])
def one_state(state_id):
    """ Retrieves a State Object """
    states = storage.all(State)
    state_list = [state.to_dict() for state in states.values()]
    one_state = [state for state in state_list if state["id"] == state_id]
    if len(one_state) == 0:
        abort(404)
    return jsonify(one_state[0])


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """ Retrieves a State Object """
    one_state = storage.get(State, state_id)
    if not one_state:
        abort(404)
    storage.delete(one_state)
    storage.save()
    return {}, 200


@app_views.route("/states", methods=["POST"])
def create_state():
    """ Create a new State object """
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    new_state = State(name=data["name"])

    storage.new(new_state)
    storage.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """ Update a State object """
    one_state = storage.get(State, state_id)

    if not one_state:
        return jsonify({"error": "Not found"}), 404

    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(one_state, key, value)

    storage.save()
    return jsonify(one_state.to_dict()), 200
