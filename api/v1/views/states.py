#!/usr/bin/python3
"""Module to handle the GET, POST, and PUT methods for states"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<state_id>',
                methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def states(state_id=None):
    all_states = storage.all(State)
    state_list = [one_state.to_dict() for one_state in all_states.values()]
    if not state_id:
        if request.method == 'GET':
            return jsonify(state_list)
        elif request.method == 'POST':
            input_json = request.get_json()
            if not input_json:
                abort(400, "Not a JSON")
            if input_json["name"] is None:
                abort(400, "Missing name")
            new_state = State(**input_json)
            new_state.save()
            return jsonify(new_state.to_dict()), 201
    
    if state_id:
        state_obj = storage.get(State, state_id)
        if state_obj is None:
            abort(404)
        if request.method == 'GET':
            return jsonify(state_obj.to_dict()), 200
        elif request.method == 'DELETE':
            storage.delete(state_obj)
            storage.save()
            return jsonify({}), 200
        elif request.method == 'PUT':
            input_json = request.get_json()
            if not input_json:
                abort(400, "Not a JSON")
            if not input_json["name"]:
                abort(400, "Missing name")
            state_obj.name = input_json["name"]
            state_obj.save()
            return jsonify(state_obj.to_dict()), 200
