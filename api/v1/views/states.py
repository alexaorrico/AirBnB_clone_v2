#!/usr/bin/python3
"""View for State objects"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"])
def states():
    """Retrieves all State objects"""
    objs = storage.all(State)
    return jsonify([obj.to_dict() for obj in objs.values()])


@app_views.route("/states/<state_id>", methods=["GET"])
def state(state_id):
    """Retrieves a State object"""
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """Deletes a State object"""
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states", methods=["POST"])
def create_state():
    """Creates a new State object"""
    info = request.get_json()
    if not info:
        abort(400, "Not a JSON")
    if "name" not in info:
        abort(400, "Missing name")
    obj = State(**info)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """Updates an existing State object"""
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)

    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    for k, v in req.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(obj, k, v)

    storage.save()
    return jsonify(obj.to_dict())
