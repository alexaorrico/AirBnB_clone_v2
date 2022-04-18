#!/usr/bin/python3
"""State view model"""
from flask import abort
from flask import jsonify
from flask import request
from models import storage
from models.state import State
from api.v1.views import app_views

# states_objs = storage.all('State')


<<<<<<< HEAD
@app_views.route('/states/', methods=['GET'])
=======

@app_views.errorhandler(404)
def not_found(error):
    """ 404 - Not found function """
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route('/states', methods=['GET'])
>>>>>>> 5b59787121a426bfb78aeb21694265d3d0c482c1
def get_states():
    """Returns a list of all state models."""
    states_objs = storage.all('State')
    states = [obj.to_dict() for obj in states_objs.values()]

    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Returns a specified state model."""
    states_objs = storage.all('State')
    state_id = "State." + state_id

    if state_id not in states_objs.keys():
        abort(404)

<<<<<<< HEAD
    state = states_objs.get(state_id)

    return jsonify(state.to_dict())
=======
    return jsonify(states[state_id],)
>>>>>>> 5b59787121a426bfb78aeb21694265d3d0c482c1


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a specified state model."""
    states_objs = storage.all('State')
    state_id = "State." + state_id

    if state_id not in states_objs.keys():
        abort(404)

<<<<<<< HEAD
    storage.all().pop(state_id)
    storage.save()

=======
    del states[state_id]
>>>>>>> 5b59787121a426bfb78aeb21694265d3d0c482c1
    return jsonify({}), 200, {'ContentType': 'application/json'}


@app_views.route('/states/', methods=['POST'])
def create_state():
    """Creates a new state object."""
    if not request.json:
        abort(400, "Not a JSON")
    if "name" not in request.get_json().keys():
        abort(400, 'Missing name')

    state = (State(**request.get_json()))
    storage.new(state)
    return state.to_dict(), 201, {'ContentType': 'application/json'}


@app_views.route('/states/<state_id>', methods=["PUT"])
def update_state(state_id):
    """Modifies a state object."""
    states_objs = storage.all('State')
    state_id = "State." + state_id

    if not request.json:
        abort(400, "Not a JSON")
    if state_id not in states_objs.keys():
        abort(404)

<<<<<<< HEAD
    state = State(**request.get_json())
    state.save()

    return state.to_dict(), 200, {'ContentType': 'application/json'}
=======
    states[state_id]['name'] = \
        request.get_json.get('name', states[state_id]['name'])
    states[state_id]['__class__'] = request.get_json.get(
        'name', states[state_id]['__class__'])

    return states[state_id], 200, {'ContentType': 'application/json'}
>>>>>>> 5b59787121a426bfb78aeb21694265d3d0c482c1
