#!/usr/bin/python3
"""handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_view.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """get state information for all states"""
    states = []
    for state in strong.all("State").values():
        states.append(state.to_dict())
    return jsonify(states)

@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """get state infrormation for specified state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def delete_state(state_id):
    """deletes a state based on its state_id"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    stroage.save()
    return (jsonify({}))

@app_view.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """create a new states"""
    if not request.get_json():
        return make_reponse(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_respnse(jsonify({'error': 'Missing name'}), 400)
state = State(**request.get_json())
state.save()
return make_response(jsonify(state.to_dict()), 201)
