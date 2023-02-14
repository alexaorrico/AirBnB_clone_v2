#!/usr/bin/python3
"""Module for State related endpoints"""
from api.v1.views import app_views
from api.v1.views import *
from flask import jsonify, make_response, abort, request
from models import storage
from models.state import State


model = "State"


@app_views.route("/states", strict_slashes=False,
                 methods=["GET"], defaults={"state_id": None})
@app_views.route("/states/<state_id>", methods=["GET"])
def get_state(state_id):
    """GET /state api route"""
    if not state_id:
        list_objs = [v.to_dict() for v in storage.all(model).values()]
        return jsonify(list_objs)

    return get_model(model, state_id)


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """DELETE /state api route"""
    return delete_model(model, state_id)


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def post_state():
    """POST /state api route"""
    required_data = {"name"}
    return post_model(model, None, None, required_data)


@app_views.route("/states/<state_id>", methods=["PUT"])
def put_state(state_id):
    """PUT /state api route"""
    ignore_data = ["id", "created_at", "updated_at"]
    return put_model(model, state_id, ignore_data)
