#!/usr/bin/python3
"""Index file"""

from flask import jsonify, abort, request
from models import storage
from api.v1.views import state_views
from models.state import State


@state_views.route('/', methods=['GET', 'POST'])
@state_views.route('/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def states(state_id=None):
    """Returns states in storage"""
    if state_id is None:
        if request.method == 'GET':
            states_dict = [v.to_dict() for k, v in storage.all(State).items()]
            return jsonify(states_dict)
        elif request.method == 'POST':
            state_dict = request.get_json()
            if (state_dict is None):
                abort(404)
            else:
                if (state_dict.get('name', None)) is None:
                    abort(404)
                new_state = State(**state_dict)
                new_state.save()
                return jsonify(new_state.to_dict()), 201
    else:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
            return
        if request.method == 'GET':
            return jsonify(state.to_dict())
        if request.method == 'PUT':
            state_dict = request.get_json()
            if state_dict is None:
                abort(404)
            else:
                if (state_dict.get('name', None)) is None:
                    abort(404)
                for k, v in state_dict.items():
                    if k not in ['id', 'created_at', 'updated_at']:
                        setattr(self, k, v)
                    state.save()
                return jsonify(state.to_dict()), 200