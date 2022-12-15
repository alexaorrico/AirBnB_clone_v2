#!/usr/bin/python3
""" new view for State objects """

from models import storage
from api.v1.views import app_views
from models.state import State
from flask import Flask, make_response, jsonify


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>')
def states(state_id=None):
    """ Retrieves the list of all State objects """
    if state_id is not None:
        obj = storage.get(State, state_id)
        if obj is None:
            return make_response(jsonify({'error': 'Not found'}), 404)
        else:
            return obj.to_dict()
    else:
        state_objs = [state.to_dict() for state in storage.all(State).values()]
        return state_objs
