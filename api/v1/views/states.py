#!/usr/bin/python3
"""State Objects"""
from api.v1.views import *
from flask import Flask, jsonify
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False, methods=['GET'])
def state(state_id=None):
    """GET Method"""
    return jsonify([obj.to_dict() for obj in storage.all('State').values()])


@app_views.route("/states/<state_id>", methods=['GET'])
def get_state_id(state_id=None):
    """"State by id GET Method"""
    if state_id:
        return get_object(State, state_id)


@app_views.route("/states/<state_id>", methods=['DELETE'])
def delete_state(state_id):
    """Delete a State DELETE Method"""
    return delete(State, state_id)


@app_views.route("/states", strict_slashes=False, methods=['POST'])
def post_sate():
    """POST Method"""
    return post(State, None, None, {"name"})


@app_views.route("/states/<state_id>", methods=['PUT'])
def put_state(state_id):
    """PUT Method"""
    return put(State, state_id, ["id", "created_at", "updated_at"])
