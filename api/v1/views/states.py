#!/usr/bin/python3
"""
Module that creates a view for States
"""

from flask import jsonify, abort, request
from api.v1.views.__init__ import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def index(state_id=None):
    """
    Retrieves a list of all state objects on
    GET /api/v1/states request
    """
    if state_id is None:
        states_obj = list(storage.all(State).values())
        states_list = list(state.to_dict() for state in states_obj)
        return jsonify(states_list)
    else:
        obj = storage.get(State, state_id)
        if obj is not None:
            return jsonify(obj.to_dict())
        else:
            abort(404)


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def post_state():
    """
    Posts a state object on
    POST /api/v1/states request
    """
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        abort(400, description='Not a JSON')
    else:
        json = request.get_json()
        if json is None:
            abort(400, description='Not a JSON')
        if 'name' in json.keys():
            obj = State(**json)
            obj_id = obj.id
            obj.save()
            return index(obj_id), 201
        else:
            abort(400, description='Missing name')


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    """
    Deletes a state object on
    DELETE /api/v1/states/<state_id> request
    """
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """
    Replaces a state object on
    PUT /api/v1/states/<state_id> request
    """
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)

    else:
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            abort(400, description='Not a JSON')
        else:
            json = request.get_json()
            if json is None:
                abort(400, description='Not a JSON')
            for key, value in json.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(obj, key, value)
                storage.save()
            return index(state_id), 200
