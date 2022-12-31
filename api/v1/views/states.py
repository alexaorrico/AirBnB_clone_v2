#!/usr/bin/python3
''' states.py'''

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    '''Retrieves the list of all State objects'''
    objects = storage.all("State")
    list_states = []
    for k, state_obj in objects.items():
        list_states.append(state_obj.to_dict())
    return jsonify(list_states)


@app_views.route("/states/<id>", methods=["GET"], strict_slashes=False)
def get_state_id(id):
    '''Retrieves a State object'''
    state_obj = storage.get("State", id)
    if state_obj:
        return jsonify(state_obj.to_dict())
    abort(404)


@app_views.route("/states/<id>", methods=["DELETE"], strict_slashes=False)
def delete_state_id(id):
    '''Deletes a State object'''
    state_obj = storage.get("State", id)
    if state_obj:
        storage.delete(state_obj)
        storage.save()
        return jsonify({}), 200

    abort(400)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    '''Creates a State'''
    if request.headers.get('Content-Type') != "application/json":
        abort(400, description="Not a JSON")

    state_json = request.get_json()

    if not state_json.get("name"):
        abort(400, description="Missing name")

    state_obj = State(**state_json)
    storage.new(state_obj)
    storage.save()

    return jsonify(state_obj.to_dict()), 200


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    '''Updates a State object'''
    state_obj = storage.get("State", state_id)
    if not state_obj:
        abort(404)

    if request.headers.get('Content-Type') != "application/json":
        abort(400, description="Not a JSON")

    state_json = request.get_json()
    for attr, attr_value in state_json.items():
        if attr not in ["id", "created_at", "updated_at"]:
            setattr(state_obj, attr, attr_value)

    storage.save()

    return jsonify(state_obj.to_dict()), 200
