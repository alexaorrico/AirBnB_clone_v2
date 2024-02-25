#!/usr/bin/python3
""" State view """

from api.v1.views import app_views
from flask import jsonify, abort
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def list_states():
    """ Lists all State objects """
    all_states = storage.all('State')
    return jsonify([state.to_dict() for state in all_states.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_id(state_id):
    """ Returns the State object with the given id """
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state_id(state_id):
    """ Deletes an object via its ID """
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    else:
        storage.get('State', state_id).delete()
        return {}
