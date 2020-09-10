#!/usr/bin/python3
""" States handler of app """
from api.v1.views import app_views
from flask import jsonify, abort, Response, request
from json import dumps
from models import storage
from models.state import State


@app_views.route("/states/", methods=["GET"], strict_slashes=False)
def app_route_state():
    """ GET all states """
    converted_states = []
    all_states = storage.all()
    for values in all_states.values():
        converted_states.append(values.to_dict())

    return jsonify(converted_states)


@app_views.route("/states/<states_id>", methods=["GET"], strict_slashes=False)
def app_route_state2(states_id):
    """ GET state from ID """
    search = storage.get("State", states_id)
    if search:
        return jsonify(search.to_dict())
    return abort(404)


@app_views.route("/states/<states_id>", methods=["DELETE"])
def app_route_state3(states_id):
    """ DELETE state from ID """
    search = storage.get("State", states_id)
    if search:
        storage.delete(search)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def app_route_state4():
    """ POST new user """
    data = request.get_json()
    if 'name' not in data:
        return abort(400, "Missing name")
    if data is None:
        return abort(400, "Not a JSON")
    state = State(**data)
    state_dict = state.to_dict()
    state.save()
    return jsonify(state_dict), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def app_route_state5(state_id):
    """ PUT update an state """
    state = storage.get("State", state_id)

    if state is None:
        return abort(404)

    data = request.get_json()

    if data is None:
        return abort(400, "Not a JSON")

    res = state.to_dict().update(**data)

    state = State(**res)
    storage.save()

    return jsonify(res), 200
