#!/usr/bin/python3
"""Create a new view for State objects that
handles all default RESTFul API"""

from models.base_model import BaseModel
from models.state import State
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def states():
    """getting all members of state"""
    state_object = storage.all('State').values()
    state_list = []
    for item in state_object:
        state_list.append(item.to_dict())
    return jsonify(state_list)


@app_views.route("/states/<string:state_id>",
                 methods=['GET'], strict_slashes=False)
def get_states(state_id=None):
    """getting a particular state"""
    state_object = storage.get(State, state_id)
    if state_object is None:
        abort(404)
    return jsonify(state_object.to_dict()), 'OK'
