#!/usr/bin/python3
"""Index file"""

from flask import jsonify, abort, request
from models import storage
from api.v1.views import state_views
from models.state import State


@state_views.route('/states', methods=['GET', 'POST'])
@state_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def states(state_id=None):
    """Returns states in storage"""
    if state_id is None:
        if request.method == 'GET':
            states_dict = [x.to_dict() for x in storage.all(State)]
            return jsonify(states_dict)
        else:
            state_dict = request.get_json()
            print(state_dict)
    else:
        states_dict = storage.get(State, state_id).to_dict()
        if states_dict is None:
            abort(404)
        else:
            return jsonify(states_dict)