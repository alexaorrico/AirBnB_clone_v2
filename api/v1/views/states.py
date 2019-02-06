#!/usr/bin/python3
""" prepares data for easier viewing """
from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """ Returns all the state obj in json """
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])
