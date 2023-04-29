#!/usr/bin/python3
""" State objects that handles all default RESTFul API """
from flask import jsonify
from flask import request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

from api.v1.views import app_views
from models import storage
from models.state import State

ALLOWED_METHODS = ['GET', 'POST', 'PUT', 'DELETE']

""" allowed methods for the states endpoint"""


@app_views.route('/states', methods=ALLOWED_METHODS)
@app_views.route('/states/<state_id>', methods=ALLOWED_METHODS)
def handle_states(state_id=None):
    """ handler for the sates endpioint"""
    handlers = {
            'GET': get_state_data,
            'DELETE': remove_state,
            'POST': add_state,
            'PUT': update_state,
            }
    if request.method in handlers:
        return handlers[request.method](state_id)
    else:
        return MethodNotAllowed(list(handlers.key()))


def get_state_data(state_id=None):
    """Gets the state with it id or get all states."""
    all_states = storage.all(State).values()
    if state_id:
        matching_states = list(filter(lambda x: x.id == state_id, all_states))
        if matching_states:
            return jsonify(matching_states[0].to_dict())
        raise NotFound()
    all_states = list(map(lambda x: x.to_dict(), all_states))
    return jsonfiy(all_states)


def remove_state(state_id=None):
    """ delete state with the given id"""
    all_states = storage.all(State).values()
    matching_states = list(filter(lambda x: x.id == state_id, all_states))
    if matching_states:
        storage.delete(matching_states[0])
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def add_state(state_id=None):
    """ Adds a new state"""
    request_data = request.get_json()
    if type(request_data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in request_data:
        raise BadRequest(description='Missing name')
    state_to_add = State(**request_data)
    state_to_add.save()
    return jsonify(state_to_add.to_dict()), 201


def update_state(state_id=None):
    """ update the state with the given id"""
    keys = ('id', 'created_at', 'updated_at')
    all_states = storage.all(State).values()
    matching_states = list(filter(lambda x: x.id == state_id, all_states))
    if matching_states:
        request_data = request.get_json()
        if type(request_data) is not dict:
            raise BadRequest(description='Not a JSON')
        old_state = matching_states[0]
        for key, value in request_data.items():
            if key not in keys:
                setattr(old_state, key, value)
                old_state.save()
                return jsonify(old_state.to_dict()), 200
            raise NotFound()
