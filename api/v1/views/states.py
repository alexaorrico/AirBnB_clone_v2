#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage


@app_views.route('/states', strict_slashes=False)
def all_states():
    """
    Return list of the all states
    """
    states_list = []
    states_obj = storage.all("State")
    for _,value in states_obj.items():
        states_list.append(value.to_dict())
    return jsonify(states_list)

@app_views.route('/states/<state_id>')
def state(state_id):
    """
    Return  a state with the id
    """
    state = storage.get("State", state_id)
    if state is not None:
        return jsonify(state.to_dict())
    return jsonify({"error": "Not found"}), 404

@app_views.route('/states/<state_id>', methods=['DELETE'])
def del_state(state_id):
    """
    Delete a state with id
    """
    state = storage.get("State", state_id)
    if state is not None:
        storage.delete(state)
        storage.save()
        return jsonify()
    return jsonify({"error": "Not found"}), 404

@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    if not request.json or not 'name' in request.json:
        abort(404)
    state = request.json
    new_state = State(**state)
    storage.save()
    return jsonify(new_state.to_dict()), 201

@app_views.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": "Not found"}), 404
