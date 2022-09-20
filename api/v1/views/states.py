#!/usr/bin/python3
"""
flask application module for retrieval of
State Objects
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


@app_views.route('/states',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def get_all_states():
    """Retrieves the list of all State objects"""
    if request.method == 'GET':
        returnedValue, code = State.api_get_all(
                    storage.all("State").values()
        )
    if request.method == 'POST':
        returnedValue, code = State.api_post(
                    ['name'],
                    request.get_json())
    return (jsonify(returnedValue), code)


@app_views.route('/states/<string:state_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def state_by_id(state_id):
    """handles State object: state_id"""
    if request.method == 'GET':
        returnedValue, code = State.api_get_single(
                        storage.get("State", state_id))
    if request.method == 'DELETE':
        returnedValue, code = State.api_delete(
                    storage.get("State", state_id))
    if request.method == 'PUT':
        returnedValue, code = State.api_put(
                    ['id', 'created_at', 'updated_at'],
                    request.get_json(),
                    storage.get("State", state_id))
    if code == 404:
        abort(404)
    storage.save()
    return (jsonify(returnedValue), code)
