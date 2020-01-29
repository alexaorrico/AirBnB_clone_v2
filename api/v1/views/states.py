#!/usr/bin/python3
"""
Handles all default RESTful API actions for State objects
"""

from . import app_views
from models.state import State
from flask.json import jsonify
from flask import abort
from models import storage


@app_views.route("/states", methods=['GET'])
def states():
    """Retrieves the list of all State objects"""
    return jsonify([state.to_dict() for state in storage.all('State').values()])

@app_views.route("/states/<state_id>", methods=['GET'])
def state(state_id):
    """Retrieves a state given its ID"""
    try:
        s = storage.all('State')
        return jsonify(s['State.' + state_id].to_dict())
    except KeyError:
        abort(404)
