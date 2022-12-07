#!/usr/bin/python3
"""
    State
"""


from api.v1.views import app_views
from flask import request
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'])
def index():
    states = storage.all(State)
    states_dict = []
    for state in states:
        states_dict.append(states[state].to_dict())
    return states_dict


@app_views.route("/states/<id>", methods=['GET'])
def get(id):
    if storage.get(State, id) is None:
        return {"error": "Not found"}, 404

    return storage.get(State, id).to_dict()


@app_views.route("/states/<id>", methods=['DELETE'])
def delete(id):
    if storage.get(State, id) is None:
        return {"error": "Not found"}, 404

    storage.get(State, id).delete()
    storage.save()
    return {}, 200


@app_views.route("/states", methods=['POST'])
def store():
    if not request.is_json:
        return {"error": "Not a Json"}, 400

    new_state = request.get_json()

    if "name" not in new_state:
        return {"error": "Missing name"}, 400

    new_state = State(**new_state)
    new_state.save()
    return new_state.to_dict(), 201


@app_views.route("/states/<id>", methods=['PUT'])
def update(id):
    state = storage.get(State, id)
    data = request.get_json()

    if state is None:
        return {"error": "Not found"}, 404

    if not request.is_json:
        return {"error": "Not a Json"}, 400

    for key in data:
        if key == 'id':
            continue
        if key == 'created_at':
            continue
        if key == 'updated_at':
            continue
        if key in State.__dict__:
            setattr(state, key, data[key])

    state.save()
    return state.to_dict(), 202
