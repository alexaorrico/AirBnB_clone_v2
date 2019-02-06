#!/usr/bin/python3
""" prepares data for easier viewing """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_all_states():
    """ Returns all the state obj in json """
    states = storage.all(State).values()
    states = [state.to_dict() for state in states]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id=None):
    """ Returns all the state obj in json """
    state = storage.get('State', state_id)
    state.delete()
    storage.save()
    return jsonify({}), 201


@app_views.route('/states', methods=['POST'])
def create_state():
    """ state creator """
    import pdb; pdb.set_trace()
    state_json = ""
    try:
        data = request.get_json()
    except:
        return jsonify(error="Not a JSON"), 400
    if not data.get('name'):
        return jsonify(error="Missing name"), 400
    state = State(**data)
    state.save()