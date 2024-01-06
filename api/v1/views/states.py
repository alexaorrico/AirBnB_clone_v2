#!/usr/bin/python3
"""imports app_views and creates a route /status"""

from flask import jsonify, Blueprint
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json


@app_views.route("/states")
def return_states():
    """returns all state objects"""
    states = State.query.all()
    states_list = []
    for state in states:
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route("/states/<state_id>", strict_slashes=False)
def return_state(state_id):
    state = storage.get(state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())
