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


@app_views.route("/states", methods=['GET'])
def states():
    """Retrieves the list of all State objects"""
    return jsonify([s.to_dict() for s in storage.all('State').values()])


@app_views.route("/states/<state_id>", methods=['GET'])
def state(state_id):
    """Retrieves a state given its ID"""
    try:
        return jsonify(storage.get('State', state_id).to_dict())
    except KeyError:
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
        s = State(**request.get_json())
        s.save()
        return make_response(jsonify(s.to_dict()), 200)
    except TypeError:
        abort(404)
