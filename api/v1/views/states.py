#!/usr/bin/python3
"""
flask application module for retrieval of
State Objects
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.exceptions import BaseModelInvalidObject
from models.state import State


@app_views.route('/states',
                 methods=['GET'],
                 strict_slashes=False)
def get_all_states():
    """Retrieves the list of all State objects"""
    return (jsonify(State.api_get_all()), 200)


@app_views.route('/states',
                 methods=['POST'],
                 strict_slashes=False)
def post_states():
    """Retrieves the list of all State objects"""
    returnedValue, code = State.api_post(
                ["name"],
                request.get_json(silent=True))
    return (jsonify(returnedValue), code)


@app_views.route('/states/<string:state_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_state_by_id(state_id):
    """handles get State object: state_id"""
    try:
        return (jsonify(
            State.api_get_single(state_id)), 200)
    except BaseModelInvalidObject:
        abort(404)

@app_views.route('/states/<string:state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_state_by_id(state_id):
    """handles State object: state_id"""
    try:
        return (jsonify(
            State.api_delete(state_id)), 200)
    except BaseModelInvalidObject:
        abort(404)

@app_views.route('/states/<string:state_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def put_state_by_id(state_id):
    """handles State object: state_id"""
    returnedValue, code = State.api_put(
                ['id', 'created_at', 'updated_at'],
                request.get_json(silent=True),
                storage.get("State", state_id))
    if code == 404:
        abort(404)
    storage.save()
    return (jsonify(returnedValue), code)
