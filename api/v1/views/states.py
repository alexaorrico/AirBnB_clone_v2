#!/usr/bin/python3
""" States view """

from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def all_states():
    """ all State objects """
    return (jsonify([state.to_dict() for state in storage.all("State").values()]))


@app_views.route('/states/<state_id>', strict_slashes=False)
def a_state(state_id):
    """ retrieves a State object by id """
    try:
        return (jsonify(storage.all("State").pop("State." + state_id).to_dict()))
    except KeyError:
        abort(404)
