#!/usr/bin/python3
""" New view for State objects that handles all default RESTFul API actions"""
from models.state import State
from api.v1.views import app_views
from models import storage
from flask.json import jsonify
from flask import request
from flask import abort


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states():
    """Retrieves the list of all State objects"""
    states = []
    all_states = storage.all("State")
    for state in all_states.values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>',
                 strict_slashes=False,
                 methods=['GET'])
def get_state_id(state_id):
    """Retrieves a State object"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404, 'Not found')
    else:
        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """ Deletes a State object """
    state = storage.get('State', state_id)
    if state is None:
        abort(404, 'Not found')
    else:
        state.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """ Creates a State / request"""
    json_req = request.get_json()
    if json_req is None:
        abort(400, 'Not a JSON')
    elif "name" not in json_req:
        abort(400, 'Missing name')
    else:
        new_state = State(**json_req)
        new_state.save()
        check_create_state = storage.get('State', new_state.id)
        return jsonify(check_create_state.to_dict()), 201


@app_views.route('/states/<state_id>',
                 strict_slashes=False,
                 methods=['PUT'])
def update_state(state_id):
    """ Updates a State object """
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404, 'Not found')
    else:
        json_req = request.get_json()
        if json_req is None:
            abort(400, 'Not a JSON')
        else:
            state_obj.update(json_req)
            state_obj.save()
            check_update_state = storage.get('State', state_id)
            return jsonify(check_update_state.to_dict()), 200
