#!/usr/bin/python3
"""
Handles all default RESTful API actions for State objects
"""

from . import app_views
from models.state import State
from flask.json import jsonify
from flask import abort
from flask import make_response
from models import storage
from flask import request

STATE_IGNORE_KEYS = {'id', 'created_at', 'updated_at'}


@app_views.route("/states", methods=['GET'])
def states():
    """Retrieves the list of all State objects"""
    return jsonify([s.to_dict() for s in storage.all('State').values()])


@app_views.route("/states/<state_id>", methods=['GET'])
def get_state(state_id):
    """Retrieves a state given its ID"""
    try:
        return jsonify(storage.get('State', state_id).to_dict())
    except AttributeError:
        abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'])
def del_state(state_id):
    """Deletes a state given its ID"""
    try:
        storage.get('State', state_id).delete()
        return make_response(jsonify({}), 200)
    except AttributeError:
        abort(404)


@app_views.route("/states", methods=['POST'])
def post_state():
    """Creates a state"""
    try:
        r = request.get_json()
        if 'name' not in r:
            abort(make_response(jsonify("Missing name"), 400))
        s = State(**r)
        s.save()
        return make_response(jsonify(s.to_dict()), 201)
    except TypeError:
        abort(make_response(jsonify("Not a JSON"), 400))


@app_views.route("/states/<state_id>", methods=['PUT'])
def put_state(state_id):
    """Updates a State at a given ID"""
    try:
        s = storage.get('State', state_id)
        if s is None:
            abort(404)
        r = request.get_json()
        for key, value in r.items():
            if key not in STATE_IGNORE_KEYS:
                setattr(s, key, value)
    except AttributeError:
        abort(make_response(jsonify("Not a JSON"), 400))
    s.save()
    return make_response(jsonify(s.to_dict()), 200)
