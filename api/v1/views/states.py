#!/usr/bin/python3
"""handles all default RESTFul API actions for State"""
from api.v1.views import states_views
from models import storage
from models.state import State
from flask import request, jsonify as js


@states_views.route('/states')
@states_views.route('/states/<state_id>')
def all_states(state_id=None):
    """retrieves the list of all State objects"""
    if state_id is None:
        states = storage.all(State)
        try:
            return js([state.to_dict() for state in states.values()])
        except Exception as e:
            return js({"Error retrieving states": "{}".format(e)})
    else:
        try:
            states = storage.all(State)
            for state in states.values():
                if state.id == state_id:
                    return js(state.to_dict())
        except Exception as e:
            return js({"Error retrieving a State": "{}".format(e)})
    return js({"error": "Not found"}), 404


@states_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """deletes a State object:"""
    states = storage.all(State)
    for key, state in states.items():
        if key.split('.')[1] == state_id:
            try:
                storage.delete(state)
                storage.save()
                return {}
            except Exception as e:
                return js({"Error deleting a State": "{}".format(e)})
    return js({"error": "Not found"}), 404


@states_views.route('/states', methods=['POST'])
def create_state():
    """creates and returns a State object"""
    # check HTTP body for a valid JSON
    # if using cURL, append "Content-Type" header for is_json
    # property to check for valid JSON.
    if not request.is_json:
        return js({"error": "Not a JSON"}), 400
    # retrieve json
    request_info = request.get_json()
    # check for a name value in JSON
    if request_info.get('name'):
        state = State(name=request_info.get('name'))
        return js(state.to_dict()), 201
    return js({"error": "Missing name"}), 400


@states_views.route('states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """updates a State object"""
    # check for a State object with state_id
    state = storage.get(State, state_id)
    if not state:
        return js({"error": "State object does not exist"}), 404
    # check HTTP body for a valid JSON
    if not request.is_json:
        return js({"error": "Not a JSON"}), 400
    # retrieve json
    request_info = request.get_json()
    # check for keys to be updated
    attrs_to_ignore = ["id", "created_at", "updated_at"]
    for attr, value in request_info.items():
        if attr not in attrs_to_ignore:
            state.__setattr__(attr, value)
    # persist changes to storage engine
    storage.save()
    return js(state.to_dict()), 200
