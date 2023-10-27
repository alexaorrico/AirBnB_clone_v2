#!/usr/bin/python3
"""module containing a Flask Blueprint routes that handles
all default RESTFul API actions for State resource"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from markupsafe import escape
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_get(state_id=None):
    """returns a state resource if id is given, else returns all states"""
    if not state_id:
        states_list = [obj.to_dict() for obj in storage.all(State).values()]
        return (jsonify(states_list))
    key = 'State.' + escape(state_id)
    obj = storage.all(State).get(key)
    if not obj:
        abort(404)
    return (jsonify(obj.to_dict()))


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def states_delete(state_id):
    """deletes a state resource if given id is found."""
    key = 'State.' + escape(state_id)
    obj = storage.all(State).get(key)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def states_post():
    """Creates a state resource if request content is valid."""
    req_json = request.get_json(silent=True)
    if not req_json:
        return make_response(jsonify({'message': "Not a JSON"}), 400)
    if 'name' not in req_json:
        return make_response(jsonify({'message': "Missing name"}), 400)
    new_state = State(**req_json)
    new_state.save()
    return (jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def states_put(state_id):
    """updates a state resource with given id."""
    key = 'State.' + escape(state_id)
    obj = storage.all(State).get(key)
    if not obj:
        abort(404)
    req_json = request.get_json(silent=True)
    if not req_json:
        return make_response(jsonify({'message': "Not a JSON"}), 400)
    ignore = ['id', 'created_at', 'updated_at']
    for key, value in req_json.items():
        if key not in ignore:
            setattr(obj, key, value)
    obj.save()
    return (jsonify(obj.to_dict()), 200)
