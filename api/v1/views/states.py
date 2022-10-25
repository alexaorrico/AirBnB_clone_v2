#!/usr/bin/python3

"""Module to handle state request Blueprint"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """return json array of all states"""
    states = storage.all(State).values()
    all_states = []
    for state in states:
        all_states.append(state.to_dict())
    return jsonify(all_states)
