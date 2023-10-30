#!/usr/bin/python3
"""Module containing a Flask Blueprint routes that handles
all default RESTFul API actions for State resource"""
from api.v1.views import app_views
from flask import abort, make_response, jsonify, request
from markupsafe import escape
from models import storage
from models.state import State


def retrive_object(state_id):
    """Retrives a State resource based of id."""
    obj = storage.get(State, escape(state_id))
    if obj is None:
        abort(404)
    return (obj)


def validate_request_json(request):
    """Checks validity of request's json content"""
    if not request.is_json:
        abort(make_response(jsonify(error="Not a JSON"), 400))
    req_json = request.get_json()
    if request.method == 'POST' and 'name' not in req_json:
        abort(make_response(jsonify(error="Missing name"), 400))
    return (req_json)


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_get(state_id=None):
    """Returns a State resource if id is given, else returns all states"""
    if state_id is None:
        states_list = [obj.to_dict() for obj in storage.all(State).values()]
        return (jsonify(states_list))
    obj = retrive_object(state_id)
    return (jsonify(obj.to_dict()))


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def states_delete(state_id):
    """Deletes a State resource if given id is found."""
    obj = retrive_object(state_id)
    storage.delete(obj)
    storage.save()
    return (jsonify({}))


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def states_post():
    """Creates a State resource if request content is valid."""
    req_json = validate_request_json(request)
    new_state = State(**req_json)
    new_state.save()
    return (jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def states_put(state_id):
    """Updates a State resource of given id if request content is valid."""
    obj = retrive_object(state_id)
    req_json = validate_request_json(request)
    ignore = ['id', 'created_at', 'updated_at']
    for key, value in req_json.items():
        if key not in ignore:
            setattr(obj, key, value)
    obj.save()
    return (jsonify(obj.to_dict()))
