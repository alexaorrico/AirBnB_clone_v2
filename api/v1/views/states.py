#!/usr/bin/python3
""" States handler of app """
from api.v1.views import app_views
from flask import jsonify, abort, Response, request, make_response
from json import dumps, loads
from models import storage
from models.state import State


@app_views.route("/states/", methods=["GET"], strict_slashes=False)
def app_route_state():
    """ GET all states """
    converted_states = []
    all_states = storage.all()
    for values in all_states.values():
        if values.to_dict()["__class__"] == "State":
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
    if data is None:
        return abort(400, "Not a JSON")
    if 'name' not in data:
        return abort(400, "Missing name")
    state = State(**data)
    state_dict = state.to_dict()
    state.save()
    return jsonify(state_dict), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def app_route_state5(state_id):
    """ PUT update an state """
    if state_id:
            obj_states = storage.get(State, state_id)
            if obj_states is None:
                abort(404)

            if not request.get_json():
                return make_response(jsonify({"error": "Not a JSON"}), 400)
            req = request.get_json()
            for key, value in req.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(obj_states, key, value)
            obj_states.save()
            return make_response(jsonify(obj_states.to_dict()), 200)
